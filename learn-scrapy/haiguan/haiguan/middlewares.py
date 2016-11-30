# -*- coding: utf-8 -*-

import random
from haiguan.headers import agents, proxies


class UserAgentMiddleware(object):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = random.choice(proxies)
        request.meta['proxy'] = proxy
