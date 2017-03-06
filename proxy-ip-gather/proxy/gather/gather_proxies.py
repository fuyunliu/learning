# -*- coding: utf-8 -*-

import random
import requests
import time
import pymysql.cursors
from bs4 import BeautifulSoup
from constants import agents


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
        self.session.headers['user-agent'] = random.choice(agents)
        self.insert_sql = """insert into proxy_ip (ip, port, area, type,
            protocol) values (%s, %s, %s, %s, %s)"""

    def __call__(self):
        self.parse_list()

    def parse_list(self):
        raise NotImplementedError

    def parse_detail(self):
        raise NotImplementedError

    def save(self, values):
        for one in values:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(self.insert_sql, one)
                self.conn.commit()
                print("成功保存 --> %s" % one[0])
            except Exception as e:
                print("已存在 --> %s" % one[0])


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
        self.list_url = "http://www.xicidaili.com/nt/{page}"
        super().__init__()

    def parse_list(self):
        for p in range(1, 100):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#ip_list tr')
                values = self.parse_detail(trs)
                self.save(values)
                print("解析第【%s】页完成！" % p)
                time.sleep(random.randint(5, 10))
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
        super().__init__()

    def parse_list(self):
        for p in range(1, 100):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                r.encoding = 'gb2312'
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('table tbody tr')
                values = self.parse_detail(trs)
                self.save(values)
                print("解析第【%s】页完成！" % p)
                time.sleep(random.randint(5, 10))
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
        super().__init__()

    def parse_list(self):
        for p in range(1, 100):
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


if __name__ == '__main__':
    try:
        XiCi()
        # IP181()
        # MimiIp()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
