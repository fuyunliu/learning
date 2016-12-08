# -*- coding: utf-8 -*-

import re
import random
import scrapy
from datetime import datetime
from scrapy.http import FormRequest
from company.items import HaiguanItem, HaiGuanIdItem
from company.headers import viewstates


class HaiGuanSpider(scrapy.Spider):
    name = 'haiguan'

    def start_requests(self):
        url = "http://www.haiguan.info/OnLineSearch/IndustryInfo/Default.aspx"
        for p in range(100, 5000):  # 共116289页
            formdata = {
                '__EVENTTARGET': 'ctl00$MainContent$AspNetPager1',
                '__EVENTARGUMENT': str(p),
                '__LASTFOCUS': '',
                '__VIEWSTATE': random.choice(viewstates)
            }
            yield FormRequest(url, formdata=formdata)

    def parse(self, response):
        for href in response.xpath(
                "//div[@class='qy_nr blue']//h2/a/@href").extract():
            try:
                Id = re.findall(r'/infos(\d+)\.aspx', href)[0]
                item = HaiGuanIdItem()
                item['Id'] = Id
                yield item
            except Exception as e:
                self.log(str(e))
        curpage = response.xpath(
            "//input[@id='ctl00$MainContent$AspNetPager1_input']/@value").extract_first()
        print('*' * 20 + '已采集至' + curpage + '页' + '*' * 20)

    # def parse(self, response):
    #     for href in response.xpath(
    #             "//div[@class='qy_nr blue']//h2/a/@href").extract():
    #         Id = re.findall(r'/infos(\d+)\.aspx', href)[0]
    #         item = HaiGuanIdItem()
    #         item['Id'] = Id
    #         yield item
    #     curpage = response.xpath(
    #         "//input[@id='ctl00$MainContent$AspNetPager1_input']/@value").extract_first()
    #     print('*' * 10 + '正在采集第' + curpage + '页' + '*' * 10)
    #     viewstate = response.xpath(
    #         "//*[@id='__VIEWSTATE']/@value").extract_first()
    #     yield FormRequest.from_response(
    #         response, formname="aspnetForm",
    #         formdata={'__EVENTTARGET': 'ctl00$MainContent$AspNetPager1',
    #                   '__EVENTARGUMENT': str(int(curpage) + 1),
    #                   '__LASTFOCUS': '',
    #                   '__VIEWSTATE': viewstate},
    #         callback=self.parse)

    # def parse_detail(self, response):
    #     def extract_with_xpath(query):
    #         result = response.xpath(query).extract_first()
    #         return result.strip() if result else ''

    #     item = HaiguanItem()
    #     item['company_name'] = extract_with_xpath(
    #         "//*[@id='ctl00_MainContent_lblFull_Name']/text()")
    #     item['industry_type'] = extract_with_xpath(
    #         "//*[@id='ctl00_MainContent_lblBusi_Type']/text()")
    #     item['business_scope'] = extract_with_xpath(
    #         "//*[@id='ctl00_MainContent_lblCOP_Range']/text()")
    #     item['business_level'] = extract_with_xpath(
    #         "//*[@id='ctl00_MainContent_lblCO_Class']/text()")
    #     item['company_gather_time'] = datetime.now(
    #     ).strftime("%Y-%m-%d %H:%M:%S")
    #     item['gather_id'] = 8
    #     item['chanle_id'] = 0
    #     yield item
