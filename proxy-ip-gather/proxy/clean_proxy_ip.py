# -*- coding: utf-8 -*-
"""
清理数据库的代理ip，测试网站 http://httpbin.org/ip
"""

import pymysql.cursors
import requests


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='testdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


class CleanProxy:

    def __init__(self):
        self.conn = conn
        self.test_url = "http://httpbin.org/ip"
        self.fetch_sql = "select id, ip, port from proxy_ip where id >= 34715 and id <=164211"
        self.update_sql = "update proxy_ip set usability = {u} where id = {id}"

    def fetch_all(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.fetch_sql)
            rows = cursor.fetchall()
        return rows

    def update(self, id, u):
        sql = self.update_sql.format(id=id, u=u)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def clean(self, rows):
        for row in rows:
            id, ip, port = row['id'], row['ip'], row['port']
            proxies = {'http': 'http://{ip}:{port}'.format(ip=ip, port=port)}
            try:
                r = requests.get(self.test_url, proxies=proxies, timeout=5)
                origin_ip = r.json().get('origin')
                if origin_ip != ip:
                    self.update(id, 0)
                    print("%s:%s is not anonymous!" % (ip, port))
                else:
                    self.update(id, 1)
                    print("%s:%s is ok!" % (ip, port))
            except Exception as e:
                self.update(id, 0)
                print("connecting %s:%s failed!" % (ip, port))

    def control(self):
        rows = self.fetch_all()
        self.clean(rows)


if __name__ == '__main__':
    c = CleanProxy()
    c.control()
