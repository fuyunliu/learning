# -*- coding: utf-8 -*-

import sys
import locale
import os

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
