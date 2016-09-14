# -*- coding: utf-8 -*-
"""随机生成6位字符串，只包含字母和数字"""

import random
import string
import os
import sys
from imp import reload


# Answer in one line
''.join(random.choice(string.ascii_uppercase + string.digits)
        for _ in range(6))

# A more secure version
''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(6))


# 在python3中，字符就是unicode字符，字符串就是unicode字符数组
# str转bytes叫encode，bytes转str叫decode
# chrome --> F12 --> Element --> Ctrl + F 通过xpath查找元素


# 用递归方法找到本文件的上n级目录
def parent_filedir(n):
    return parent_filedir_iter(n, os.path.dirname(__file__))


def parent_filedir_iter(n, path):
    n = int(n)
    if n <= 1:
        return path
    return parent_filedir_iter(n - 1, os.path.dirname(path))


testdir = os.path.abspath(parent_filedir(5))
reload(sys)
sys.path.append(testdir)


# python倒计时
import time

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('Goodbye!')
