# -*- coding: utf-8 -*-

from tornado.httpclient import AsyncHTTPClient
from tornado import gen


# 协程版本
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)


if __name__ == '__main__':
    url = "http://httpbin.org/html"
    print(fetch_coroutine(url))
