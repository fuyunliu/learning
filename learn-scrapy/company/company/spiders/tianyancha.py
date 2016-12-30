# -*- coding: utf-8 -*-
"""
GET http://api.tmkoo.com/app-reg.php?mobile=b4:52:7e:ca HTTP/1.1
User-Agent: Dalvik/2.1.0 (Linux; U; Android 5.1.1; C6603 Build/10.7.A.0.228)
===============================================================================
apiKey                           apiPassword                      infocount
===============================================================================
4399320012393234                 331nd3342d                       500次/天
TEST001                          TEST_P_001
appf4:8e:92:24                   qfcqBYITGX
app7c:1d:d9:f7                   /VqgzCA2bj
app68:3e:34:5f                   O2KyEpivfm
appb4:52:7e:ca                   szsjA2bw1B
appb4:53:7e:ca                   HInX7wrzsW
appb4:54:7e:ca                   IkD6ncrA2b
appb4:55:7e:ca                   MByUrA2btL
appb4:56:7e:ca                   i/urGFWDir
appb4:57:7e:ca                   WoRSuwohvv
appb4:58:7e:ca                   VOoZnm3JND
appb4:59:7e:ca                   ch2UBu0XCe
appb4:60:7e:ca                   47CM90GA2b
appb4:61:7e:ca                   1qQCXD9pqk
appb4:62:7e:ca                   RBdPmlXfnh
appb4:63:7e:ca                   0RW6iraSyu
appb4:64:7e:ca                   IkDNP56WcB
appb4:65:7e:ca                   HJnrAcqnyB
app70:3e:34:5f                   WxcQR4A2bN
app71:3e:34:5f                   As1xy79j7Z
app72:3e:34:5f                   weF63yJXZK
app73:3e:34:5f                   MGBZdYysny
app74:3e:34:5f                   wCS6nA2bUn
app75:3e:34:5f                   0BcxWejGxu
app76:3e:34:5f                   ajCPHYkJ27
app77:3e:34:5f                   eNdmmJZmVz
app78:3e:34:5f                   1eys1xeTzL
app79:3e:34:5f                   uyswlQhKyQ
===============================================================================
"""
import re
import math
import json
import scrapy
from datetime import datetime
from company.constants import companies
from company.items import TrademarkItem


tianyancha = "http://www.tianyancha.com/tm/search/{key}.json"
detail_url = "http://api.tmkoo.com/app-info.php?apiKey=4399320012393234&apiPassword=331nd3342d&regNo={regno}&intCls={intcls}"


class TrademarkSpider(scrapy.Spider):
    name = 'tianyancha'
    start_urls = [tianyancha.format(key=key) for key in companies]

    def parse(self, response):
        data = json.loads(response.text)
        if data['state'] == 'ok':
            count = int(data['data']['total'])
            if count != 0:
                for r in data['data']['items']:
                    regno = r['regNo']
                    intcls = re.findall(r'第(\d+)类', r['intCls'])[0]
                    detail = detail_url.format(regno=regno, intcls=intcls)
                    yield scrapy.Request(detail, callback=self.parse_detail)
                pn = int(data['data']['pageNum']) + 1
                if pn <= math.ceil(count / 20):
                    next_page = response.url.split('?')[0] + '?pageNum={pn}'.format(pn=pn)
                    yield scrapy.Request(next_page, callback=self.parse)
        else:
            log = "state: %s, message: %s." % (data['state'], data['message'])
            self.log(log)

    def parse_detail(self, response):
        data = json.loads(response.text)
        if data['ret'] == '0':
            item = TrademarkItem()
            item['company_name'] = data['applicantCn']
            item['trademark_class_code'] = data['intCls']
            item['trademark_name'] = data['tmName']
            item['trademark_appli_code'] = data['regNo']
            item['trademark_apply_time'] = data['appDate']
            status = []
            for f in data['flow']:
                s = f['flowDate'] + f['flowName']
                status.append(s)
            item['trademark_status'] = ''.join(status)
            item['trademark_apply_name'] = data['applicantCn']
            image_weburl = "http://pic.tmkoo.com/pic.php?zch=" + data['tmImg']
            item['trademark_image_weburl'] = image_weburl
            item['trademark_regist_time'] = data['regDate']
            item['trademark_regist_no'] = data['regIssue']
            item['trademark_preli_no'] = data['announcementIssue']
            item['trademark_preli_time'] = data['announcementDate']
            item['trademark_type'] = data['category']
            item['trademark_valid_time'] = data['privateDate']
            item['trademark_agent_name'] = data['agent']
            item['company_url'] = response.url
            item['company_gather_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['gather_id'] = 8
            item['chanle_id'] = 0
            yield item
        else:
            log = "ret: %s, remainCount: %s, msg: %s." % (
                data['ret'], data['remainCount'], data['msg'])
            self.log(log)
