# -*- coding: utf-8 -*-

import re
import scrapy
from bs4 import BeautifulSoup
from company.items import CreditItem
from org.wzty.utils.strings.String_Manager import Utils_String
list_url = 'http://bcp.12312.gov.cn/ratingList?sid=1&rn=30&pn={pn}'


class CreditSpider(scrapy.Spider):

    name = 'credit'
    start_urls = [list_url.format(pn=p) for p in range(1, 474)]

    def parse(self, response):
        for href in response.xpath("//a[text()='查看']/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            html = response.css('.pj_content').extract_first()
            soup = BeautifulSoup(html, 'lxml')
            content = re.sub(r'\s', '', soup.text)
            su = Utils_String()
            item = CreditItem()
            company_name = su.parse_static(content, '', 0, '【评价结果信息】', 0)
            item['company_name'] = re.findall(r'[\u4e00-\u9fa5]+', company_name)[0]
            item['credit_rating'] = su.parse_static(content, '评价等级：', 0, 'EvaluationUnit：', 0)
            item['credit_certifi_code'] = su.parse_static(content, '证书编号：', 0, 'CertificateNumber：', 0)
            item['credit_certifi_time'] = su.parse_static(content, '颁发日期：', 0, 'IssueDate：', 0)
            item['credit_validit_period'] = su.parse_static(content, '有效期至：', 0, 'ValidPeriod：', 0)
            item['credit_certifi_unit'] = su.parse_static(content, '发证单位（协会）：', 0, 'IssueUnit：', 0)
            item['company_org_code'] = su.parse_static(content, '组织机构代码：', 0, 'OrganizationCode：', 0)
            item['company_regis_code'] = su.parse_static(content, '工商注册号：', 0, 'RegistrationNumber：', 0)
            item['credit_url'] = response.url
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
        except Exception as e:
            self.log('ERROR: %s' % str(e))
