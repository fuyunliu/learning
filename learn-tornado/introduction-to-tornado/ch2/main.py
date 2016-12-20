# -*- coding: utf-8 -*-

import os
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index2.html')


class MungedHanlder(tornado.web.RequestHandler):

    def map_by_first_letter(self, text):
        mapped = {}
        for l in text.split('\r\n'):
            for w in [x for x in l.split(' ') if len(x) > 0]:
                if w[0] not in mapped:
                    mapped[w[0]] = []
                mapped[w[0]].append(w)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map,
                    change_lines=change_lines, choice=random.choice)


def make_app():
    return tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', MungedHanlder)
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True
    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
