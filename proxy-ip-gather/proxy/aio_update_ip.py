# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import async_timeout
import aiomysql


async def execute(sql):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            return await cur.fetchall()


async def fetch(url, **kwargs):
    with async_timeout.timeout(5):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **kwargs) as response:
                return await response.text()


async def sem_fetch(sem, url, **kwargs):
    async with sem:
        try:
            return await fetch(url, **kwargs)
        except asyncio.TimeoutError:
            pass


async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='root',
                                      db='testdb',
                                      loop=asyncio.get_event_loop())

    sem = asyncio.Semaphore(5)
    sql = "select ip, port from proxy_ip"
    url = "http://httpbin.org/ip"
    tasks = []
    for ip, port in await execute(pool, sql):
        proxy = 'http://' + ip + ':' + port
        task = asyncio.ensure_future(sem_fetch(sem, url))
        tasks.append(task)
        responses = asyncio.gather(*tasks)
　



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
