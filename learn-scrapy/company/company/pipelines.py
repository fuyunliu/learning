# -*- coding: utf-8 -*-

import os
import cx_Oracle
from twisted.enterprise import adbapi
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
        table = crawler.settings.get('HAIGUAN_TABLE')
        columns = crawler.settings.get('HAIGUAN_COLUMNS')
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class NaShuiPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = crawler.settings.get('NASHUI_TABLE')
        columns = crawler.settings.get('NASHUI_COLUMNS')
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class SecurePipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = crawler.settings.get('SECURE_TABLE')
        columns = crawler.settings.get('SECURE_COLUMNS')
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))


class EnvironPipeline(BasePiPeline):

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = crawler.settings.get('DATABASES').get('oracle')
        table = crawler.settings.get('ENVIRON_TABLE')
        columns = crawler.settings.get('ENVIRON_COLUMNS')
        return cls(dbargs=dbargs,
                   insert_sql=cls.create_insert_sql(table, *columns))
