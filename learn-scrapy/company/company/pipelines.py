# -*- coding: utf-8 -*-

import os
import company.settings as settings
from twisted.enterprise import adbapi
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class BasePiPeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('cx_Oracle', **settings.DATABASES['oracle'])

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_insert, item, spider)
        return d

    def _do_insert(self, txn, item, spider):
        pass


class HaiguanPipeline(BasePiPeline):

    def __init__(self):
        self.insert_sql = """insert into company_custom_rating (company_name,
            industry_type, business_scope, business_level,
            company_gather_time, gather_id, chanle_id) values
            (:company_name, :industry_type, :business_scope, :business_level,
            :company_gather_time, :gather_id, :chanle_id)"""
        super().__init__()

    def _do_insert(self, txn, item, spider):
        values = {
            'company_name': item['company_name'],
            'industry_type': item['industry_type'],
            'business_scope': item['business_scope'],
            'business_level': item['business_level'],
            'company_gather_time': item['company_gather_time'],
            'gather_id': item['gather_id'],
            'chanle_id': item['chanle_id']
        }
        txn.execute(self.insert_sql, values)
        spider.log("保存数据成功： %s" % item['company_name'])


class NaShuiPipeline(BasePiPeline):

    def __init__(self):
        self.insert_sql = """insert into company_tax_rating (company_name,
            taxpayer_code, evaluate_year, grant_enterprise, tax_level,
            company_gather_time, gather_id, chanle_id) values
            (:company_name, :taxpayer_code, :evaluate_year, :grant_enterprise,
            :tax_level, :company_gather_time, :gather_id, :chanle_id)"""
        super().__init__()

    def _do_insert(self, txn, item, spider):
        values = {
            'company_name': item['company_name'],
            'taxpayer_code': item['taxpayer_code'],
            'evaluate_year': item['evaluate_year'],
            'grant_enterprise': item['grant_enterprise'],
            'tax_level': item['tax_level'],
            'company_gather_time': item['company_gather_time'],
            'gather_id': item['gather_id'],
            'chanle_id': item['chanle_id']
        }
        txn.execute(self.insert_sql, values)
        spider.log("保存数据成功： %s" % item['company_name'])


class SecurePipeline(BasePiPeline):

    def __init__(self):
        self.insert_sql = """insert into company_secure_license (company_name,
            secure_code, secure_area, company_legal_name, secure_industry,
            company_class_name, secure_pro_ability, secure_level,
            secure_issue_time,
            company_gather_time, gather_id, chanle_id) values
            (:company_name, :secure_code, :secure_area, :company_legal_name,
            :secure_industry, :company_class_name, :secure_pro_ability,
            :secure_level, :secure_issue_time, :company_gather_time,
            :gather_id, :chanle_id)"""
        super().__init__()

    def _do_insert(self, txn, item, spider):
        values = {
            'company_name': item['company_name'],
            'secure_code': item['secure_code'],
            'secure_area': item['secure_area'],
            'company_legal_name': item['company_legal_name'],
            'secure_industry': item['secure_industry'],
            'company_class_name': item['company_class_name'],
            'secure_pro_ability': item['secure_pro_ability'],
            'secure_level': item['secure_level'],
            'secure_issue_time': item['secure_issue_time'],
            'company_gather_time': item['company_gather_time'],
            'gather_id': item['gather_id'],
            'chanle_id': item['chanle_id']
        }
        txn.execute(self.insert_sql, values)
        spider.log("保存数据成功： %s" % item['company_name'])
