import requests
from bs4 import BeautifulSoup
rs = requests.session()

keyword = input("Please input keyword:")  # 输入关键字
payload = {  # payload为post过去的数据
    "_CSRFToken": "",
    "captcha": "",
    "email": "b1577084@trbvn.com",
    "from": "login",
    "password": "123456a",
    "rememberMe": "1",
}
res2 = rs.post(
    "http://www.dajie.com/account/newloginsubmit?callback=LOGIN_CALLBACK&ajax=1", data=payload)  # 登录
# res2 = rs.get("http://www.dajie.com/home")


soup = BeautifulSoup(res2.content, "lxml")
# print(soup.script)
# print(soup.script.text[93:].split('\'')[1])
csrf1 = soup.script.text[93:].split('\'')[1]  # 获取到csrftoken的值，为了下一步发送请求
# print(csrf1)

# 发送下一个请求，目的是为了获取到csrf2的值
res3 = rs.get(
    "http://so.dajie.com/job/search?from=home&jobsearch=6&keyword=%E7%A8%8B%E5%BA%8F%E5%91%98&_CSRFToken=" + csrf1)
soup = BeautifulSoup(res3.content, "lxml")
# print(soup.script)
# print(soup.script.text[93:].split('\'')[1])
csrf2 = soup.script.text[93:].split('\'')[1]
print(csrf2)
page = 1  # 页数
listsalary = []  # 定义一个列表，用来存放获取到的字符串
while page < 11:
    print("\n" + str(page) + "\n")
    payload = {
        "CSRFToken": csrf2,
        "ajax": "1",
        "city": "",
        "segree": "",
        "experience": "",
        "from": "auto",
        "jobsearch": "6",
        "keyword": keyword,
        "order": "0",
        "page": page,
        "pagereferer": "http://www.dajie.com/home?f=inbound",
        "positionFunction": "",
        "positionIndustry": "",
        "quality": "",
        "recruitType": "",
        "salary": "",
    }

    headers = {  # referer是必须要填写的。并且csrf1必须正确，否则返回404.
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://so.dajie.com/job/search?from=home&jobsearch=6&keyword=%E7%A8%8B%E5%BA%8F%E5%91%98&_CSRFToken=" + csrf1,
    }
    res4 = rs.get("http://so.dajie.com/job/ajax/search/filter",
                  params=payload, headers=headers)
    print(res4.url)
    # print(res4.json())
