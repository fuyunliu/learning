# -*- coding: utf-8 -*-


print_line = lambda x: print('*' * x)
# 在python如果用list作为函数的参数会让人困惑
def foo(a=[]):
    a.append(5)
    return a


print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print_line(50)


# 可以看出上面的调用都是调用了同一个函数对象，而这个函数对象绑定了初始化数据，列表是可变的。
# 所以要避免使用可变对象作为函数的参数，上面的函数更改如下：
def foo(a=None):
    if a is None:
        a = []
    a.append(5)
    return a


print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()

print(foo())
print(id(foo()))
print()
