#!/usr/bin/python3

import requests
import re
import json

http_proxy  = "http://127.0.0.1:8888"
https_proxy = "https://127.0.0.1:8888"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy,
            }

def verify_link(link):
    result = re.match(r'https?:\/\/hdonline.vn\/[\w-]+.html', link, re.M | re.I)
    if result is None:
        return False
    return True


def get_link_video(link):
    headers = dict()
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Cache-Control'] = 'max-age=0'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = 'hdonline.vn'
    headers['Referer'] = link
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'


    s = requests.session()
    s.cookies.clear()

    r = s.get(link, headers=headers, proxies=proxyDict)
    r.close()

    body = r.text

    # print(r.text)
    # print(r.headers)

    # lay cooie
    cookie = re.search(r'__cfduid=[\w]+', r.headers['Set-Cookie'], re.M | re.I).group()

    # lay PHPSESSID
    php_sess_id = re.search(r'PHPSESSID=[\w]+', r.headers['Set-Cookie'], re.M | re.I).group()

    # lay fid
    fid = re.search(r'PlayFilm.*\d+', body, re.M | re.I).group()
    fid = re.search(r'\d+', fid, re.M | re.I).group()

    # lay token
    token = re.search(r'\w{86,96}.*?\d{10}', body, re.M | re.I).group()
    token = token.replace('|', '-')

    headers = dict()
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Cache-Control'] = 'max-age=0'
    headers['Connection'] = 'keep-alive'
    headers['Cookie'] = cookie +'; ' + php_sess_id + ';'
    headers['Host'] = 'hdonline.vn'
    headers['Referer'] = link
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
    
    s.cookies.clear()
    
    xmlplay_url = 'http://hdonline.vn/frontend/episode/xmlplay?ep=1&fid=' + fid + '&token=' + token + '&format=json'
    r = s.get(xmlplay_url, headers=headers, proxies=proxyDict)
    r.close()

    data = json.loads(r.text)
    return body, data

def getLink(url):
    link = url
    if verify_link(link) is False:
        print('Duong dan khong hop le!')
        exit()
    link = link.strip()
    return get_link_video(link)
