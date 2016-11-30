# -*- coding: utf-8 -*-

import os
import haiguan.settings as settings
from twisted.enterprise import adbapi
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class HaiguanPipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('cx_Oracle', **settings['oracle'])
        self.insert_sql = """insert into company_custom_rating (company_name,
            industry_type, business_scope, business_level,
            company_gather_time, gather_id, chanle_id) values
            (:company_name, :industry_type, :business_scope, :business_level,
            :company_gather_time, :gather_id, :chanle_id)"""

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_insert, item, spider)
        return d

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
