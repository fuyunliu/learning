# -*- coding: utf-8 -*-
import logging
import random
from company.constants import agents, proxies, cookies

logger = logging.getLogger(__name__)


class UserAgentMiddleware(object):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookieMiddleware(object):

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.headers["Cookie"] = cookie


class RefererMiddleware(object):

    def process_request(self, request, spider):
        request.headers["Referer"] = 'http://www.cninfo.com.cn/cninfo-new/announcement/show'


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = random.choice(proxies)
        request.meta['proxy'] = proxy


class RetryMiddleware(object):

    def __init__(self, settings):
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if not response.text:
            reason = 'empty response'
            return self._retry(request, reason, spider) or response
        return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
