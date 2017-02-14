# -*- coding: utf-8 -*-
"""
GET http://api.tmkoo.com/app-reg.php?mobile=b4:52:7e:ca
"""

import pymysql.cursors
import random
import requests
import string
from constants import agents, proxy


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='testdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_random_mobile():
    return ':'.join(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(2)) for _ in range(4))


def create_api(mobile):
    url = 'http://api.tmkoo.com/app-reg.php'
    payload = {'mobile': mobile}
    headers = {'user-agent': random.choice(agents)}
    proxies = {'http': random.choice(proxy)}
    try:
        r = requests.get(url, headers=headers,
                         proxies=proxies, params=payload)
        data = r.json()
        if data['ret'] == '0':
            api = {'key': data['apiKey'], 'password': data['apiPassword']}
            return api
        else:
            print("ret: %s, msg: %s" % (data['ret'], data['msg']))
    except Exception as e:
        print("连接失败！代理：%s" % proxies['http'])


def save_api(api):
    if isinstance(api, dict):
        key, password = api['key'], api['password']
        with connection.cursor() as cursor:
            sql = "INSERT INTO `tmkoo` (`key`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, (key, password))
            print("成功添加！key: %s, password: %s" % (key, password))
        connection.commit()


def main():
    n = 1
    while n <= 100:
        mobile = get_random_mobile()
        api = create_api(mobile)
        save_api(api)
        n += 1


if __name__ == '__main__':
    main()
    connection.close()
