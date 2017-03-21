
import logging
import os
import time
import redis
import requests
from bs4 import BeautifulSoup


FORMAT = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'debug.log')
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=FORMAT
                    )


redis_server = redis.Redis(host='123.196.124.161', port=6379, db=0,
                           password='redispwd')
headers = {
    "Accept": "text/html, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,und;q=0.4",
    "Connection": "keep-alive",
    "Cookie": "statistics=2017031309073759835; qpZg_90cd_search1=d959a46jREHtaTWmxHZ63KnqqJ85UNDhEvgEW42Zyv8hTMH9R099Lyuj11xEWnoYac2wYF%2BL0G5%2FwG3nb8aVeiqrWsOe33VnMmjF8P9dv4Q6DLGOuksZ",
    "Host": "m.biaoju01.com",
    "Referer": "http://m.biaoju01.com/trademark/index/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


class Trademark:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = headers
        self.domian = "http://m.biaoju01.com"
        self.search_url = "http://m.biaoju01.com/proposer/index/?keyword={keyword}"
        self.file = os.path.join(os.path.dirname(__file__), 'biaoju.txt')

    def gather(self):
        keywords = redis_server.lrange(
            'dynamic_gather_keyword_list', 14048, 50000)
        count = len(keywords)
        for idx, kw in enumerate(keywords, 1):
            logging.debug("正在查询第%s/%s个公司..." % (idx, count))
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "正在查询第%s/%s个公司..." % (idx, count))

            url = self.search_url.format(keyword=kw.decode())
            r = self.session.get(url)
            time.sleep(20)

            if not r.text.strip():
                continue

            soup = BeautifulSoup(r.text, 'lxml')
            links = soup.select("td.td-more a")
            print("\t\t\t找到%s个申请人" % len(links))
            for link in links:
                page = 1
                while True:
                    url = self.domian + link['href']
                    r = self.session.get(url, params={'page': page})
                    time.sleep(20)

                    if r.text == '\t\t\t':
                        break

                    soup = BeautifulSoup(r.text, 'lxml')
                    details = soup.select("td.td-more a")
                    print("\t\t\t\t找到%s个商标" % len(details))

                    with open(self.file, 'at') as f:
                        for a in details:
                            href = self.domian + a['href']
                            f.write(href)
                            f.write('\n')

                    page += 1


if __name__ == '__main__':
    Trademark().gather()
