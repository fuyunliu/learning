# -*- coding: utf-8 -*-

import os
import logging
import itertools
import json
import scrapy
from datetime import datetime
from company.items import StockItem

LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'debug.log')
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# 公告类别，总共24个类别，总数据量220万条以上
plates = {'sz': '深市公司', 'szmb': '深市主板', 'szzx': '中小板',
          'szcy': '创业板', 'shmb': '沪市主板'}
trades = ['农、林、牧、渔业', '采矿业', '制造业', '电力、热力、燃气及水生产和供应业',
          '建筑业', '批发和零售业', '交通运输、仓储和邮政业', '住宿和餐饮业',
          '信息传输、软件和信息技术服务业', '金融业', '房地产业', '租赁和商务服务业',
          '科学研究和技术服务业', '水利、环境和公共设施管理业',
          '居民服务、修理和其他服务业', '教育', '卫生和社会工作',
          '文化、体育和娱乐业', '综合']
categories = [
    {'category': 'category_ndbg_szsh', 'name': '年度报告'},
    {'category': 'category_sjdbg_szsh', 'name': '三季度报告'},
    {'category': 'category_zf_szsh', 'name': '增发'},
    {'category': 'category_qtrz_szsh', 'name': '其他融资'},
    {'category': 'category_jy_szsh', 'name': '交易'},
    {'category': 'category_tbclts_szsh', 'name': '特别处理和退市'},
    {'category': 'category_ssgszd_szsh', 'name': '上市公司制度'},
    {'category': 'category_tzzgx_szsh', 'name': '投资者关系信息'},
    {'category': 'category_bndbg_szsh', 'name': '半年度报告'},
    {'category': 'category_scgkfx_szsh', 'name': '首次公开发行及上市'},
    {'category': 'category_kzhz_szsh', 'name': '可转换债券'},
    {'category': 'category_qyfpxzcs_szsh', 'name': '权益及限制出售股份'},
    {'category': 'category_gddh_szsh', 'name': '股东大会'},
    {'category': 'category_bcgz_szsh', 'name': '补充及更正'},
    {'category': 'category_zqgg_szsh', 'name': '债券公告'},
    {'category': 'category_dshgg_szsh', 'name': '董事会公告'},
    {'category': 'category_yjdbg_szsh', 'name': '一季度报告'},
    {'category': 'category_pg_szsh', 'name': '配股'},
    {'category': 'category_qzxg_szsh', 'name': '权证相关公告'},
    {'category': 'category_gqbd_szsh', 'name': '股权变动'},
    {'category': 'category_cqfxyj_szsh', 'name': '澄清风险业绩预告'},
    {'category': 'category_zjjg_szsh', 'name': '中介机构报告'},
    {'category': 'category_qtzdsx_szsh', 'name': '其它重大事项'},
    {'category': 'category_jshgg_szsh', 'name': '监事会公告'}
]
request_url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
notice_url = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/bulletin_detail/true/{notice_id}"
notice_file_url = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/download/{notice_id}"
payload = {
    'stock': '', 'searchkey': '', 'plate': '', 'category': '', 'trade': '',
    'column': 'szse', 'columnTitle': '历史公告查询', 'pageNum': '',
    'pageSize': '30', 'tabName': 'fulltext', 'sortName': '', 'sortType': '',
    'limit': '', 'showTitle': '', 'seDate': '请选择日期'
}


class StockNtoice(scrapy.Spider):

    name = "stocknotice"
    category, notice_type = categories[0]['category'], categories[0]['name']

    def start_requests(self):
        for i in itertools.product(list(plates.keys()), trades):
            formdata = payload.copy()
            formdata['category'] = self.category
            meta = {'plate': i[0], 'trade': i[1], 'pageNum': '1'}
            formdata.update(meta)
            yield scrapy.FormRequest(request_url, formdata=formdata,
                                     callback=self.parse, meta=meta)

    def parse(self, response):
        data = json.loads(response.text)
        total = data['totalRecordNum']
        plate = response.meta['plate']
        trade = response.meta['trade']
        pn = response.meta['pageNum']
        for a in data['announcements']:
            notice_id = a['announcementId']
            publishtime = int(a['announcementTime']) // 1000
            item = StockItem()
            item['company_name'] = a['secName']
            item['notice_id'] = notice_id
            item['notice_shares_code'] = a['secCode']
            item['notice_title'] = a['announcementTitle']
            item['notice_type'] = self.notice_type
            item['notice_publishtime'] = datetime.fromtimestamp(
                publishtime).strftime("%Y-%m-%d")
            item['notice_url'] = notice_url.format(notice_id=notice_id)
            item['notice_file_url'] = notice_file_url.format(
                notice_id=notice_id)
            item['notice_industry'] = trade
            item['notice_plate'] = plates[plate]
            item['company_gather_time'] = datetime.now(
            ).strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
        message = "公告类别：%s，板块：%s，行业：%s，当前页：%s，总记录：%s" % (
            self.notice_type, plates[plate], trade, pn, total)
        self.log(message)
        if data['hasMore']:
            formdata = payload.copy()
            formdata['category'] = self.category
            meta = {
                'plate': plate, 'trade': trade, 'pageNum': str(int(pn) + 1)
            }
            formdata.update(meta)
            yield scrapy.FormRequest(request_url, formdata=formdata,
                                     callback=self.parse, meta=meta)
