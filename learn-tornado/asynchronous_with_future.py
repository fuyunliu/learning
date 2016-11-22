# -*- coding: utf-8 -*-


from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future


# 使用Future代替回调
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(lambda f: my_future.set_result(f.result()))
    return my_future


if __name__ == '__main__':
    url = "http://httpbin.org/html"
    future = async_fetch_future(url)
    print(future)
