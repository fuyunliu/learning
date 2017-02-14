# -*- coding: utf-8 -*-

import scrapy
import redis


def get_image_url(start=0, stop=-1):
    r = redis.Redis(host='123.196.124.161', port=6379, db=0, password='redispwd')
    return r.lrange('company_trademark_image_weburl', start, stop)


class ImageSpider(scrapy.Spider):

    name = 'image'
    start_urls = [url.decode() for url in get_image_url(16001, 32000)]

    def parse(self, response):
        name = response.url.split('=')[-1]
        img = 'D:/gather_node_liufuyun/trademark/images/%s.jpg' % name
        with open(img, 'wb') as f:
            f.write(response.body)
