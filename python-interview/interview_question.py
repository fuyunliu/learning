# -*- coding: utf-8 -*-
"""python面试题目总结"""


# python之禅
import this


# 一些pythonic
# 交换两个变量值
a, b = b, a


# 去掉list中的重复元素
old_list = [1, 1, 1, 3, 4]
new_list = list(set(old_list))


# 翻转一个字符串
s = 'abcde'
ss = s[::-1]


# 用两个元素之间有对应关系的list构造一个dict
names = ['jianpx', 'yue']
ages = [23, 40]
m = dict(zip(names, ages))


# 将数量较多的字符串相连，如何效率较高，为什么
fruits = ['apple', 'banana']
result = ''.join(fruits)

# python字符串效率问题之一就是在连接字符串的时候使用‘+’号，例如 s = s1 + s2 + s3 +
# ...+ sN，总共将N个字符串连接起来， 但是使用+号的话，python需要申请N-1次内存空间，
# 然后进行字符串拷贝。原因是字符串对象PyStringObject在python当中是不可变对象
# 所以每当需要合并两个字符串的时候，就要重新申请一个新的内存空间 （大小为两个字符串长度之和）来给这个合并之后的新字符串，然后进行拷贝。
# 所以用+号效率非常低。建议在连接字符串的时候使用字符串本身的方法 join（list），这个方法能提高效率，原因是它只是申请了一次内存空间，
# 因为它可以遍历list中的元素计算出总共需要申请的内存空间的大小，一次申请完。


# 你调试python代码的方法有哪些?
import ipdb
ipdb.set_trace()


# 什么是GIL?
# 什么是GIL(Global Interpreter Lock)全局解释器锁? 简单地说就是:
# 每一个interpreter进程,只能同时仅有一个线程来执行, 获得相关的锁, 存取相关的资源.
# 那么很容易就会发现,如果一个interpreter进程只能有一个线程来执行,
# 多线程的并发则成为不可能, 即使这几个线程之间不存在资源的竞争.
# 从理论上讲,我们要尽可能地使程序更加并行, 能够充分利用多核的功能.


# 元类
# 用来创建类的东西


# 对比一下dict中items与iteritems?
D = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
D.items()  # 一次性取出所有
# [('a', 1), ('c', 3), ('b', 2), ('d', 4)]

D.iteritems()  # 迭代对象，每次取出一个。用for循环遍历出来；
# <dictionary-itemiterator object at 0x00000000026243B8>

for i in D.iteritems():
    print(i)
# ('a', 1)('c', 3)('b', 2)('d', 4)

for k, v in D.iteritems():
    print(k)
# a c b d
# 总结:
# 1. 一般iteritems()迭代的办法比items()要快，特别是数据库比较大时。
# 2. 在Python3中一般取消前者函数


# python的模块间循环引用
# 代码组织不够清晰
# 1. 使用 “__all__” 白名单开放接口
# 2. 尽量避免 import


# 用Python生成指定长度的斐波那契数列
def fibs(x):
    result = [0, 1]
    for index in range(x - 2):
        result.append(result[-2] + result[-1])
    return result

if __name__ == '__main__':
    num = input('Enter one number: ')
    print(fibs(num))


# Python里如何生产随机数
import random
random.random()
random.randint(1,11)
random.choice(range(11))


# Python里如何反序的迭代一个序列
# 如果是一个list, 最快的解决方案是：
list1.reverse()
try:
    for x in list1:
        pass
finally:
    list1.reverse()

# 如果不是list, 最通用但是稍慢的解决方案是：
for i in range(len(sequence)-1, -1, -1):
x = sequence[i]


# Python程序中文输出问题怎么解决
# 文件开头# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 如何用Python删除一个文件
import os
os.remove(filename)


# Python是如何进行内存管理的
# python内部使用引用计数来保持追踪内存中的对象，Python内部记录了对象有多少个引用，即引用计数，
# 当对象被创建时就创建了一个引用计数，当对象不再需要时，这个对象的引用计数为0时，它被垃圾回收。
# 所有这些都是自动完成，不需要像C一样，人工干预，从而提高了程序员的效率和程序的健壮性。


# 列表的交、并、差


# Python如何copy一个文件
import shutil
shutil.copyfile('a.py', 'copy_a.py')


# Python判断当前用户是否是root
import os
if os.getuid() != 0:    # root账号的uid=0
    print os.getuid()
    print 'Should run as root account'
else:
    print 'Hello, Root!'


# 打乱一个排好序的list对象alist
# random模块中的shuffle(洗牌函数)
import random
alist = [1, 2, 3, 4]
random.shuffle(alist)
print alist


# Python处理命令行参数示例代码
# 最简单、最原始的方法就是手动解析了
import sys
for arg in sys.argv[1:]:
    print(arg)
