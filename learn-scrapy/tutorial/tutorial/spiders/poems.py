# -*- coding: utf-8 -*-

import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'poems'
    start_urls = ['http://poetry.eserver.org/sonnets/']

    def parse(self, response):
        for link in response.xpath("//tt/a/@href").extract():
            yield scrapy.Request(response.urljoin(link),
                                 callback=self.parse_poems)

    def parse_poems(self, response):
        def extract_first_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        def extract_with_xpath(query):
            return response.xpath(query).extract()

        content = extract_with_xpath("/html/body/div/p/text()")
        yield {
            'title': extract_first_with_xpath("//h3/text()"),
            'content': '\n'.join([x.strip() for x in content])
        }
