# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class WebTestBase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_search_in_baidu(self):
        driver = self.driver
        driver.get("https://www.baidu.com/")
        self.assertIn("百度一下，你就知道", driver.title)
        elem = driver.find_element_by_xpath('//*[@id="kw"]')
        elem.clear()
        elem.send_keys("python")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def test_login_zhihu(self):
        xpaths = {
            'email': ("//div[@class='email input-wrapper']"
                      "/input[@name='account']"),
            'passwd': ("//div[@class='view view-signin']"
                       "//div[@class='input-wrapper']/input"),
            'submit': ("//div[@class='view view-signin']"
                       "//button[@class='sign-button submit']")
        }
        driver = self.driver
        driver.get("https://www.zhihu.com/#signin")
        self.assertIn("知乎 - 与世界分享你的知识、经验和见解", driver.title)

        # 输入邮箱
        email = driver.find_element_by_xpath(xpaths['email'])
        email.clear()
        email.send_keys("920507252@qq.com")

        # 输入密码
        passwd = driver.find_element_by_xpath(xpaths['passwd'])
        passwd.clear()
        passwd.send_keys("myzhihu")

        # 登入
        submit = driver.find_element_by_xpath(xpaths['submit'])
        submit.click()

        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
