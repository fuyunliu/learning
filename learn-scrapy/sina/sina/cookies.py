# -*- coding: utf-8 -*-
"""模拟登入新浪微博获取cookie"""

import base64
import binascii
import json
import requests
import re
import rsa
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}


class SinaCookie(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"

    def encrypt_username(self):
        "加密用户名"
        return base64.b64encode(
            self.username.encode('utf-8')).decode('utf-8')

    def encrypt_password(self, servertime, nonce, pubkey):
        "加密密码"
        pubkey = int(pubkey, 16)
        rsa_pubkey = rsa.PublicKey(pubkey, 65537)
        rsa_code = str(servertime) + '\t' + nonce + '\n' + self.password
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
        r = requests.get(url, params=payload, headers=headers)
        json_str = re.findall(r'(\{.*?\})', r.text)[0]
        data = json.loads(json_str)
        return data['servertime'], data['nonce'], data['pubkey'], data['rsakv']

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
        r = requests.post(self.login_url, data=payload, headers=headers)
        return r.cookies.get_dict()


if __name__ == '__main__':
    # my = SinaCookie('13014844547', '123456789o')
    # print(my.get_cookie())
    url = "http://weibo.com/p/1005056069383293/info?mod=pedit"
    cookies = {'tgc': 'TGT-NjA2OTM4MzI5Mw==-1479980152-xd-CB6C15E010DE6F03A16C472E656B3E56', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFk.PjmjbWw4meVqjXC5OG05NHD95Qcehq4e0n0eo.0Ws4DqcjZUcH0UGUaMJp.e5tt', 'LT': '1479980152', 'SUB': '_2A251MsQoDeTxGeBO7VsS-C3Owj-IHXVWSbLgrDV_PUNbm9AKLUikkW9gwuma-YP_FbGtr8xknBhy8PX1dQ..', 'ALF': '1511516152', 'sso_info': 'v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLmOk5S5joOMtY2TnLGJp5WpmYO0toyDmLmMs6CzjKOksw==', 'SCF': 'AkI_4dCQmZ5czzShpSyGRX9HOCefvAH7r8kJ6me7cLt_1uivTDaplGxkS-jDvWp7mHC6Ksw29kHhvWvegw5sFis.', 'ALC': 'ac%3D0%26bt%3D1479980152%26cv%3D5.0%26et%3D1511516152%26scf%3D%26uid%3D6069383293%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D7ea4dd85bec43308bc52244dc3afd013'}
    r = requests.get(url, headers=headers, cookies=cookies)
    print(r.content.decode('utf-8'))

