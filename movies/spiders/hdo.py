# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from movies.items import MoviesItem

class HdoSpider(scrapy.Spider):
    name = 'hdo'
    urls = ['phim-le','phim-bo']

    def getUrl(self,cag, page):
        print("Crawl den page {}".format(page))
        return 'http://hdonline.vn/danh-sach/{}/trang-{}.html'.format(cag,page)

    def start_requests(self):
        self.i = 0
        x = self.urls[self.i]
        self.page = 1
        self.cag = x
        print(x)
        yield scrapy.Request(self.getUrl(self.cag,self.page))

    def parse(self, response):
        boxs = response.xpath('//div[@class=$val]',val='tn-bxitem')
        count = 0
        for box in boxs:
            film = MoviesItem()
            url = box.xpath('.//a[@class=$val]/@href', val='jt bxitem-link').extract_first()
            filmID = url.split('-')
            filmID = filmID[-1]
            filmID = filmID.split('.')[0]
            film["url"] = url
            film["_id"] = filmID

            yield film
            count += 1
        if count > 0: # Van con item, tim tiep
            print("Tim tiep")
            self.page += 1
            print(self.page)
            yield scrapy.Request(self.getUrl(self.cag,self.page))
        else:
            self.i += 1
            try:
                self.cag = self.urls[self.i]
                self.page = 1
                yield scrapy.Request(self.getUrl(self.cag,self.page))
            except:
                pass
                