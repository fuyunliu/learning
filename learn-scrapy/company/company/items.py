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


class EnvironItem(scrapy.Item):

    company_name = scrapy.Field()
    monitor_area_code = scrapy.Field()
    monitor_legal_name_code = scrapy.Field()
    monitor_class = scrapy.Field()
    monitor_province = scrapy.Field()
    monitor_year = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()


class GmpgspItem(scrapy.Item):

    company_name = scrapy.Field()
    gmp_gsp_province = scrapy.Field()
    gmp_gsp_code = scrapy.Field()
    gmp_gsp_address = scrapy.Field()
    gmp_gsp_scope = scrapy.Field()
    gmp_gsp_issue_time = scrapy.Field()
    gmp_gsp_validity_time = scrapy.Field()
    gmp_gsp_continue_time = scrapy.Field()
    gmp_gsp_continue_to = scrapy.Field()
    gmp_gsp_continue_scope = scrapy.Field()
    gmp_gsp_version_gmp = scrapy.Field()
    gmp_gsp_remarks = scrapy.Field()
    company_url = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()
