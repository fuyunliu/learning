# -*- coding: utf-8 -*-

from tornado.httpclient import HTTPClient


# 一个简单的同步函数
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body


if __name__ == '__main__':
    url = "http://httpbin.org/html"
    print(synchronous_fetch(url))
