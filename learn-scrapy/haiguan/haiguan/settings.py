# -*- coding: utf-8 -*-

BOT_NAME = 'haiguan'
SPIDER_MODULES = ['haiguan.spiders']
NEWSPIDER_MODULE = 'haiguan.spiders'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
    'haiguan.middlewares.UserAgentMiddleware': 100,
    'haiguan.middlewares.ProxyMiddleware': 110,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 120
}
ITEM_PIPELINES = {
    'haiguan.pipelines.HaiguanPipeline': 300,
}
DATABASES = {
    'oracle': {
        'user': 'username',
        'password': 'password',
        'dsn': 'dsn'
    }
}

try:
    from haiguan.local_settings import *
except ImportError:
    pass
