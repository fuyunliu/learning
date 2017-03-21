# -*- coding: utf-8 -*-

import scrapy


class HaiGuanIdItem(scrapy.Item):
    Id = scrapy.Field()


class TrademarkUrlItem(scrapy.Item):
    url = scrapy.Field()


class GmpGspUrlItem(scrapy.Item):
    url = scrapy.Field()


class TmkooApiItem(scrapy.Item):
    api = scrapy.Field()


class HaiguanItem(scrapy.Item):

    company_name = scrapy.Field()
    industry_type = scrapy.Field()
    business_scope = scrapy.Field()
    business_level = scrapy.Field()
    company_url = scrapy.Field()
    site_name = scrapy.Field()
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
    site_name = scrapy.Field()
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
    site_name = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()


class TrademarkItem(scrapy.Item):

    company_name = scrapy.Field()
    trademark_class_code = scrapy.Field()
    trademark_name = scrapy.Field()
    trademark_appli_code = scrapy.Field()
    trademark_apply_time = scrapy.Field()
    trademark_status = scrapy.Field()
    trademark_produce_name = scrapy.Field()
    trademark_apply_name = scrapy.Field()
    trademark_regist_time = scrapy.Field()
    trademark_regist_no = scrapy.Field()
    trademark_preli_no = scrapy.Field()
    trademark_preli_time = scrapy.Field()
    trademark_specif_color = scrapy.Field()
    trademark_priority_date = scrapy.Field()
    trademark_type = scrapy.Field()
    trademark_valid_time = scrapy.Field()
    trademark_agent_name = scrapy.Field()
    trademark_image_lopath = scrapy.Field()
    trademark_image_weburl = scrapy.Field()
    trademark_reg_time = scrapy.Field()
    site_name = scrapy.Field()
    company_url = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()


class CreditItem(scrapy.Item):

    company_name = scrapy.Field()
    credit_rating = scrapy.Field()
    credit_certifi_code = scrapy.Field()
    credit_certifi_time = scrapy.Field()
    credit_validit_period = scrapy.Field()
    credit_certifi_unit = scrapy.Field()
    company_org_code = scrapy.Field()
    company_regis_code = scrapy.Field()
    credit_url = scrapy.Field()
    site_name = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()


class StockItem(scrapy.Item):

    company_name = scrapy.Field()
    notice_id = scrapy.Field()
    notice_shares_code = scrapy.Field()
    notice_title = scrapy.Field()
    notice_type = scrapy.Field()
    notice_publishtime = scrapy.Field()
    notice_url = scrapy.Field()
    notice_file_url = scrapy.Field()
    notice_industry = scrapy.Field()
    notice_plate = scrapy.Field()
    site_name = scrapy.Field()
    company_gather_time = scrapy.Field()
    gather_id = scrapy.Field()
    chanle_id = scrapy.Field()
