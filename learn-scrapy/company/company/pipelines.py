# -*- coding: utf-8 -*-

import os
import cx_Oracle
import redis
from twisted.enterprise import adbapi
from company.items import (
    HaiguanItem, NaShuiItem, SecureItem, EnvironItem, TrademarkItem,
    CreditItem, StockItem)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class BasePiPeline(object):

    def __init__(self, dbargs, insert_sql):
        self.dbargs = dbargs
        self.insert_sql = insert_sql

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('cx_Oracle', **self.dbargs)

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self._do_insert, item, spider)

    def _do_insert(self, txn, item, spider):
        try:
            txn.execute(self.insert_sql, dict(item))
            spider.log("保存数据成功： %s" % item['company_name'])
        except cx_Oracle.IntegrityError:
            spider.log("该条数据已存在： %s" % item['company_name'])
        except Exception as e:
            spider.log(str(e))

    @staticmethod
    def create_insert_sql(table, *columns):
        sql = "insert into {} ".format(table) + "(" + ", ".join(columns) + \
              ") values (:" + ", :".join(columns) + ")"
        return sql


class HaiguanPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_custom_rating'
        columns = list(HaiguanItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class NaShuiPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_tax_rating'
        columns = list(NaShuiItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class SecurePipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_secure_license'
        columns = list(SecureItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class EnvironPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_environ_monitor'
        columns = list(EnvironItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class TrademarkPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_trademark'
        columns = list(TrademarkItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class CreditPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_ind_cred_record'
        columns = list(CreditItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class StockPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = 'company_stock_notice'
        columns = list(StockItem.fields.keys())
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class HaiGuanIdPipeline(object):

    def __init__(self):
        self.set_key = 'company_custom_rating_detail_id_set'
        self.list_key = 'company_custom_rating_detail_id_list'

    def open_spider(self, spider):
        self.dbpool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def close_spider(self, spider):
        self.dbpool.disconnect()

    def process_item(self, item, spider):
        r = redis.Redis(connection_pool=self.dbpool)
        Id = item['Id']
        if not r.sismember(self.set_key, Id):
            r.sadd(self.set_key, Id)
            r.lpush(self.list_key, Id)
            spider.log("成功添加： %s" % Id)
        else:
            spider.log("该数据已存在： %s" % Id)
