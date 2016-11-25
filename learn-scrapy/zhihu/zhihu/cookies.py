# -*- coding: utf-8 -*-
"""模拟登入知乎获取cookie"""

import os
import random
import requests
import time
from bs4 import BeautifulSoup
from PIL import Image
from agents import user_agents


class ZhihuCookie(object):

    def __init__(self, email=None, phone=None, password=None):
        self.email = email
        self.phone = phone
        self.password = password
        self.session = requests.Session()
        self.session.headers['user-agent'] = random.choice(user_agents)
        self.index_url = "https://www.zhihu.com/"
        self.email_url = "https://www.zhihu.com/login/email"
        self.phone_url = "https://www.zhihu.com/login/phone_num"
        self.captcha_url = "https://www.zhihu.com/captcha.gif"
        self.image_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'images'))

    def get_captcha(self):
        params = {
            'r': str(int(time.time() * 1000)),
            'type': 'login'
        }
        r = self.session.get(self.captcha_url, params=params)
        img = os.path.join(self.image_path, 'captcha.gif')
        with open(img, 'wb') as f:
            f.write(r.content)
        return img

    def get__xsrf(self):
        r = self.session.get(self.index_url)
        soup = BeautifulSoup(r.text, 'lxml')
        _xsrf = soup.select_one("input[name='_xsrf']")['value']
        return _xsrf

    def get_cookie(self):
        _xsrf = self.get__xsrf()
        img = Image.open(self.get_captcha())
        img.show()
        captcha = input("请输入验证码：")
        payload = {
            '_xsrf': _xsrf,
            'password': self.password,
            'captcha': captcha
        }
        if self.email is not None:
            payload['email'] = self.email
            login_url = self.email_url
        else:
            payload['phone_num'] = self.phone
            login_url = self.phone_url
        r = self.session.post(login_url, data=payload)
        data = r.json()
        print(data)
        if data['r'] == 0:
            return r.cookies.get_dict()
        else:
            print(data['msg'])


if __name__ == '__main__':
    my = ZhihuCookie(phone='13014844547', password='123456')
    print(my.email, my.phone, my.password)
    print(my.get_cookie())
