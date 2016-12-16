# -*- coding: utf-8 -*-
"在tornado中使用jinja2"

import os
import threading
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.template
import tornado.web
from jinja2 import Environment, FileSystemLoader

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Template(object):

    def __init__(self, template_instance):
        self.template_instance = template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)


class JinjaLoader(tornado.template.BaseLoader):

    def __init__(self, root_directory, **kwargs):
        self.jinja_env = Environment(loader=FileSystemLoader(root_directory),
                                     **kwargs)
        self.templates = {}
        self.lock = threading.RLock()

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        template_instance = Template(self.jinja_env.get_template(name))
        return template_instance


class IndexHanlder(tornado.web.RequestHandler):

    def get(self):
        name = self.get_argument('name', 'World')
        self.render('index.html', name=name)


def make_app():
    return tornado.web.Application(
        handlers=[
            (r'/', IndexHanlder)
        ],
        template_loader=JinjaLoader(os.path.join(
            os.path.dirname(__file__), 'templates'))
    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
