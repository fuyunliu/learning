# -*- coding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index1.html')


class PoemHandler(tornado.web.RequestHandler):

    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        noun3 = self.get_argument('noun3')
        verb = self.get_argument('verb')
        self.render('poem.html', roads=noun1, wood=noun2,
                    made=verb, difference=noun3)


def make_app():
    return tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', PoemHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
