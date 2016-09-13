"""学习requests"""

import requests
import urllib.request
import urllib3

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'}

r = requests.get('https://www.zhihu.com/', headers=headers)

print(r.ok)

r'^*(\d+)*(\d+)*'
