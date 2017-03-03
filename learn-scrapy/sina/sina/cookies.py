# -*- coding: utf-8 -*-
"""模拟登入新浪微博获取cookie"""

import base64
import binascii
import json
import random
import requests
import re
import rsa
from constants import agents


class SinaCookie(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {"User-Agent": random.choice(agents)}
        self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"

    def encrypt_username(self):
        "加密用户名"
        return base64.b64encode(
            self.username.encode()).decode()

    def encrypt_password(self, servertime, nonce, pubkey):
        "加密密码"
        pubkey = int(pubkey, 16)
        rsa_pubkey = rsa.PublicKey(pubkey, 65537)
        rsa_code = servertime + '\t' + nonce + '\n' + self.password
        sp = rsa.encrypt(rsa_code.encode(), rsa_pubkey)
        return binascii.b2a_hex(sp).decode()

    def get_prelogin_data(self, su):
        "获取加密密码所需的四个参数"
        url = "https://login.sina.com.cn/sso/prelogin.php"
        payload = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': su,
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.18)'
        }
        r = requests.get(url, params=payload, headers=self.headers)
        json_str = re.findall(r'(\{.*?\})', r.text)[0]
        data = json.loads(json_str)
        return tuple(str(data[k])
                     for k in ['servertime', 'nonce', 'pubkey', 'rsakv'])

    def get_cookie(self):
        su = self.encrypt_username()
        servertime, nonce, pubkey, rsakv = self.get_prelogin_data(su)
        sp = self.encrypt_password(servertime, nonce, pubkey)
        payload = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': 'http://login.sina.com.cn/sso/logout.php',
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': '0',
            'url': 'http://weibo.com/ajaxlogin.php',
            'returntype': 'META'
        }
        r = requests.post(self.login_url, data=payload,
                          headers=self.headers)
        return r.cookies.get_dict()


if __name__ == '__main__':
    my = SinaCookie('13014844547', '123456789o')
    print(my.get_cookie())
