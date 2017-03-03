# -*- coding: utf-8 -*-

import re
import scrapy
from company.items import GmpGspUrlItem


gmp_url = "http://app1.sfda.gov.cn/datasearch/face3/search.jsp?tableId=23&bcId=118715589530474392063703010776&curstart={p}"
gsp_url = "http://app1.sfda.gov.cn/datasearch/face3/search.jsp?tableId=24&bcId=118715593187347941914723540896&curstart={p}"
gmp_detail_url = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=23&tableName=TABLE23&Id={Id}"
gsp_detail_url = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=24&tableName=TABLE24&Id={Id}"


class GmpGspSpider(scrapy.Spider):
    name = 'gmpgsp_url'
    start_urls = [gmp_url.format(p=p) for p in range(1, 2000)]

    def parse(self, response):
        for href in response.xpath("//a/@href").extract():
            Id = re.findall(r'.*Id=(\d+).*', href)[0]
            url = gmp_detail_url.format(Id=Id)
            item = GmpGspUrlItem()
            item['url'] = url
            yield item
