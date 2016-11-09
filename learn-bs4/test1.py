# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


html = """
<ul class="content-link"><li class=""><h3><div><a href="http://daguu.com/" title="" target="_blank" class="text-con">大谷打工网</a></div></h3></li><li class=""><h3><div><a href="http://www.zhubajie.com/" title="" target="_blank" class="text-con">猪八戒威客网</a></div></h3></li><li class=""><h3><div><a href="http://www.taskcn.com/" title="" target="_blank" class="text-con">任务中国</a></div></h3></li><li class=""><h3><div><a href="http://www.chinalao.com/" title="" target="_blank" class="text-con">中劳网</a></div></h3></li><li class=""><h3><div><a href="http://z.paidai.com/" title="" target="_blank" class="text-con">派代电商招聘</a></div></h3></li><li><h3 class="last-row"><div><a href="http://www.680.com/" title="" target="_blank" class="text-con">时间财富网</a></div></h3></li><li class=""><h3 class="last-row"><div><a href="http://www.lagou.com/" title="" target="_blank" class="text-con">拉勾网IT招聘</a></div></h3></li><li class=""><h3 class="last-row"><div><a href="http://www.quanzhi.com/" title="" target="_blank" class="text-con">全职招聘</a></div></h3></li></ul>
"""


soup = BeautifulSoup(html, "lxml")

links = soup.find_all('a')



for i in links:
    print("[{}]({})".format(i.get_text(), i['href']))

