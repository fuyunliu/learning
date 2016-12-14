# -*- coding: utf-8 -*-

from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    text = "Hello, %s!" % request.args.get('name', 'World')
    return Response(text)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)
