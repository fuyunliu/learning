# -*- coding: utf-8 -*-

import re
from datetime import datetime

import redis
import scrapy
from bs4 import BeautifulSoup

from company.items import HaiGuanIdItem, HaiguanItem


class HaiGuanIdSpider(scrapy.Spider):

    name = 'haiguanid'
    start_urls = [
        "http://www.haiguan.info/OnLineSearch/IndustryInfo/Default.aspx"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        [s.extract() for s in soup('script')]
        links = soup.select(".qy_nr h2 a")
        for l in links:
            item = HaiGuanIdItem()
            item['Id'] = re.findall(r"\/infos(\w+)\.aspx", l['href'])[0]
            yield item
        viewstate = soup.find(id='__VIEWSTATE')['value']
        pagenum = soup.find(id='ctl00$MainContent$AspNetPager1_input')['value']
        payload = {
            '__EVENTTARGET': 'ctl00$MainContent$AspNetPager1',
            '__EVENTARGUMENT': str(int(pagenum) + 1),
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate
        }
        if int(pagenum) < 116289:
            yield scrapy.FormRequest(response.url, formdata=payload,
                                     callback=self.parse)


def get_haiguan_ids(start=0, stop=-1):
    r = redis.Redis(host='localhost', port=6379, db=0)
    ids = r.lrange('company_haiguan_detail_id', start, stop)
    return ids


class HaiGuanSpider(scrapy.Spider):
    name = 'haiguan'
    detail_url = "http://www.haiguan.info/infos{id}.aspx"
    start_urls = [
        detail_url.format(id=id.decode()) for id in get_haiguan_ids(0, -1)
    ]

    def parse(self, response):
        def extract_with_xpath(query):
            result = response.xpath(query).extract_first()
            return result.strip() if result else ''

        item = HaiguanItem()
        item['company_name'] = extract_with_xpath(
            "//*[@id='ctl00_MainContent_lblFull_Name']/text()")
        item['industry_type'] = extract_with_xpath(
            "//*[@id='ctl00_MainContent_lblBusi_Type']/text()")
        item['business_scope'] = extract_with_xpath(
            "//*[@id='ctl00_MainContent_lblCOP_Range']/text()")
        item['business_level'] = extract_with_xpath(
            "//*[@id='ctl00_MainContent_lblCO_Class']/text()")
        item['company_url'] = response.url
        item['company_gather_time'] = datetime.now(
        ).strftime("%Y-%m-%d %H:%M:%S")
        item['gather_id'] = 8
        item['chanle_id'] = 0
        yield item
