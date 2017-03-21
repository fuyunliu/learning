# -*- coding: utf-8 -*-
"""
GET http://api.tmkoo.com/app-reg.php?mobile=b4:52:7e:ca HTTP/1.1
"""
import json
import math
import re
import redis
import scrapy
from company.items import TrademarkUrlItem


redis_server = redis.Redis(host='123.196.124.161', port=6379, db=0, password='redispwd')


class TrademarkUrlSpider(scrapy.Spider):
    name = 'tianyancha_url'
    start_urls = [url.decode() for url in redis_server.lrange(
        'trademark_search_url_list', 0, 20000)]

    def parse(self, response):
        data = json.loads(response.text)
        if data['state'] == 'ok':
            count = int(data['data']['total'])
            if count != 0:
                for r in data['data']['items']:
                    item = TrademarkUrlItem()
                    regno = r['regNo']
                    intcls = re.findall(r'第(\d+)类', r['intCls'])[0]
                    item['url'] = "&regNo=%s&intCls=%s" % (regno, intcls)
                    yield item
                pn = int(data['data']['pageNum']) + 1
                if pn <= math.ceil(count / 20):
                    next_page = response.url.split(
                        '?')[0] + '?pageNum={pn}'.format(pn=pn)
                    yield scrapy.Request(next_page, callback=self.parse)
        else:
            log = "state: %s, message: %s." % (data['state'], data['message'])
            self.log(log)
