# -*- coding: utf-8 -*-

# 为了理解什么是yield,你必须理解什么是生成器。在理解生成器之前，让我们先走近迭代。
# 当你建立了一个列表，你可以逐项地读取这个列表，这叫做一个可迭代对象。
print_line = lambda x: print('*' * x)
mylist = [1, 2, 3, 4, 5]
for i in mylist:
    print(i)
print_line(20)
# mylist是一个可迭代的对象。当你使用一个列表生成式来建立一个列表的时候，就建立了一个可迭代的对象。
mylist = [x * x for x in range(5)]
for i in mylist:
    print(i)
print_line(20)
# 所有你可以使用for...in...语法的叫做一个迭代器。列表，字符串，文件等等，你经常使用它们是因为你可以如你所愿的读取其中的元素，但是你把所有的值都存储到了内存中，如果你有大量数据的话这个方式并不是你想要的。

# 生成器是可以迭代的，但是你只可以读取它一次，因为它并不把所有的值放在内存中，它是实时地生成数据。
mygenerator = (x * x for x in range(5))
for i in mygenerator:
    print(i)
print(mygenerator)
print(type(mygenerator))
print_line(20)
# 你不可以再次迭代生成器
try:
    next(mygenerator)
except StopIteration:
    print("停止迭代")
print('*' * 20)


# yield是一个类似return的关键字，只是这个函数返回的是个生成器。
def create_generator():
    for i in range(5):
        yield i * i


mygenerator = create_generator()  # 如果函数内部使用return，则返回0
print(mygenerator)
for i in mygenerator:
    print(i)
print_line(20)


# 斐波拉契数列
def fib():
    x, y = 0, 1
    while True:
        x, y = y, x + y
        yield x

# 获取斐波拉契数列前10个
import itertools
print(list(itertools.islice(fib(), 10)))
print_line(20)


# 杨辉三角
def triangle():
    a = [1]
    while True:
        yield a
        a = [sum(i) for i in zip([0] + a, a + [0])]

# 输出前10行杨辉三角
import pprint
pprint.pprint(list(itertools.islice(triangle(), 10)))
print_line(20)


# 控制迭代器的穷尽
class Bank():
    crisis = False  # crisis是危机的意思

    def create_atm(self):
        while not self.crisis:
            yield "$100"


bank = Bank()  # 创建一个银行
corner_street_atm = bank.create_atm()  # 创建一个ATM机
print([next(corner_street_atm) for _ in range(5)])
bank.crisis = True  # 危机来了
try:
    print(next(corner_street_atm))
except StopIteration:
    print("corner_street_atm: no more money!")
try:
    wall_street_atm = bank.create_atm()
    print(next(wall_street_atm))
except StopIteration:
    print("wall_street_atm: no more money!")
bank.crisis = False  # 问题是，即使改变crisis的值，ATM依然是空的
try:
    print(next(corner_street_atm))
except StopIteration:
    print("crisis is %s, and still no more money!" % bank.crisis)
# 重新创建一个ATM机，现在有钱了
brand_new_atm = bank.create_atm()
print([next(brand_new_atm) for _ in range(5)])
print_line(20)

# itertools模块包含了许多特殊的迭代方法
# 比赛中4匹马可能到达终点的先后顺序的可能情况
horses = [1, 2, 3, 4]
races = itertools.permutations(horses)
print(races)
pprint.pprint(list(races))
print_line(20)


# 一个实现了__iter__方法的对象是可迭代的，一个实现了__next__方法的对象是迭代器。
class Fibs():

    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

    def __iter__(self):
        return self


fibs = Fibs()
print([next(fibs) for _ in range(10)])
print_line(20)
