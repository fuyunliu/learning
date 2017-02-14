# -*- coding: utf-8 -*-

import requests
import pymysql.cursors
from selenium import webdriver


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='testdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


class ChinaProxy(object):

    def __init__(self):
        self.conn = conn
        self.list_url = "http://cn-proxy.com/"
        self.test_url = "http://httpbin.org/ip"
        self.insert_sql = """insert into proxy_ip (ip, port, area, type,
            protocol) values (%s, %s, %s, '高匿', 'HTTP')"""

    def parse_list(self):
        driver = webdriver.PhantomJS()
        driver.get(self.list_url)
        trs = driver.find_elements_by_xpath("(//table)[2]/tbody/tr")
        values = self.parse_detail(trs)
        self.save_data(values)

    def parse_detail(self, trs):
        values = []
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            one = tuple(td.text for td in tds[:3])
            if self.test_ip(one):
                values.append(one)
        return values

    def save_data(self, values):
        for one in values:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(self.insert_sql, one)
                self.conn.commit()
                print("保存数据成功！")
            except Exception as e:
                print(str(e))

    def test_ip(self, one):
        ip, port = one[:2]
        proxies = {'http': 'http://{0}:{1}'.format(*one)}
        try:
            r = requests.get(self.test_url, proxies=proxies, timeout=5)
            origin_ip = r.json().get('origin')
            if origin_ip == ip:
                print("%s:%s is ok!" % (ip, port))
                return True
            else:
                print("%s:%s is not anonymous!" % (ip, port))
                return False
        except:
            print("connecting %s:%s failed!" % (ip, port))
            return False

    def control(self):
        self.parse_list()


if __name__ == '__main__':
    c = ChinaProxy()
    c.control()
