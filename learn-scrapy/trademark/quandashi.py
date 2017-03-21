
import logging
import os
import time
import redis
import requests
from bs4 import BeautifulSoup


FORMAT = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'quandashi.log')
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=FORMAT
                    )


redis_server = redis.Redis(host='123.196.124.161', port=6379, db=0,
                           password='redispwd')
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,und;q=0.4",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "YZNAME=e42c0141250d02dad20c86609d5d19d155f12717; _csrf=dfc3474c537b5156d4ae4c0fe92571edf8d75bc4804b49d4c28215217ae536f8s%3A32%3A%227GpLrso_dhlHyCx0Liu2Eu2bgP1fDnka%22%3B; PHPSESSID=ljdqi25jojjo66oungsb9ujpp5; QDS_COOKIE=02feb4017d52fe87f1352bf03beb3fa37e999aa1; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guest81624CCA-27C5-2E,tid:1489384191823230}; NTKF_T2D_CLIENTID=guest81624CCA-27C5-2E65-485B-C6373750DC29",
    "Host": "so.quandashi.com",
    "Referer": "http://www.quandashi.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",

}


class Trademark:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = headers
        self.domian = "http://so.quandashi.com"
        self.index_url = "http://so.quandashi.com/index/search?s=%2Findex%2Fsearch&key={keyword}&param=2&signature=812f8383dd3e608694fcc813d468c51919f783c9&nonce=147684&timestamp=0&page={page}&per-page=10"
        self.file = os.path.join(os.path.dirname(__file__), 'quandashi.txt')

    def gather(self):
        keywords = redis_server.lrange(
            'dynamic_gather_keyword_list', 1200000, 1250000)
        count = len(keywords)
        for idx, kw in enumerate(keywords, 1):
            page = 1
            logging.debug("正在查询第%s/%s个公司..." % (idx, count))
            print(time.strftime("%Y-%m-%d %H:%M:%S"),
                  "正在查询第%s/%s个公司..." % (idx, count))

            while True:
                try:
                    url = self.index_url.format(keyword=kw.decode(), page=page)
                    r = self.session.get(url)
                    time.sleep(20)

                    if "温馨提示" in r.text:
                        break

                    soup = BeautifulSoup(r.text, 'lxml')
                    dls = soup.select(".searchLis-result dl")
                    msg = "找到【%s】商标%s个，当前是第【%s】页。" % (kw.decode(), len(dls), page)
                    logging.debug(msg)
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), msg)

                    with open(self.file, 'at') as f:
                        for dl in dls:
                            href = self.domian + dl.a['href']
                            f.write(href)
                            f.write('\n')

                    page += 1
                except Exception as e:
                    logging.debug(str(e))
                    print(str(e))


if __name__ == '__main__':
    Trademark().gather()
