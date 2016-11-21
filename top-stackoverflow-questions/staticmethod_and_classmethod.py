# -*- coding: utf-8 -*-


print_line = lambda x: print('*' * x)
# 实例方法，类方法和静态方法的区别
class A(object):

    def foo(self, x):
        print("executing foo(%s, %s)" % (self, x))

    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s, %s)" % (cls, x))

    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)


a = A()
# 实例方法的第一个参数是实例本身
A.foo(a, 1)
a.foo(1)
print_line(50)

# 类方法的第一个参数是类对象
A.class_foo(1)
a.class_foo(1)
print_line(50)

# 静态方法和定义在类之外的普通函数一样，可以没有参数
A.static_foo(1)
a.static_foo(1)
