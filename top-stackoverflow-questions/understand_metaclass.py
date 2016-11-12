# -*- coding: utf-8 -*-
print_line = lambda x: print('*' * x)


# python中类的概念借鉴于Smalltalk，在大多数语言中类就是一段用于生成一个对象的代码。
class ObjectCreator(object):
    pass


myobj = ObjectCreator()
print(myobj)
print_line(50)

# 但是类在python中也是对象，每当你用class关键字申明一个类时，python就会执行它并创建一个对象。比如上面的代码，python在内存中创建了一个名为ObjectCreator的对象。
# 类对象本身也有创建对象（实例）的能力，这就是为什么它叫做类。
# 但是同时，类本身也是个对象，因此你可以把它赋给一个变量，拷贝，添加属性或者作为函数的参数。
print(ObjectCreator) # 你可以打印它，因为它是一个对象
def echo(obj):
    print(obj)
echo(ObjectCreator) # 你可以把类作为参数传递
print(hasattr(ObjectCreator, 'new_attribute'))
ObjectCreator.new_attribute = 'foo' # 你可以给它添加属性
print(hasattr(ObjectCreator, 'new_attribute'))
print(ObjectCreator.new_attribute)
ObjectCreatorMirror = ObjectCreator # 你可以把它赋给一个变量
print(ObjectCreatorMirror.new_attribute)
print(ObjectCreatorMirror())
print_line(50)


# 因为类也是一个对象，你可以像任何其他对象一样动态地创建它。
def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo # 注意这里返回类，而不是实例
    else:
        class Bar(object):
            pass
        return Bar

MyClass = choose_class('foo')
print(MyClass) # 函数返回的是一个类，而不是实例
print(MyClass()) # 你可以用这个类创建一个实例对象
print_line(50)

# 但这还不够动态，因为你还得自己手动编写整个类的代码。既然类是对象，那么肯定有什么东西来生成它，每当你使用class关键字时，python就自动创建这个对象，但是python也给你自己动手的机会，还记得type这个古老的函数吗？它返回这个对象的类型。
print(type(1))
print(type('1'))
print(type(ObjectCreator))
print(type(ObjectCreator()))
print_line(50)

# type还有另一种完全不同的能力，它也能够动态地创建类，type接受一个类地描述作为参数然后返回一个类。
# 比如下面这个类可以这样手动创建
"""
class MyShinyClass(object):
    pass


type(name of the class,
     tuple of the parent class (for inheritance, can be empty),
     dictionary containing attributes names and values)
"""
MyShinyClass = type('MyShinyClass', (), {}) # 返回类对象
print(MyShinyClass)
print(MyShinyClass())
print_line(50)

# 再来个例子
"""
class Foo(object):
    bar = True
"""
# 可以写成
Foo = type('Foo', (), {'bar': True})
# 然后我们像正常的类一样来使用它
print(Foo)
print(Foo.bar)
f = Foo()
print(f)
print(f.bar)
# 我们还可以继承它
FooChild = type('FooChild', (Foo,), {})
print(FooChild)
print(FooChild.bar) # bar属性从Foo继承
# 在类中添加方法
def echo_bar(self):
    print(self.bar)

FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
print(hasattr(Foo, 'echo_bar'))
print(hasattr(FooChild, 'echo_bar'))
my_foo = FooChild()
my_foo.echo_bar()
print_line(50)

# 综上，type就是元类，用于创建所有类的元类，是python内建的元类，你也可以创建自己的元类
# 不信你看
age = 35
name = 'fuyun'
def foo(): pass
class Bar(object): pass
print(age.__class__)
print(age.__class__.__class__)
print(name.__class__)
print(name.__class__.__class__)
print(foo.__class__)
print(foo.__class__.__class__)
print(Bar().__class__)
print(Bar().__class__.__class__)
print_line(50)

# 当你创建一个类的时候，你可以添加__metaclass__属性，python将会在类定义中寻找__metaclass__，如果找到了就用它来创建类，如果没有就用type来创建类。
"""
class Foo(Bar):
    pass
"""
# 上面的代码python将会这样做，首先python会在Foo中找__metaclass__，找到就用它来创建类对象，如果没有就会从父类Bar中找__metaclass__，如果在任何父类中都找不到__metaclass__，就会在模块层次中找__metaclass__，都找不到那就用内置的type来创建类对象。
# 因此我们可以在__metaclass__中写一些用于创建类的代码，什么可以创建类？那就是type，或者任何使用到type或子类化type的东西。


# 元类的主要目的就是在创建类的时候能够自动改变类。
# 举个例子，编写一个元类，让类的属性都改成大写形式。
# 元类会自动将你通常传给'type'的参数作为自己的参数传入
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    """
    返回一个将属性列表变为大写字母的类对象
    """

    # 选取所有不以'__'开头的属性，并把它们变成大写
    uppercase_attr = {}
    for name, val in future_class_attr.items():
        if not name.startswith('__'):
            uppercase_attr[name.upper()] = val
        else:
            uppercase_attr[name] = val

    # 用type创建类
    return type(future_class_name, future_class_parents, uppercase_attr)


class Foo(metaclass=upper_attr):
    # __metaclass__ = upper_attr 这是python2的写法
    bar = 'foo'


print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))
print(Foo().BAR)
print_line(50)


# type实际上是一个类，就像str和int一样，所以，你可以从type继承
class UpperAttrMetaclass(type):
    # __new__ 是在__init__之前被调用的特殊方法
    # __new__是用来创建对象并返回它的方法
    # 而__init__只是用来将传入的参数初始化给对象
    # 你很少用到__new__，除非你希望能够控制对象的创建
    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return type(future_class_name, future_class_parents, uppercase_attr)


# 但是这不是真正的面向对象(OOP)。我们直接调用了type，而且我们没有改写父类的new方法。
class UpperAttrMetaclass(type):

    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        # 重用 type.__new__ 方法
        # 这就是基本的OOP编程，没什么魔法
        return type.__new__(upperattr_metaclass, future_class_name,
                            future_class_parents, uppercase_attr)
        # 这里有个额外的参数upperattr_metaclass，类似于self，类方法的第一个参数总是代表当前实例。


# 为了便于理解上面的代码名字编的太长，实际产品中的代码应该是这样的
class UpperAttrMetaclass(type):

    def __new__(cls, clsname, bases, dct):

        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return type.__new__(cls, clsname, bases, uppercase_attr)


# 我们还可以使用super方法使代码变得更清晰一点
class UpperAttrMetaclass(type):

    def __new__(cls, clsname, bases, dct):

        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        # return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr) 这是python2的写法
        return super().__new__(cls, clsname, bases, uppercase_attr)


# 元类要做的事就是拦截类的创建，修改一个类，返回修改之后的类。
# 当你需要动态修改类的时候，最好使用“monkey patching”或“装饰器”。
