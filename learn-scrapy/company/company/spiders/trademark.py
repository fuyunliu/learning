# -*- coding: utf-8 -*-
"""
GET http://api.tmkoo.com/app-reg.php?mobile=b4:52:7e:ca HTTP/1.1
"""
import json
import math
import urllib.parse as urlparse
from datetime import datetime

import redis
import scrapy

from company.items import TrademarkUrlItem, TrademarkItem


redis_server = redis.Redis(host='localhost', port=6379, db=0)
scroll_url = "http://api.tmkoo.com/app-search-scroll.php?logId={logid}&pageSize=50&pageNo={pn}"


class TrademarkUrlSpider(scrapy.Spider):
    name = 'trademark_url'
    start_urls = [url.decode() for url in redis_server.lrange(
        'trademark_search_url_list', 0, -1)]

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
    start_urls = [url.decode() for url in redis_server.lrange(
        'trademark_detail_url_list', 0, -1)]

    def parse(self, response):
        data = json.loads(response.text)
        if data['ret'] == '0':
            item = TrademarkItem()
            item['company_name'] = data['applicantCn']
            item['trademark_class_code'] = data['intCls']
            item['trademark_name'] = data['tmName']
            item['trademark_appli_code'] = data['regNo']
            item['trademark_apply_time'] = data['appDate']

            # 商标流程、状态变化
            status = []
            for f in data.get('flow', []):
                s = f['flowDate'] + ' ' + f['flowName']
                status.append(s)
            item['trademark_status'] = '\n'.join(status)

            # 商标服务商品列表
            goods = []
            for g in data.get('goods', []):
                goods.append(g['goodsName'])
            item['trademark_produce_name'] = '，'.join(goods)

            item['trademark_apply_name'] = data['applicantCn']
            item['trademark_regist_time'] = data['regDate']
            item['trademark_regist_no'] = data['regIssue']
            item['trademark_preli_no'] = data['announcementIssue']
            item['trademark_preli_time'] = data['announcementDate']
            item['trademark_specif_color'] = data.get('color', '')
            item['trademark_priority_date'] = data.get('yxqrq', '')
            item['trademark_type'] = data['category']
            item['trademark_valid_time'] = data['privateDate']
            item['trademark_agent_name'] = data['agent']
            image_weburl = "http://pic.tmkoo.com/pic.php?zch=" + data['tmImg']
            item['trademark_image_weburl'] = image_weburl
            item['trademark_reg_time'] = data.get('gjzcrq', '')
            item['site_name'] = '标库网'
            item['company_url'] = response.url
            item['company_gather_time'] = datetime.now(
            ).strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0

            # 商标图片本地保存路径
            if item['trademark_apply_time']:
                dirname = item['trademark_apply_time'].replace('-', '')[:6]
            else:
                dirname = item['company_gather_time'].replace('-', '')[:6]
            item['trademark_image_lopath'] = dirname + '/' + data['tmImg'] + '.jpg'

            yield item
        else:
            log = "ret: %s, remainCount: %s, msg: %s." % (
                data['ret'], data['remainCount'], data['msg'])
            self.log(log)
