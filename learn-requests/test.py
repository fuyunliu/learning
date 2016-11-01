# -*- coding: utf-8 -*-

import requests

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36')
}

r = requests.get('https://www.zhihu.com/', headers=headers)

print(r.ok)
