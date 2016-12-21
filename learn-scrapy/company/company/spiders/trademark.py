# -*- coding: utf-8 -*-

import math
import json
import urllib.parse as urlparse
import scrapy
from datetime import datetime
from ._companies import companies
from company.items import TrademarkItem


search_url = "http://api.tmkoo.com/app-search.php?keyword={key}&apiKey=TEST001&apiPassword=TEST_P_001&pageSize=50&condition=1&intCls=0"
detail_url = "http://api.tmkoo.com/app-info.php?apiKey=4399320012393234&apiPassword=331nd3342d&regNo={regno}&intCls={intcls}"
scroll_url = "http://api.tmkoo.com/app-search-scroll.php?logId={logid}&pageSize=50&pageNo={pn}"


class TrademarkSpider(scrapy.Spider):
    name = 'trademark'
    start_urls = [search_url.format(key=key) for key in companies]

    def parse(self, response):
        data = json.loads(response.text)
        if data['ret'] == '0':
            count = int(data['allRecords'])
            if count != 0:
                for r in data['results']:
                    regno = r['regNo']
                    intcls = r['intCls']
                    detail = detail_url.format(regno=regno, intcls=intcls)
                    yield scrapy.Request(detail, callback=self.parse_detail)
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

    def parse_detail(self, response):
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
                s = f['flowDate'] + f['flowName']
                status.append(s)
            item['trademark_status'] = ''.join(status)
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
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
        else:
            log = "ret: %s, remainCount: %s, msg: %s." % (
                data['ret'], data['remainCount'], data['msg'])
            self.log(log)
