# -*- coding: utf-8 -*-

import requests


yanzhengma_url = "http://wenshu.court.gov.cn/Content/CheckVisitCode"
r = requests.post(yanzhengma_url, data={'ValidateCode': '5515'})
