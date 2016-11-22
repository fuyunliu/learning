# -*- coding: utf-8 -*-

from tornado.httpclient import AsyncHTTPClient


# 将synchronous_fetch用回调参数改写成异步函数
def asynchronous_fetch(url, callback=None):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)


if __name__ == '__main__':
    url = "http://httpbin.org/html"
    asynchronous_fetch(url)
