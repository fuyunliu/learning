# -*- coding: utf-8 -*-

BOT_NAME = 'company'
SPIDER_MODULES = ['company.spiders']
NEWSPIDER_MODULE = 'company.spiders'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 5
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 501, 502, 503, 504, 400, 403, 404, 408]
# LOG_FILE = 'spider.log'
# LOG_LEVEL = 'INFO'
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
    "company.middlewares.UserAgentMiddleware": 100,
    # "company.middlewares.CookieMiddleware": 130,
    # 'company.middlewares.ProxyMiddleware': 110,
    # "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 120
}
ITEM_PIPELINES = {
    # 'company.pipelines.HaiguanPipeline': 300,
    # 'company.pipelines.NaShuiPipeline': 300,
    # 'company.pipelines.SecurePipeline': 300,
    # 'company.pipelines.EnvironPipeline': 300,
    # 'company.pipelines.HaiGuanIdPipeline': 300,
    # 'company.pipelines.TrademarkPipeline': 300,
    # 'company.pipelines.StockPipeline': 300,
    # 'company.pipelines.TrademarkUrlPipeline': 300,
    # 'company.pipelines.CreditPipeline': 300,
    'company.pipelines.GmpGspUrlPipeline': 300,
}
DATABASES = {
    'oracle': {
        'user': 'username',
        'password': 'password',
        'dsn': 'dsn',
        'threaded': True
    }
}

try:
    from company.local_settings import *
except ImportError:
    pass
