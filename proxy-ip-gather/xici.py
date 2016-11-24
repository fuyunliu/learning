# -*- coding: utf-8 -*-

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
sql = """insert into proxy_ip (ip, port, type, anonymity, address,
         availability) values (%s, %s, %s, %s, %s, '未知')"""
xici = ['nn', 'nt', 'wn', 'wt', 'qq']
xici_url = 'http://www.xicidaili.com/{typ}/{page}'
kuaidaili = ['inha', 'intr', 'outha', 'outtr']
kuaidaili_url = 'http://www.kuaidaili.com/free/intr/4/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}
proxies = {'http': 'http://46.101.3.126:8118'}


class GatherXiCi(object):

    def __init__(self):
        self.conn = conn
        self.sql = sql

    def gather_start(self):
        for i in xici:
            self.parsing_list(i)

    def parsing_list(self, typ):
        page = 261
        while True:
            try:
                url = url_format.format(typ=typ, page=page)
                r = requests.get(url, headers=headers, proxies=proxies)
                time.sleep(10)
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#ip_list tr')
                if len(trs) <= 1:
                    break
                values = self.parsing_detail(trs)
                self.save_data(values)
                print("解析第%s页完成！" % page)
                page += 1
            except Exception as e:
                print(str(e))
                print("解析第%s页出错..." % page)

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
        self.gather_start()


if __name__ == '__main__':
    p = ProxyIP()
    p.control()
