# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from company.items import NaShuiItem

list_url = "http://hd.chinatax.gov.cn/fagui/action/InitCredit.do?articleField01=&articleField02=&articleField03=2015&articleField06=&taxCode=&cPage={p}&randCode=&flag=1"


class HaiGuanSpider(scrapy.Spider):
    name = 'nashui'
    start_urls = [list_url.format(p=p) for p in range(20802, 25987)]

    def parse(self, response):
        html = response.xpath("//td[@class='sv_hei']/table[1]").extract_first()
        soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
        trs = soup.find_all('tr')
        del trs[0]
        for tr in trs:
            tds = tr('td')
            item = NaShuiItem()
            item['taxpayer_code'] = tds[0].get_text(strip=True)
            item['company_name'] = tds[1].get_text(strip=True)
            item['evaluate_year'] = tds[2].get_text(strip=True)
            item['grant_enterprise'] = ''
            item['tax_level'] = 'A'
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
