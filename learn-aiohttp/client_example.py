# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import async_timeout
import aiomysql


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def update():
    conn = await aiomysql.connect(host='localhost', port=3306,
                                  user='root', password='root',
                                  db='testdb', loop=loop)

    cur = yield from conn.cursor()
    yield from cur.execute("SELECT Host,User FROM user")
    print(cur.description)
    r = yield from cur.fetchall()
    print(r)
    yield from cur.close()
    conn.close()


async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'http://httpbin.org/ip')
        print(html)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
