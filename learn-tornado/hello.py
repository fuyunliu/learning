# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web


# 一个简单地helloworld应用
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("hello, world!")


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
