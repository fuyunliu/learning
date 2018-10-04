# -*- coding: utf-8 -*-

import random
import requests
import time
import warnings
import pymysql.cursors
from bs4 import BeautifulSoup
from useragent import browsers


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='testdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


class Base:

    def __init__(self):
        self.conn = conn
        self.session = requests.Session()
        self.session.headers['User-Agent'] = random.choice(browsers)

    def parse_list(self):
        raise NotImplementedError

    def parse_detail(self):
        raise NotImplementedError

    def save(self, values):
        for one in values:
            try:
                with self.conn.cursor() as cursor:
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore")
                        cursor.execute(self.insert_sql, one)
                print("成功保存 --> %s" % one[0])
            except Exception as e:
                print("已存在 --> %s" % one[0])
        self.conn.commit()

    def control(self):
        self.parse_list()


class XiCi(Base):
    """
    国内高匿
    http://www.xicidaili.com/nn/
    国内透明
    http://www.xicidaili.com/nt/
    HTTPS代理
    http://www.xicidaili.com/wn/
    HTTP代理
    http://www.xicidaili.com/wt/
    SOCKS代理
    http://www.xicidaili.com/qq/
    """

    def __init__(self):
        self.list_url = "http://www.xicidaili.com/nn/{page}"
        self.insert_sql = """insert ignore into proxy_ip (ip, port, area, type,
            protocol) values (%s, %s, %s, %s, %s)"""
        super().__init__()

    def parse_list(self):
        for p in range(2, 300):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#ip_list tr')
                values = self.parse_detail(trs)
                self.save(values)
                print("解析第【%s】页完成！" % p)
                time.sleep(random.randint(45, 60))
            except Exception as e:
                print(e)
                print("解析第【%s】页出错..." % p)

    def parse_detail(self, trs):
        values = []
        del trs[0]
        for tr in trs:
            tds = tr('td')
            one = tuple(td.get_text(strip=True) for td in tds[1:6])
            values.append(one)
        return values


class IP181(Base):

    def __init__(self):
        self.list_url = "http://www.ip181.com/daili/{page}.html"
        self.insert_sql = """insert ignore into proxy_ip (ip, port, type,
            protocol, area) values (%s, %s, %s, %s, %s)"""
        super().__init__()

    def parse_list(self):
        for p in range(400, 400):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                r.encoding = 'gb2312'
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('table tbody tr')
                values = self.parse_detail(trs)
                self.save(values)
                print("解析第【%s】页完成！" % p)
                time.sleep(random.randint(10, 15))
            except Exception as e:
                print(e)
                print("解析第【%s】页出错..." % p)

    def parse_detail(self, trs):
        values = []
        del trs[0]
        for tr in trs:
            tds = tr('td')
            del tds[4]
            one = tuple(td.get_text(strip=True) for td in tds[:5])
            values.append(one)
        return values


class MimiIp(Base):

    def __init__(self):
        self.list_url = "http://www.mimiip.com/gngao/{page}"
        self.insert_sql = """insert ignore into proxy_ip (ip, port, area, type,
            protocol) values (%s, %s, %s, %s, %s)"""
        super().__init__()

    def parse_list(self):
        for p in range(50, 50):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('table.list tr')
                values = self.parse_detail(trs)
                self.save(values)
                print("解析第【%s】页完成！" % p)
                time.sleep(random.randint(10, 15))
            except Exception as e:
                print(e)
                print("解析第【%s】页出错..." % p)

    def parse_detail(self, trs):
        values = []
        del trs[0]
        for tr in trs:
            tds = tr('td')
            one = tuple(td.get_text(strip=True) for td in tds[:5])
            values.append(one)
        return values


class KuaiDaiLi(Base):
    """
    国内高匿代理
    http://www.kuaidaili.com/free/inha/
    国内普通代理
    http://www.kuaidaili.com/free/intr/
    国外高匿代理
    http://www.kuaidaili.com/free/outha/
    国外普通代理
    http://www.kuaidaili.com/free/outtr/
    """

    def __init__(self):
        self.list_url = "http://www.kuaidaili.com/free/inha/{page}/"
        self.insert_sql = """insert ignore into proxy_ip (ip, port, type,
            protocol, area) values (%s, %s, %s, %s, %s)"""
        super().__init__()

    def parse_list(self):
        for p in range(1300, 1500):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#list table tr')
                values = self.parse_detail(trs)
                self.save(values)
                print("解析第【%s】页完成！" % p)
                time.sleep(random.randint(10, 15))
            except Exception as e:
                print(e)
                print("解析第【%s】页出错..." % p)

    def parse_detail(self, trs):
        values = []
        del trs[0]
        for tr in trs:
            tds = tr('td')
            one = tuple(td.get_text(strip=True) for td in tds[:5])
            values.append(one)
        return values


if __name__ == '__main__':
    try:
        XiCi().control()
        # IP181().control()
        # MimiIp().control()
        # KuaiDaiLi().control()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
