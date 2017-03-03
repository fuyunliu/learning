# -*- coding: utf-8 -*-
import random
from company.constants import agents, proxies, cookies


class UserAgentMiddleware:

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookieMiddleware:

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.headers["Cookie"] = cookie


class ProxyMiddleware:

    def process_request(self, request, spider):
        proxy = random.choice(proxies)
        request.meta['proxy'] = proxy
