# -*- coding: utf-8 -*-

print_line = lambda x: print('*' * x)


# 在python中函数也是对象，举个例子
def shout(word='yes'):
    return word.capitalize() + '!'


print(shout())
# 你还可以把函数赋给一个变量
scream = shout
print(scream())
# 你可以删除旧的函数名，而scream依然可以用
del shout
try:
    print(shout())
except NameError as e:
    print(e)
print(scream())
print_line(50)


# python的另一个有趣的特性就是你可以在一个函数里定义另一个函数
def talk():

    # 定义另一个函数
    def whisper(word='yes'):
        return word.lower() + '...'

    # 现在调用它
    print(whisper())


# 每次调用talk时都会定义一次whisper，然后talk会调用whisper
talk()
# 但是在talk之外whisper是不存在的
try:
    print(whisper())
except NameError as e:
    print(e)
# 总结：函数是对象，可以赋给一个变量，可以在函数里面定义，因此函数可以返回另一个函数
print_line(50)


def get_talk(kind='shout'):

    # 先定义两个函数
    def shout(word='yes'):
        return word.capitalize() + '!'

    def whisper(word='yes'):
        return word.lower() + '...'

    # 根据传入的参数返回不同的函数对象
    if kind == 'shout':
        return shout
    else:
        return whisper


# 把函数值赋给变量
talk = get_talk()
# 可以看出函数值是一个函数对象
print(talk)
# 再看看函数对象返回的对象
print(talk())
# 你还可以这么用
print(get_talk('whisper')())
print_line(50)


# 既然可以return一个函数，那么把函数作为参数传递好了
def do_something_before(func):
    print("I do something before then I call the function you gave me")
    print(func())


do_something_before(scream)
print_line(50)
# 装饰器就是在函数执行之前或之后执行另一些代码而不用修改函数


# 装饰器就是把其他函数作为参数的函数，然后返回一个函数的函数
def my_shiny_new_decorator(a_function_to_decorate):

    # 在函数里面，装饰器在运行中定义函数: 包装器
    # 这个函数将被包装在原始函数的外面，所以可以在原始函数之前和之后执行其他代码
    def the_wrapper_around_the_original_function():

        # 把要在原始函数被调用前执行的代码放在这里
        print("Before the function runs")

        # 调用原始函数
        a_function_to_decorate()

        # 把要在原始函数调用后执行的代码放在这里
        print("After the function runs")

    # 在这里a_function_to_decorate函数还没有被执行
    # 在这里返回刚刚包装过的函数
    # 在包装函数里包含要在原始函数前后执行的代码
    return the_wrapper_around_the_original_function


# 现在假想一下你创建了一个永远也不想去修改的函数
def a_stand_alone_function():
    print("I am a stand alone function, don't you dare modify me!")


# 先尝试运行一下这个永不修改的函数
a_stand_alone_function()
print()
# 现在你可以装饰器来增加它的功能，把它作为参数传递给装饰器，装饰器会返回一个被包装过的函数，
a_stand_alone_function_decorated = my_shiny_new_decorator(
    a_stand_alone_function)
a_stand_alone_function_decorated()
print()
# 现在你想要每次都是用a_stand_alone_function_decorated来代替a_stand_alone_function
a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function()
# 函数名字改变了，变成了装饰器返回的那个函数的名字
print(a_stand_alone_function.__name__)
print_line(50)


# 接下来看看装饰器的语法
@my_shiny_new_decorator
def another_stand_alone_function():
    print("Leave me alone!")


# @my_shiny_new_decorator就是another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)的缩写
another_stand_alone_function()
# 但是这个函数的名字也改变了
print(another_stand_alone_function.__name__)
print_line(50)


# 当然你也可以自己写一个装饰器
def bread(func):
    def wrapper():
        print("</''''''\>")
        func()
        print("<\______/>")
    return wrapper


def ingredients(func):
    def wrapper():
        print("#tomatoes#")
        func()
        print("~salad~")
    return wrapper


def sandwich(food="--ham--"):
    print(food)


# 现在来做两个不同的三明治
one_sandwich = bread(ingredients(sandwich))
one_sandwich()
print()
two_sandwich = ingredients(bread(sandwich))
two_sandwich()
print()


# 或者用装饰器语法糖做三明治
@bread
@ingredients
def sandwich_a(food="--ham--"):
    print(food)


# 改变一下顺序看看如何
@ingredients
@bread
def sandwich_b(food="--ham--"):
    print(food)


sandwich_a()
print()
sandwich_b()
print_line(50)


# 粗体装饰器
def makebold(fn):
    # 装饰器将返回新的函数
    def wrapper():
        # 在之前或者之后插入新的代码
        return "<b>" + fn() + "</b>"
    return wrapper


# 斜体装饰器
def makeitalic(fn):
    # 装饰器将返回新的函数
    def wrapper():
        # 在之前或者之后插入新的代码
        return "<i>" + fn() + "</i>"
    return wrapper


@makebold
@makeitalic
def say():
    return "hello"


print(say())


# 这相当于
def say():
    return "hello"


say = makebold(makeitalic(say))
print(say())
print_line(50)


# 在装饰器函数里传入参数
def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print("I got args! Look:", arg1, arg2)
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments


# 当你调用装饰器返回的函数时，也就调用了包装器，把参数传入包装器里，包装器再把参数传递给被装饰的函数
@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print("My name is", first_name, last_name)


print_full_name("fuyun", "Liu")
print_line(50)


# 用装饰器装饰类方法也是一样的，唯一的区别就是类方法的第一个参数是self，代表实例对象
def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        lie = lie - 3
        return method_to_decorate(self, lie)
    return wrapper


class Lucy(object):

    def __init__(self):
        self.age = 32

    @method_friendly_decorator
    def say_your_age(self, lie):
        print("I am %s, what did you think?" % (self.age + lie))


l = Lucy()
l.say_your_age(-3)
print_line(50)


# 如果你想造一个更通用的可以同时满足方法和函数的装饰器，用*args，**kwargs就可以了
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # 包装器接受所有参数
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print("Do I have args?:")
        print(args)
        print(kwargs)
        # args是个列表，kwargs是个字典
        # 这里可以把args和kwargs解包并对其处理
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments


@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print("Python is cool, no argument here.")


function_with_no_argument()
print()


@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print(a, b, c)


function_with_arguments(1, 2, 3)
print()


@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus="Why not ?"):
    print("Do %s, %s and %s like platypus? %s" % (a, b, c, platypus))


function_with_named_arguments("Bill", "Linus", "Steve", platypus="Indeed!")
print()


class Mary(object):

    def __init__(self):
        self.age = 31

    @a_decorator_passing_arbitrary_arguments
    def say_your_age(self, lie=-3):  # 可以加入一个默认值
        print("I am %s, what did you think?" % (self.age + lie))


m = Mary()
m.say_your_age(lie=-5)  # 这里又覆盖了默认值，可以变换着看一下
print_line(50)


# 像上面的把参数传给被装饰器返回的函数，实际上就是被定义在装饰器内部的包装器接收了。
# 那如何给装饰器传参数呢？再来回顾一下装饰器的用法
def my_decorator(func):
    print("I am an ordinary function")

    def wrapper():
        print("I am function returned by the decorator")
        func()
    return wrapper


def lazy_function():
    print("zzzzzzzz")


# 装饰函数的过程其实调用了装饰器函数，下面这句有打印信息。
decorated_function = my_decorator(lazy_function)


# 这样也是，输出"I am an ordinary function"
@my_decorator
def lazy_function():
    print("zzzzzzzz")


print_line(50)


# 再用一层函数包装装饰器，我们就可以传参数给装饰器了，类似闭包，动态返回装饰器。
def decorator_maker():

    print("I make decorators! I am executed only once: " +
          "when you make me create a decorator.")

    def my_decorator(func):

        print("I am a decorator! I am executed only when you decorate a function.")

        def wrapped():
            print("I am the wrapper around the decorated function. "
                  "I am called when you call the decorated function. "
                  "As the wrapper, I return the RESULT of the decorated function.")
            return func()

        print("As the decorator, I return the wrapped function.")

        return wrapped

    print("As a decorator maker, I return a decorator")
    return my_decorator


# 用函数创建一个装饰器
new_decorator = decorator_maker()
print()


def decorated_function():
    print("I am the decorated function.")


# 用刚刚创建的装饰器装饰函数
decorated_function = new_decorator(decorated_function)
print()
# 执行被装饰过的函数
decorated_function()
print_line(50)
# 用一行代码概括上面的
decorator_maker()(decorated_function)()
print_line(50)


# 用@语法糖简化
@decorator_maker()
def decorated_function():
    print("I am the decorated function.")


# 执行一下
decorated_function()
print_line(50)


# 现在来写一个带参数的装饰器生成函数
def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):

    print("I make decorators! And I accept arguments:", decorator_arg1, decorator_arg2)

    def my_decorator(func):
        # 这里传参的能力借鉴了闭包
        # 参考 http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
        print("I am the decorator. Somehow you passed me arguments:", decorator_arg1, decorator_arg2)

        # 不要忘了装饰器参数和函数参数
        def wrapped(function_arg1, function_arg2):
            print("I am the wrapper around the decorated function.\n"
                  "I can access all the variables\n"
                  "\t- from the decorator: {0} {1}\n"
                  "\t- from the function call: {2} {3}\n"
                  "Then I can pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator


@decorator_maker_with_arguments("Leonard", "Sheldon")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print("I am the decorated function and only knows about my arguments: {0}"
          " {1}".format(function_arg1, function_arg2))


decorated_function_with_arguments("Rajesh", "Howard")
print_line(50)


# 参数还可以设置成变量
c1 = "Penny"
c2 = "Leslie"


@decorator_maker_with_arguments("Leonard", c1)
def decorated_function_with_arguments(function_arg1, function_arg2):
    print("I am the decorated function and only knows about my arguments:"
          " {0} {1}".format(function_arg1, function_arg2))


decorated_function_with_arguments(c2, "Howard")
print_line(50)


# 最后神奇的一招，如何装饰一个装饰器，动态地返回一个可以带任意参数的装饰器。
def decorator_with_args(decorator_to_enhance):
    """
    这个函数接收一个装饰器作为参数，返回一个被装饰的装饰器
    这没什么高深，只不过是为了给装饰器传参而已
    """

    def decorator_maker(*args, **kwargs):

        # 我们动态地建立一个只接收一个函数的装饰器
        # 但是他能接收来自maker的参数
        def decorator_wrapper(func):

            # 最后我们返回原始的装饰器，毕竟它只是普通的函数
            # 唯一的陷阱：装饰器必须有这个特殊的，否则将不会奏效
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper

    return decorator_maker


# 把装饰器语法糖加到装饰器上面，注意这个装饰器是用来装饰函数的
@decorator_with_args
def decorated_decorator(func, *args, **kwargs):
    def wrapper(function_arg1, function_arg2):
        print("Decorated with", args, kwargs)
        return func(function_arg1, function_arg2)
    return wrapper


# 现在用被装饰过的装饰器装饰你的函数
@decorated_decorator(1, 2, 3, a=1, b=2, c=3)
def decorated_function(function_arg1, function_arg2):
    print("Hello", function_arg1, function_arg2)


# 调用被装饰器装饰过的函数
decorated_function("world,", "Awesome!")
print_line(50)


# 是不是被绕晕了，来看看终极调用过程
# 首先这是一个普通的装饰器
def normal_decorator(func, *args, **kwargs):
    def wrapper(function_arg1, function_arg2):
        print("Normal decorator decorated with", args, kwargs)
        return func(function_arg1, function_arg2)
    return wrapper


# 这是一个普通的函数
def normal_function(function_arg1, function_arg2):
    print("Hello", function_arg1, function_arg2)


# 终极变态调用过程如下
decorator_with_args(normal_decorator)(1, 2, 3, a=1, b=2, c=3)(normal_function)('world,', 'Awesome!')
print_line(50)


# 现在来关注一个小问题，被装饰器装饰的函数的名字__name__改变了。
# 幸好我们有functools.wraps()函数，它可以复制函数的名字，模块和文档给它的包装器。
def foo():
    print("foo")


print(foo.__name__)


def bar(func):
    def wrapper():
        print("bar")
        return func()
    return wrapper


@bar
def foo():
    print("foo")


print(foo.__name__)


# 下面用functools.wraps()来修复
import functools
def bar(func):
    @functools.wraps(func)
    def wrapper():
        print("bar")
        return func()
    return wrapper


@bar
def foo():
    print("foo")


print(foo.__name__)
print_line(50)


# 如何使用装饰器
def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time

    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__, time.clock() - t)
        return res
    return wrapper


def logging(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(func.__name__, args, kwargs)
        return res
    return wrapper


def counter(func):
    """
    A decorator that counts and prints the number of times a function has been executed
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print("{0} has been used: {1}x".format(func.__name__, wrapper.count))
        return res
    wrapper.count = 0
    return wrapper


@counter
@benchmark
@logging
def reverse_string(string):
    return str(reversed(string))


print(reverse_string("Able was I ere I saw Elba"))
print(reverse_string("A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!"))
print_line(50)


# 不用重写装饰器而可以用他们来做任何事
@counter
@benchmark
@logging
def get_html_text():
    import requests
    import pprint
    try:
        r = requests.get("http://httpbin.org/html")
        pprint.pprint(r.text)
    except:
        return "I got nothing!"


get_html_text()
get_html_text()
