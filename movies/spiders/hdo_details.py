# -*- coding: utf-8 -*-
import scrapy
import pymongo
import re
import requests
import json
from movies.items import DetailsItem
import movies.settings as settings

http_proxy  = "http://127.0.0.1:8888"
https_proxy = "https://127.0.0.1:8888"

proxyDict = { 
    "http"  : http_proxy, 
    "https" : https_proxy,
}

class HdoDetailsSpider(scrapy.Spider):
    name = 'hdo_details'
    collection_name = 'hdo'
    eps = {}

    def __init__(self):
        self.mongo_uri = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DATABASE
        self.client = None
        self.db = None


    def start_requests(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        collection = self.db[self.collection_name]
        objs = collection.find()
        print('Find done')
        for obj in objs:
            url = obj["url"]
            headers = dict()
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Accept-Encoding'] = 'gzip, deflate, sdch'
            headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
            headers['Cache-Control'] = 'max-age=0'
            headers['Connection'] = 'keep-alive'
            headers['Host'] = 'hdonline.vn'
            headers['Referer'] = url
            headers[
                'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'

            yield scrapy.Request(url)
        pass

    def parse(self, response):
        eps_data = self.eps

        print(self.eps)

        body = response.text

        data = getData(response)

        link = response.url

        # try:
        #     cookies = response.headers.getlist('Set-Cookie')
        #     test = "".join(str(x) for x in cookies)
        #     # lay cooie
        #     cookie = re.search(r'__cfduid=[\w]+', test, re.M | re.I).group()

        #     # lay PHPSESSID
        #     php_sess_id = re.search(r'PHPSESSID=[\w]+', test, re.M | re.I).group()

        #     link = response.url

        #     headers = dict()
        #     headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        #     headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        #     headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
        #     headers['Cache-Control'] = 'max-age=0'
        #     headers['Connection'] = 'keep-alive'
        #     headers['Cookie'] = cookie +'; ' + php_sess_id + ';'
        #     headers['Host'] = 'hdonline.vn'
        #     headers['Referer'] = link
        #     headers[
        #         'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
        #     s = requests.session()
        #     s.cookies.clear()
        #     playlist = eps_data["playlist"]
        #     eps = []
        #     for x in playlist:
        #         f = x['file']
        #         pos= f.find('&mirand')
        #         f = f[:pos]
        #         xmlplay_url = 'http://hdonline.vn'+f+'&format=json'
        #         r = s.get(xmlplay_url, headers=headers, proxies=proxyDict)
        #         r.close()
        #         s.cookies.clear()
        #         if r.status_code == 200:
        #             d = json.loads(r.text)
        #             item = {
        #                 'file': d['file'],
        #                 'level': d['level'],
        #                 'audiodub' : d['audiodub'],
        #                 'mediaid' : d['mediaid'],
        #                 'image' : d['image'],
        #                 'subtitle' : d['subtitle']
        #             }
        #             eps.append({
        #                 'ep': x['title'],
        #                 'data': item
        #             })
        # except:
        #     pass

        filmID = link.split('-')
        filmID = filmID[-1]
        filmID = filmID.split('.')[0]
        data['filmID'] = filmID
        # data['playlist'] = eps
        details = DetailsItem()
        details['data'] = data
        print(data)
        yield details

keys = {
    'Tên Phim: ' : 'nameVi',
    'Tên Tiếng Anh: ' : 'nameEn',
    'Tên Gốc: ' : 'nameOr',
    'Năm sản xuất: ' : 'year',
    'Thể loại: ' : 'genre',
    'Quốc gia: ' : 'country',
    'Đạo diễn: ' : 'director',
    'Thời lượng' : 'duration',
    'Phim Hành Động' : 'action', 
    'Phim Phiêu Lưu' : 'adventure', 
    'Phim Kinh Dị' : 'horror', 
    'Phim Tình Cảm' : '', 
    'Phim Hoạt Hình' :'', 
    'Phim Võ Thuật' : '', 
    'Phim Hài Hước' : 'comdy', 
    'Phim Tâm Lý' : '', 
    'Phim Viễn Tưởng' : 'sci-fi', 
    'Phim Thần Thoại' : '', 
    'Phim Lịch Sử' : 'historical', 
    'Phim TV-Show' : 'TV-show', 
    'Phim Tài Liệu' : 'documentary', 
    'Phim Kịch Tính' : 'thriller', 
    'Phim Gia Đình' : 'family', 
    'Phim Thể Thao' : '', 
    'Phim Bí Ẩn' : '', 
    'Phim Viễn Tây' : ''
    }

def crawlInfo(a,data):
    ul = a.xpath('.//ul[@class="filminfo-fields"]')[0]
    li = ul.xpath('.//li')
    img = li[0].xpath('.//img/@src').extract()[0]
    data["poster_ver"] = img
    for x in li[1:]:
        title = x.xpath('.//text()').extract()
        title = [s for s in title if not s == ', ']
        if len(title) > 1:
            if not title[0] ==  'Thể loại: ':
                data[keys[title[0]]] = title[1]
            else:
                data[keys[title[0]]] = title[1:]
        else:
            title = title[0].split(':')
            if len(title) > 1:
                number = re.search(r'\b\d+\b',title[1])[0]
                data[keys[title[0]]] = int(number)
    description = a.xpath('.//div[@itemprop="description"]/p//text()[not(ancestor::a)]').extract()
    data["description"] = ''.join(description)
    cast = a.xpath('.//li[@class="media"]//div/span[1]/a/text()').extract()
    data["cast"] = cast

def crawlTrailer(a,data):
    src = a.xpath("./iframe/@src").extract()[0]
    match = re.search(r'file=.*',src,flags= re.M)
    link = src[match.start()+5:]
    data["trailer"] = link

def getData(response):
    divs = response.xpath('//div[@class="block-movie"]')
    divs = [x for x in divs if len(x.xpath('.//div[@class="header-block-title"]'))>0]
    divs = divs[0:-1]
    data = dict()
    data["category"] = 'Movie'
    isSeries = False
    for x in divs:
        title = x.xpath('.//div[@class="header-block-title"]/text()').extract()[0]
        if title.find("Thông tin") >= 0:
            crawlInfo(x,data)
        elif title.find("Trailer") >= 0:
            crawlTrailer(x,data)
        elif title.find("Tập") >= 0:
            tmp = re.search(r'\(.*/',title,flags= re.M)
            status = title[tmp.start()+1:tmp.end()-1]
            isSeries = True
            data["current"] = int(status)

    body = response.text
    try:
        tmp = self.eps
        img = tmp['playlist'][0]['image']
        data["poster_hoz"] = img
    except:
        pass

    if isSeries:
        data["status"] = {
            "current" : data["current"],
            "duration" : data["duration"]
        }
        del data["current"]
        del data["duration"]
        data['category'] = 'Series'

    return data