# -*- coding: utf-8 -*-
"""有时爬取某些网站时，我们需要禁用javascript"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# firefox驱动下载，加入PATH
# https://github.com/mozilla/geckodriver/releases
# firefox禁用javascript
binary = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", False)
firefox = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)

# chrome禁用javascript
options = Options()
prefs = {'profile.managed_default_content_settings.javascript': 2}
options.add_experimental_option("prefs", prefs)
chrome = webdriver.Chrome(chrome_options=options)

# chrome禁止弹出式窗口
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)

# chrome禁用图片
options = Options()
prefs = {'profile.managed_default_content_settings.images': 2}
options.add_experimental_option("prefs", prefs)
chrome = webdriver.Chrome(chrome_options=options)
