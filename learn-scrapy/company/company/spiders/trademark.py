# -*- coding: utf-8 -*-
"""
GET http://api.tmkoo.com/app-reg.php?mobile=b4:52:7e:ca HTTP/1.1
"""
import json
import math
import urllib.parse as urlparse
from datetime import datetime

import pymysql.cursors
import redis
import scrapy

from company.items import TrademarkUrlItem, TrademarkItem

# 连接MySQL数据库
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='testdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# 网站各种url
search_url = "http://api.tmkoo.com/app-search.php?keyword={keyword}&apiKey={key}&apiPassword={password}&pageSize=50&condition=1&intCls=0"
detail_url = "http://api.tmkoo.com/app-info.php?apiKey={key}&apiPassword={password}"
scroll_url = "http://api.tmkoo.com/app-search-scroll.php?logId={logid}&pageSize=50&pageNo={pn}"


def get_new_api(id=1):
    with connection.cursor() as cursor:
        sql = "select `key`, `password` from `tmkoo` where `id` = %s"
        cursor.execute(sql, (id, ))
        row = cursor.fetchone()
    return (row['key'], row['password'])


def get_keyword(start=0, stop=-1):
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.lrange('dynamic_gather_keyword_list', start, stop)


def get_trademark_url(start=0, stop=-1):
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.lrange('company_trademark_url_list', start, stop)


class TrademarkUrlSpider(scrapy.Spider):
    name = 'trademark_url'
    key, password = get_new_api(id=1)
    start_urls = [
        search_url.format(
            keyword=kw.decode(), key=key, password=password
        ) for kw in get_keyword(0, 99)
    ]

    def parse(self, response):
        data = json.loads(response.text)
        if data['ret'] == '0':
            count = int(data['allRecords'])
            if count != 0:
                for r in data['results']:
                    item = TrademarkUrlItem()
                    item['url'] = "&regNo=%s&intCls=%s" % (
                        r['regNo'], r['intCls'])
                    yield item
                query = urlparse.urlsplit(response.url).query
                params = dict(urlparse.parse_qsl(query))
                logid = data['logId'] or params.get('logId', '')
                pn = int(params.get('pageNo', 1)) + 1
                if pn <= math.ceil(count / 50):
                    next_page = scroll_url.format(logid=logid, pn=pn)
                    yield scrapy.Request(next_page, callback=self.parse)
        else:
            log = "ret: %s, remainCount: %s, msg: %s." % (
                data['ret'], data['remainCount'], data['msg'])
            self.log(log)


class TrademarkSpider(scrapy.Spider):
    name = 'trademark'
    key, password = get_new_api(id=1)
    start_urls = [
        detail_url.format(key=key, password=password) + url.decode()
        for url in get_trademark_url(0, 499)
    ]

    def parse(self, response):
        data = json.loads(response.text)
        if data['ret'] == '0':
            item = TrademarkItem()
            item['company_name'] = data['applicantCn']
            item['trademark_class_code'] = data['intCls']
            item['trademark_name'] = data['tmName']
            item['trademark_appli_code'] = data['regNo']
            item['trademark_apply_time'] = data['appDate']
            status = []
            for f in data['flow']:
                s = f['flowDate'] + ' ' + f['flowName']
                status.append(s)
            item['trademark_status'] = '\n'.join(status)
            item['trademark_apply_name'] = data['applicantCn']
            image_weburl = "http://pic.tmkoo.com/pic.php?zch=" + data['tmImg']
            item['trademark_image_weburl'] = image_weburl
            item['trademark_regist_time'] = data['regDate']
            item['trademark_regist_no'] = data['regIssue']
            item['trademark_preli_no'] = data['announcementIssue']
            item['trademark_preli_time'] = data['announcementDate']
            item['trademark_type'] = data['category']
            item['trademark_valid_time'] = data['privateDate']
            item['trademark_agent_name'] = data['agent']
            item['company_url'] = response.url
            item['company_gather_time'] = datetime.now(
            ).strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
        else:
            log = "ret: %s, remainCount: %s, msg: %s." % (
                data['ret'], data['remainCount'], data['msg'])
            self.log(log)
