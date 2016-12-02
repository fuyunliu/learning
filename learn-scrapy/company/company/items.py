# -*- coding: utf-8 -*-

import scrapy


class HaiguanItem(scrapy.Item):

    company_name = scrapy.Field()
    industry_type = scrapy.Field()
    business_scope = scrapy.Field()
    business_level = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()


class NaShuiItem(scrapy.Item):

    company_name = scrapy.Field()
    taxpayer_code = scrapy.Field()
    evaluate_year = scrapy.Field()
    grant_enterprise = scrapy.Field()
    tax_level = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()


class SecureItem(scrapy.Item):

    company_name = scrapy.Field()
    secure_code = scrapy.Field()
    secure_area = scrapy.Field()
    company_legal_name = scrapy.Field()
    secure_industry = scrapy.Field()
    company_class_name = scrapy.Field()
    secure_pro_ability = scrapy.Field()
    secure_level = scrapy.Field()
    secure_issue_time = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()
