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


class CleanProxy(object):

    def __init__(self):
        self.conn = conn
        self.test_url = "http://httpbin.org/ip"
        self.fetch_sql = "select id, ip, port from proxy_ip"
        self.delete_sql = "delete from proxy_ip where id = {id}"

    def fetch_all(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.fetch_sql)
            rows = cursor.fetchall()
        return rows

    def delete(self, id):
        sql = self.delete_sql.format(id=id)
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
                    self.delete(id)
                    print("%s:%s is not anonymous, delete done!" % (ip, port))
                else:
                    print("%s:%s is ok!" % (ip, port))
            except Exception as e:
                self.delete(id)
                print("connecting %s:%s failed, delete done!" % (ip, port))

    def control(self):
        rows = self.fetch_all()
        self.clean(rows)


if __name__ == '__main__':
    # c = CleanProxy()
    # c.control()

    import pprint
    c = CleanProxy()
    rows = c.fetch_all()
    proxies = []
    for row in rows:
        proxy = "http://%s:%s" % (row['ip'], row['port'])
        proxies.append(proxy)
    pprint.pprint(proxies)
