# -*- coding: utf-8 -*-

import random
import requests
import pymysql.cursors
import time
from bs4 import BeautifulSoup


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='test',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
sql = """insert into proxy_ip (ip, port, area, type, protocol)
         values (%s, %s, %s, %s, %s)"""
list_url = 'http://www.xicidaili.com/nn/{page}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}


class GatherXiCi(object):
    """爬取西刺国内高匿代理"""

    def __init__(self):
        self.conn = conn
        self.sql = sql

    def parsing_list(self):
        page = 1
        while True:
            try:
                url = list_url.format(page=page)
                r = requests.get(url, headers=headers)
                time.sleep(random.randint(10, 15))
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#ip_list tr')
                values = self.parsing_detail(trs)
                self.save_data(values)
                print("解析第【%s】页完成！" % page)
                page += 1
            except Exception as e:
                print(str(e))
                print("解析第【%s】页出错..." % page)

    def parsing_detail(self, trs):
        values = []
        del trs[0]
        for tr in trs:
            tds = tr('td')
            one = tuple(td.get_text(strip=True) for td in tds[1:6])
            values.append(one)
        return values

    def save_data(self, values):
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(self.sql, values)
            self.conn.commit()
            print("保存数据成功！")
        except Exception as e:
            print(str(e))
            print("保存数据出错...")

    def control(self):
        self.parsing_list()


if __name__ == '__main__':
    p = GatherXiCi()
    p.control()
