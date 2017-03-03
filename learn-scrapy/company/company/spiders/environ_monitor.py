# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from company.items import EnvironItem

list_url = "http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462849093743&page.pageNo={p}"


class EnvironSpider(scrapy.Spider):
    name = 'huanjing'
    start_urls = [list_url.format(p=p) for p in range(1, 3458)]

    def parse(self, response):
        html = response.xpath("//*[@id='GridView1']").extract_first()
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        del trs[0]
        for tr in trs:
            tds = tr('td')
            item = EnvironItem()
            item['monitor_area_code'] = tds[1].get_text(strip=True)
            item['monitor_legal_name_code'] = tds[2].get_text(strip=True)
            item['company_name'] = tds[3].get_text(strip=True)
            item['monitor_class'] = tds[4].get_text(strip=True)
            item['monitor_province'] = tds[5].get_text(strip=True)
            item['monitor_year'] = tds[6].get_text(strip=True)
            item['site_name'] = '中华人民共和国环境保护部--数据中心'
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
