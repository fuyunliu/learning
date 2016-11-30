# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HaiguanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    industry_type = scrapy.Field()
    business_scope = scrapy.Field()
    business_level = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()
