# -*- coding: utf-8 -*-

BOT_NAME = 'company'
SPIDER_MODULES = ['company.spiders']
NEWSPIDER_MODULE = 'company.spiders'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 501, 502, 503, 504, 400, 403, 404, 408]
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
    'company.middlewares.UserAgentMiddleware': 100,
    'company.middlewares.ProxyMiddleware': 110,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 120
}
ITEM_PIPELINES = {
    #'company.pipelines.HaiguanPipeline': 300,
    #'company.pipelines.NaShuiPipeline': 300,
    'company.pipelines.SecurePipeline': 300
}
DATABASES = {
    'oracle': {
        'user': 'username',
        'password': 'password',
        'dsn': 'dsn'
    }
}

try:
    from company.local_settings import *
except ImportError:
    pass
