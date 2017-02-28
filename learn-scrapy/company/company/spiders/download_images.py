# -*- coding: utf-8 -*-

import re
import scrapy
import redis


redis_server = redis.Redis(host='localhost', port=6379, db=0)


class ImageSpider(scrapy.Spider):

    name = 'image'

    def start_requests(self):
        url_f = "http://pic.tmkoo.com/pic.php?zch={img}"
        regex = r"\d+/(\w+).jpg"
        local_paths = redis_server.lrange(
            'company_trademark_image_lopath', 0, 27000)
        for p in local_paths:
            p = p.decode()
            img = re.findall(regex, p)[0]
            url = url_f.format(img=img)
            meta = {"local_path": p}
            yield scrapy.Request(url, callback=self.parse, meta=meta)

    def parse(self, response):
        local_path = response.meta['local_path']
        img = 'Y:/Handled_File/trademark/' + local_path
        with open(img, 'wb') as f:
            f.write(response.body)
        message = "下载图片成功！==>%s" % img
        self.log(message)
