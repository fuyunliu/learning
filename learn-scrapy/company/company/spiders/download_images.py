# -*- coding: utf-8 -*-

import scrapy
from company.constants import trademark_image_weburl


class ImageSpider(scrapy.Spider):

    name = 'image'
    start_urls = trademark_image_weburl

    def parse(self, response):
        name = response.url.split('/')[-1]
        img = 'E:/trademark/%s' % name
        with open(img, 'wb') as f:
            f.write(response.body)
