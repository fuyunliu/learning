# -*- coding: utf-8 -*-

import re
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from company.items import GmpgspItem

list_url = "http://app1.sfda.gov.cn/datasearch/face3/search.jsp?tableId=23&bcId=118715589530474392063703010776&curstart={p}&tableName=TABLE23&viewtitleName=COLUMN152&viewsubTitleName=COLUMN151&tableView=GMP%25E8%25AE%25A4%25E8%25AF%2581"
detail_url = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=23&tableName=TABLE23&tableView=&Id={Id}"


class GmpgspSpider(scrapy.Spider):
    name = 'gmpgsp'
    start_urls = [list_url.format(p=p) for p in range(1, 1858)]

    def parse(self, response):
        html = response.xpath("//table[2]").extract_first()
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('a')
        for link in links:
            Id = re.findall(r'.*Id=(\d+).*', link['href'])[0]
            url = detail_url.format(Id=Id)
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        html = response.xpath("//table[1]").extract_first()
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')[1:-2]
        item = GmpgspItem()
        if len(trs) == 12:
            item['gmp_gsp_province'] = trs[0]('td')[1].get_text(strip=True)
            item['gmp_gsp_code'] = trs[1]('td')[1].get_text(strip=True)
            item['company_name'] = trs[2]('td')[1].get_text(strip=True)
            item['gmp_gsp_address'] = trs[3]('td')[1].get_text(strip=True)
            item['gmp_gsp_scope'] = trs[4]('td')[1].get_text(strip=True)
            item['gmp_gsp_issue_time'] = trs[5]('td')[1].get_text(strip=True)
            item['gmp_gsp_validity_time'] = trs[6]('td')[1].get_text(strip=True)
            item['gmp_gsp_continue_time'] = trs[7]('td')[1].get_text(strip=True)
            item['gmp_gsp_continue_to'] = trs[8]('td')[1].get_text(strip=True)
            item['gmp_gsp_continue_scope'] = trs[9]('td')[1].get_text(strip=True)
            item['gmp_gsp_version_gmp'] = trs[10]('td')[1].get_text(strip=True)
            item['gmp_gsp_remarks'] = trs[11]('td')[1].get_text(strip=True)
            item['company_url'] = response.url
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
