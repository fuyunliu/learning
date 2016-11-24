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
sql = """insert into proxy_ip (ip, port, anonymity, type, address,
         availability) values (%s, %s, %s, %s, %s, '未知')"""
kuaidaili = ['inha', 'intr', 'outha', 'outtr']
kuaidaili_url = 'http://www.kuaidaili.com/free/{typ}/{page}/'
headers = {
    'Cookie': '_gat=1; channelid=0; sid=1479882146129815; _ga=GA1.2.19895386.1476414255',
    'Host': 'www.kuaidaili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}
proxies = {'http': 'http://58.217.195.141:80'}


class GatherKuaiDaiLi(object):

    def __init__(self):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.sql = sql
        self.session = requests.Session()
        self.session.headers.update(headers)

    def random_sleep(self):
        sleep_time = random.randint(15, 20)
        print("等待%s秒后继续..." % sleep_time)
        time.sleep(sleep_time)

    def gather_start(self):
        for i in kuaidaili:
            self.parsing_list(i)

    def parsing_list(self, typ):
        page = 322  # 共1355页
        while True:
            try:
                url = kuaidaili_url.format(typ=typ, page=page)
                referer = kuaidaili_url.format(typ=typ, page=page - 1)
                self.session.headers.update({'Referer': referer})
                r = self.session.get(url, proxies=proxies)
                self.random_sleep()
                if not r.ok:
                    break
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#list > table > tbody > tr')
                values = self.parsing_detail(trs)
                self.save_data(values)
                print("解析第%s页完成！" % page)
                page += 1
            except Exception as e:
                print(str(e))
                print("解析第%s页出错..." % page)

    def parsing_detail(self, trs):
        values = []
        for tr in trs:
            tds = tr('td')
            one = tuple(td.get_text(strip=True) for td in tds[:5])
            values.append(one)
        return values

    def save_data(self, values):
        for val in values:
            try:
                self.cursor.execute(self.sql, val)
                self.conn.commit()
                print("保存数据成功！")
            except Exception as e:
                print(str(e))
                print("保存数据出错...")

    def control(self):
        self.gather_start()


if __name__ == '__main__':
    g = GatherKuaiDaiLi()
    g.control()
