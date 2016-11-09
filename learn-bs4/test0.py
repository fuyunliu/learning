# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = "http://221.226.175.76:8038/webapp/area/jsgy/zxxx/ajax.jsp?nd=2015&fydm=&dz=&zh=&fymc=&opt=getSxbzxrList&bzxr=%E5%85%AC%E5%8F%B8&xxlx=0&currentPage=2"

r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, "lxml")
