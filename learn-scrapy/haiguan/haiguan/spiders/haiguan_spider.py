# -*- coding: utf-8 -*-

import scrapy
from datetime import datetime
from scrapy.http import FormRequest
from haiguan.items import HaiguanItem


class HaiGuanSpider(scrapy.Spider):
    name = 'haiguan'

    def start_requests(self):
        url = "http://www.haiguan.info/OnLineSearch/IndustryInfo/Default.aspx"
        viewstate = "/wEPDwUJNjQ1ODMwNzI1D2QWAmYPZBYCAgEPZBYEZg8PFgIeB1Zpc2libGVoZGQCAg9kFggCBA8PFgIeBFRleHQFLuWFseaQnOe0ouaciSAxMTYyODgxIOadoe+8jOavj+mhteaYvuekuiAxMCDmnaFkZAIFDxAPFgYeDURhdGFUZXh0RmllbGQFCGNvX2NsYXNzHg5EYXRhVmFsdWVGaWVsZAUIY29fY2xhc3MeC18hRGF0YUJvdW5kZ2QQFQkG5omA5pyJAAABLgFBAkFBAUIBQwFEFQkAAAABLgFBAkFBAUIBQwFEFCsDCWdnZ2dnZ2dnZxYBZmQCBg8WAh4LXyFJdGVtQ291bnQCChYUZg9kFgJmDxUFCjA3MDM5OTAwMDEpTFrlhoXokpnlj6Toh6rmsrvljLrmlofnianogIPlj6TnoJTnqbbmiYAKMDcwMzk5MDAwMQABQmQCAQ9kFgJmDxUFCjA4MDAwMTA1OTgh5rKI6Ziz6YeR5p2v6L+b5Ye65Y+j5pyJ6ZmQ5YWs5Y+4CjA4MDAwMTA1OTgAAUJkAgIPZBYCZg8VBQowOTAwOTkwMDAxLExa5Lit5Zu956eR5a2m6Zmi5aSn6L+e5YyW5a2m54mp55CG56CU56m25omACjA5MDA5OTAwMDEAAUJkAgMPZBYCZg8VBQoxMDM3OTEyMDEyKuW8oOWutuWPo+W4guS6muWMl+WvueWklue7j+a1jui0uOaYk+WFrOWPuAoxMDM3OTEyMDEyAAFCZAIED2QWAmYPFQUKMTEwMDAxOTAwMi3kuK3lm73nlLXmsJTov5vlh7rlj6PogZTokKXlhazlj7jlpKnmtKXlhazlj7gKMTEwMDAxOTAwMgABQmQCBQ9kFgJmDxUFCjExMDAwOTAwMDAb5YyX5Lqs5b635rqQ55S15Zmo5Z+O5YWs5Y+4CjExMDAwOTAwMDAAAUJkAgYPZBYCZg8VBQoxMTAwOTEwMDY2DOmmlumDveWuvummhgoxMTAwOTEwMDY2AAFCZAIHD2QWAmYPFQUKMTEwMDkxMDEzNSHkuK3ljIXljbDliLfnianotYTov5vlh7rlj6Plhazlj7gKMTEwMDkxMDEzNQABQmQCCA9kFgJmDxUFCjExMDEwMTk5OTkq5Zub5bed5r6c5rW35ZOB5oKm5Zu96ZmF6LS45piT5pyJ6ZmQ5YWs5Y+4CjExMDEwMTk5OTkAAUJkAgkPZBYCZg8VBQoxMTAxMDc2MDAxHuWMl+S6rOeJueWugeenkeaKgOaciemZkOWFrOWPuAoxMTAxMDc2MDAxAAFCZAIIDw8WAh4LUmVjb3JkY291bnQCgf1GZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFGGN0bDAwJE1haW5Db250ZW50JEltZ0J0bvYKd4UuIRtsB9Iu5GNhhwdKpnpW+jTHsay4dpqO4toY"
        formdata = {'__EVENTTARGET': 'ctl00$MainContent$AspNetPager1',
                    '__EVENTARGUMENT': '80000',
                    '__LASTFOCUS': '',
                    '__VIEWSTATE': viewstate}
        return [scrapy.FormRequest(url, formdata=formdata, callback=self.parse)]

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
