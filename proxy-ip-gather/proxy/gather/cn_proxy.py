# -*- coding: utf-8 -*-

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
        self.insert_sql = """insert into proxy_ip (ip, port, area, type,
            protocol) values (%s, %s, %s, '高匿', 'HTTP')"""

    def parse_list(self):
        driver = webdriver.PhantomJS()
        driver.get(self.list_url)
        trs = driver.find_elements_by_xpath("(//table)[2]/tbody/tr")
        values = self.parse_detail(trs)
        self.save(values)

    def parse_detail(self, trs):
        values = []
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            one = tuple(td.text for td in tds[:3])
            values.append(one)
        return values

    def save(self, values):
        for one in values:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(self.insert_sql, one)
                self.conn.commit()
                print("成功保存 --> %s" % one[0])
            except Exception as e:
                print("已存在 --> %s" % one[0])

    def control(self):
        self.parse_list()


if __name__ == '__main__':
    try:
        ChinaProxy().control()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
