# -*- coding: utf-8 -*-

from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', 'World')
    text = 'Hello, ' + name + '!'
    return web.Response(text=text)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/{name}', handle)
    web.run_app(app)
