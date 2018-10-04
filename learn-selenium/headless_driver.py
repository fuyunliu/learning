# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 驱动无头浏览器
options = Options()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('window-size=1200x600')
chrome = webdriver.Chrome(chrome_options=options)
