# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from company.items import SecureItem

list_url = "http://media.chinasafety.gov.cn:8090/zhengfu3/aqxkzcx_jg.jsp?currentPage={p}"


class SecureSpider(scrapy.Spider):
    name = 'secure'
    start_urls = [list_url.format(p=p) for p in range(200, 421)]

    def parse(self, response):
        html = response.xpath("(//table)[2]").extract_first()
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        del trs[0]
        for tr in trs:
            tds = tr('td')
            item = SecureItem()
            item['secure_code'] = tds[0].get_text(strip=True)
            item['secure_area'] = tds[1].get_text(strip=True)
            item['company_name'] = tds[2].get_text(strip=True)
            item['company_legal_name'] = tds[3].get_text(strip=True)
            item['secure_industry'] = tds[4].get_text(strip=True)
            item['company_class_name'] = tds[5].get_text(strip=True)
            item['secure_pro_ability'] = tds[6].get_text(strip=True)
            item['secure_level'] = tds[7].get_text(strip=True)
            item['secure_issue_time'] = tds[8].get_text(strip=True)
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
