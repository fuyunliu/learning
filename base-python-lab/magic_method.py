"""Python 魔法方法指南"""
#
# __new__(cls, *, **)方法是对象实例化时调用的第一个方法，
# 第一个参数是类本身，其他参数将全部传递给__init__方法。
#
# __init__(self, *, **)方法为类的初始化方法，当构造函数被调用时任何参数将会传递给它。
# 比如x = MyClass(10, 'foo')，那么__init__将会得到两个参数10和‘foo’。
#
# __del__(self)方法是当一个对象进行垃圾回收时执行一些清理操作。如套接字对象和文件对象。
# 注意del x不会调用x.__del__()，前者只是减少一个x的引用，后者是当x的引用为零时调用。
#


import os


class FileObject:
    """给文件对象进行包装从而确认在删除时文件流关闭"""

    def __init__(self, filepath, filename):
        self.file = open(os.path.join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file


# __repr__(self) 由repr()函数调用，返回值必须是字符串对象。
# 如果可能，这应该是一个有效的python表达式，
# 或者类似<...some useful description...>形式的字符串。
# 如果一个类定义了__repr__()但是没有定义__str__()，那么请求该类的“非正式”字符串表示时
# 将调用__repr__()。
#
# __str__(self) 由str(object)，format()和print()调用，返回值必须是字符串。
#
# __bytes(self) 由bytes()调用，用来计算一个对象的字节字符串表示形式，返回bytes对象。
#
# __format__(self, format_spec) 由format()和str.format()方法调用，返回字符串对象。
#
# __lt__(self, other) 小于，x < y 时调用。
#
# __le__(self, other) 小于等于， x <= y 时调用。
#
# __eq__(self, other) 等于， x == y 时调用。
#
# __ne__(self, other) 不等于， x != y 时调用。
#
# __gt__(self, other) 大于， x > y 时调用。
#
# __ge__(self, other) 大于等于， x >= y 时调用。
#
# __bool__(self, other) 布尔上上下文环境中的真值， if x 调用。
#
# __hash__(self) 自定义散列值，由hash()函数调用。
#
# __getattr__(self, name) 当属性通过正常的机制没有找到时调用该方法，返回计算后的属性
# 或者抛出AttributeError异常。
#
# __getattribute__(self, name) 无条件地调用以获取实例属性，返回计算后的属性或者抛出
# AttributeError异常。
#
# __setattr__(self, name, value) 设置属性的值。
#
# __delattr__(self, name) 删除某个属性。
#
# __dir__(self) 在对象上调用dir()方法，列出对象的所有属性和方法。
#


class Dynamo:
    """比较__getattr__和__getattribute__的区别"""

    def __getattr__(self, name):
        if name == 'color':
            return 'PapayaWhip'
        else:
            raise AttributeError


class SuperDynamo:
    """比较__getattr__和__getattribute__的区别"""

    def __getattribute__(self, name):
        if name == 'color':
            return 'PapayaWhip'
        else:
            raise AttributeError


dyn = SuperDynamo()  # 改为dyn = SuperDynamo()看看区别
print(dyn.color)
dyn.color = 'LemonChiffon'
print(dyn.color)
print()


class Rastan:
    """查找类方法名称时也将调用__getattribute__"""

    def __getattribute__(self, name):
        raise AttributeError
        # return object.__getattribute__(self, name)

    def swim(self):
        pass


hero = Rastan()
try:
    hero.swim()  # 这将引发AttributeError异常
except AttributeError:
    print("hero has no attribute swim")
    print()

#
# __get__(self, instance, owner)
#
# __set__(self, instance, value)
#
# __delete__(self, instance)
#
# __set_name__(self, owner, name)
#
# __slots__ 只定义特定集合的某些属性。
#


class Object:
    """只能定义x和y属性"""
    __slots__ = {"x", "y"}


obj = Object()
obj.x = 1
obj.y = 2
# obj.z = 3  抛出AttributeError错误
#
# __init_subclass__(cls)
#


class Philosopher:
    def __init_subclass__(cls, default_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.default_name = default_name


class AustralianPhilosopher(Philosopher, default_name="Bruce"):
    pass


#
# __instancecheck__(self, instance) isinstance(instance, class)调用。
# 判断对象是否为某个类的实例。
#
# __subclasscheck__(self, subclass) issubclass(subclass, class)调用。
# 判断类是否为某个类的子类。
#
# __call__(self, *, **) 像调用函数一样调用一个实例。
#
# __len__(self) 返回对象的长度，len()函数调用。
#
# __length_hint__(self) 返回对象的预估长度，operator.length_hint()调用。
#
# __getitem__(self, key) 通过键来获取值，x[key]，key不存在将引发KeyError。
#
# __setitem__(self, key, value) 通过键来设置值，x[key] = value。
#
# __delitem__(self, key) 删除某个键值对，del x[key]。
#
# __missing__(self, key) 为缺失的键提供默认值，x[key]。
#
# __iter__(self) 遍历某个序列，iter(seq)。
#
# __reversed__(self) 反向迭代某个序列，reversed(seq)。
#
# __next__(self) 从迭代器中获取下一个值，next(seq)。
#
# __contains__(self) 成员测试，x in seq。
#
###############################################################################
#
# __add__(self, other) 加法，x + y。
#
# __sub__(self, other) 减法，x - y。
#
# __mul__(self, other) 乘法，x * y。
#
# __matmul__(self, other) 矩阵乘法，符号为@，不是python内建的运算符。
#
# __truediv__(self, other) 除法， x / y。
#
# __floordiv__(self, other) 地板除，x // y。
#
# __mod__(self, other) 取余，x % y。
#
# __divmod__(self, other) 地板除+取余，divmod(x, y)。
#
# __pow__(self, other, [, modulo]) 乘幂， x ** y 或者 x ** y % z
# 应支持可选的第三个参数。
#
# __lshift__(self, other) 左位移 x << y
#
# __rshift__(self, other) 右位移 x >> y
#
# __and__(self, other) 按位 and x & y
#
# __xor__(self, other) 按位 xor x ^ y
#
# __or__(self, other) 按位 or x | y
#
###############################################################################
#
# __radd__(self, other) 加法，x + y。
#
# __rsub__(self, other) 减法，x - y。
#
# __mul__(self, other) 乘法，x * y。
#
# __rmatmul__(self, other) 矩阵乘法，符号为@，不是python内建的运算符。
#
# __rtruediv__(self, other) 除法， x / y。
#
# __rfloordiv__(self, other) 地板除，x // y。
#
# __rmod__(self, other) 取余，x % y。
#
# __rdivmod__(self, other) 地板除+取余，divmod(x, y)。
#
# __rpow__(self, other, [, modulo]) 乘幂， x ** y 或者 x ** y % z
# 应支持可选的第三个参数。
#
# __rlshift__(self, other) 左位移 x << y
#
# __rrshift__(self, other) 右位移 x >> y
#
# __rand__(self, other) 按位 and x & y
#
# __rxor__(self, other) 按位 xor x ^ y
#
# __ror__(self, other) 按位 or x | y
#
###############################################################################
#
# __iadd__(self, other) 原地加法，x += y。
#
# __isub__(self, other) 原地减法，x -= y。
#
# __imul__(self, other) 原地乘法，x *= y。
#
# __imatmul__(self, other) 原地矩阵乘法，符号为@，不是python内建的运算符。
#
# __itruediv__(self, other) 原地除法， x /= y。
#
# __ifloordiv__(self, other) 原地地板除，x //= y。
#
# __imod__(self, other) 原地取余，x %= y。
#
# __ipow__(self, other, [, modulo]) 原地乘幂， x **= y 或者 x ** y % z
# 应支持可选的第三个参数。
#
# __ilshift__(self, other) 原地左位移 x <<= y
#
# __irshift__(self, other) 原地右位移 x >>= y
#
# __iand__(self, other) 原地按位 and x &= y
#
# __ixor__(self, other) 原地按位 xor x ^= y
#
# __ior__(self, other) 原地按位 or x |= y
#
###############################################################################
#
# __neg__(self) 负数，-x
#
# __pos__(self) 正数，+x
#
# __abs__(self) 绝对值，abs(x)
#
# __invert__(self) 取反，~x
#
# __complex__(self) 复数，complex(x)
#
# __int__(self) 整数转换，int(x)
#
# __float__(self) 浮点数，float(x)
#
# __round__(self, [, n]) 四舍五入，round(x)，round(x, n)
# 可选的第三个参数为保留n位小数。
#
# __ceil__(self) 向上取整，math.ceil(x)
#
# __floor__(self) 向下取整，math.floor(x)
#
# __trunc__(self) 对x朝向0取整，math.trunc(x)
#
# __index__(self) 作为列表索引的数字，a_list[x]
#
###############################################################################
#
# __copy__(self) 自定义对象的复制，copy.copy(x)
#
# __deepcopy__(self) 自定义对象的深度复制，copy.deepcopy(x)
#
# __getstate(self) 在pickling之前获取对象的状态，pickle.dump(x, file)
#
# __reduce__(self) 序列化某对象，pickle.dump(x, file)
#
# __reduce_ex__(self, ) 序列化某对象（新 pickling 协议），
# pickle.dump(x, file, protocol_version)
#
# __getnewargs__(self) 控制 unpickling 过程中对象的创建方式，x = pickle.load(file)
#
# __setstate__(self) 在 unpickling 之后还原对象的状态，x = pickle.load(file)
#
###############################################################################
#
# with语句上下文管理器
#
# __enter__(self) 在进入 with 语块时进行一些特别操作，with x:
#
# __exit__(self, exc_type, exc_value, traceback)
# 在退出 with 语块时进行一些特别操作，with x:
#
###############################################################################
#
# 协程
# __await__(self)
# 必须返回一个迭代器。应该用于实现awaitable的对象。
# 例如，asyncio.Future实现此方法以与await表达式兼容。
#
#
# 异步迭代器
# __aiter__(self) 必须返回一个异步迭代器对象。
#
# __anext__(self) 必须返回一个awaitable，来生成迭代器的下一个值。
# 当迭代结束的时候，应该引发一个StopAsyncIteration错误。
#


class Reader:
    """异步可迭代对象的一个示例"""
    async def readline(self):
        pass

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == b'':
            raise StopAsyncIteration
        return val


#
# 异步上下文管理器
# __aenter__(self)
# 这种方法在语义上类似于__enter__()，仅有的差异是它必须返回一个awaitable对象。
#
# __aexit__(self)
# 这个方法在语义上类似于__exit__()，仅有的差异是它必须返回一个awaitable对象。
#


class AsyncContextManager:
    """异步上下文管理类的示例"""
    async def __aenter__(self):
        await print("entering context")

    async def __aexit__(self, exc_type, exc_value, traceback):
        await print("exiting context")
