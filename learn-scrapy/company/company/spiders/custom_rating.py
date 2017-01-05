# # -*- coding: utf-8 -*-

# import redis
# import scrapy
# from datetime import datetime
# from company.items import HaiguanItem


# detail_url = "http://www.haiguan.info/infos{id}.aspx"
# r = redis.Redis(host='localhost', port=6379, db=0)
# ids = r.lrange('company_haiguan_detail_id', -10000, -1)


# class HaiGuanSpider(scrapy.Spider):
#     name = 'haiguan'
#     start_urls = [detail_url.format(id=id.decode()) for id in ids]

#     def parse(self, response):
#         def extract_with_xpath(query):
#             result = response.xpath(query).extract_first()
#             return result.strip() if result else ''

#         item = HaiguanItem()
#         item['company_name'] = extract_with_xpath(
#             "//*[@id='ctl00_MainContent_lblFull_Name']/text()")
#         item['industry_type'] = extract_with_xpath(
#             "//*[@id='ctl00_MainContent_lblBusi_Type']/text()")
#         item['business_scope'] = extract_with_xpath(
#             "//*[@id='ctl00_MainContent_lblCOP_Range']/text()")
#         item['business_level'] = extract_with_xpath(
#             "//*[@id='ctl00_MainContent_lblCO_Class']/text()")
#         item['company_gather_time'] = datetime.now(
#         ).strftime("%Y-%m-%d %H:%M:%S")
#         item['gather_id'] = 8
#         item['chanle_id'] = 0
#         yield item
