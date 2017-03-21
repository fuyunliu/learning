# -*- coding: utf-8 -*-

import json
import random
import string
import scrapy
from company.items import TmkooApiItem


url = 'http://api.tmkoo.com/app-reg.php?mobile={mobile}'


def get_random_mobile(count):
    mobiles = set()
    for _ in range(count):
        m = ':'.join(''.join(random.choice(string.ascii_lowercase +
                                           string.digits) for _ in range(2)) for _ in range(4))
        mobiles.add(m)
    return mobiles


class TmkooSpider(scrapy.Spider):
    name = 'tmkoo'
    start_urls = [url.format(mobile=m) for m in get_random_mobile(2000)]

    def parse(self, response):
        data = json.loads(response.text)
        if data['ret'] == '0':
            item = TmkooApiItem()
            key = data['apiKey']
            password = data['apiPassword']
            api = "&apiKey={key}&apiPassword={password}" % (key, password)
            item['api'] = api
            yield item
