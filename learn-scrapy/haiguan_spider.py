# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest


class HaiGuanSpider(scrapy.Spider):
    name = 'haiguan'
    download_delay = 5
    start_urls = [
        'http://www.haiguan.info/OnLineSearch/IndustryInfo/Default.aspx']

    def parse(self, response):
        for href in response.xpath(
                "//div[@class='qy_nr blue']//h2/a/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_detail)

        curpage = response.xpath(
            "//input[@id='ctl00$MainContent$AspNetPager1_input']/@value").extract_first()
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

        item = {
            'company_name': extract_with_xpath(
                "//*[@id='ctl00_MainContent_lblFull_Name']/text()"),
            'industry_type': extract_with_xpath(
                "//*[@id='ctl00_MainContent_lblBusi_Type']/text()"),
            'business_scope': extract_with_xpath(
                "//*[@id='ctl00_MainContent_lblCOP_Range']/text()"),
            'business_level': extract_with_xpath(
                "//*[@id='ctl00_MainContent_lblCO_Class']/text()")
        }
        yield item
