# -*- coding: utf-8 -*-

import scrapy
from datetime import datetime
from scrapy.http import FormRequest
from company.items import HaiguanItem


class HaiGuanSpider(scrapy.Spider):
    name = 'haiguan'
    start_urls = [
        'http://www.haiguan.info/OnLineSearch/IndustryInfo/Default.aspx'
    ]

    def parse(self, response):
        for href in response.xpath(
                "//div[@class='qy_nr blue']//h2/a/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_detail)

        curpage = response.xpath(
            "//input[@id='ctl00$MainContent$AspNetPager1_input']/@value").extract_first()
        print('*' * 10 + '正在采集第' + curpage + '页' + '*' * 10)
        viewstate = response.xpath(
            "//*[@id='__VIEWSTATE']/@value").extract_first()
        yield FormRequest.from_response(
            response, formname="aspnetForm",
            formdata={'__EVENTTARGET': 'ctl00$MainContent$AspNetPager1',
                      '__EVENTARGUMENT': str(int(curpage) + 1),
                      '__LASTFOCUS': '',
                      '__VIEWSTATE': viewstate},
            callback=self.parse)

    def parse_detail(self, response):
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
        item['company_gather_time'] = datetime.now(
        ).strftime("%Y-%m-%d %H:%M:%S")
        item['gather_id'] = 8
        item['chanle_id'] = 0
        yield item
