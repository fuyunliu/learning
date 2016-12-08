# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    url = "http://app1.sfda.gov.cn/datasearch/face3/search.jsp?tableId=24&bcId=118715593187347941914723540896&curstart=12"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    alert = driver.switch_to_alert()
    alert.accept()
    time.sleep(20)
    alert.send_keys(Keys.TAB)
    time.sleep(20)
    alert.send_keys(Keys.ENTER)
    time.sleep(20)
    alert.accept()
    time.sleep(120)


if __name__ == '__main__':
    main()
