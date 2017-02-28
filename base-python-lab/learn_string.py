# -*- coding: utf-8 -*-
"""python3默认的源码编码方式是utf-8，所以第一行可以省略，除非你想指定其他编码方式"""

import locale
import random
import string
import sys
import os
import time
from imp import reload


# Answer in one line
''.join(random.choice(string.ascii_uppercase + string.digits)
        for _ in range(6))

# A more secure version
''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(6))


# 在python3中，字符就是unicode字符，字符串就是unicode字符数组
# str转bytes叫encode，bytes转str叫decode
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
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('Goodbye!')


# python遇到编码问题，IDE不能输出中文，请设置环境变量PYTHONIOENCODING为utf-8。
# 其实是在Anaconda Python Builder下不能输出中文，Python正常。
# PYTHONIOENCODING的值会覆盖sys.std.out.encoding的值。
# sys.setdefaultencoding('utf-8')方法是错误的，并且在python3中已被移除。
print(sys.getdefaultencoding())
print(sys.stdout.encoding)
print(sys.stdin.encoding)
print(sys.stderr.encoding)
print()
print(sys.stdout.isatty())
print(locale.getpreferredencoding())
print(sys.getfilesystemencoding())
print(os.environ.get("PYTHONIOENCODING"))

# 测试输出
print("测试输出中文")
print(chr(246), chr(9786), chr(9787))
