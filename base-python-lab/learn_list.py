# -*- coding: utf-8 -*-
"收集列表操作方法"


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# pprint.pprint(list(chunks([{},{},{},{},{},{},{},{},{},{},{},{},{}], 2)))
for i in list(chunks([{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], 2)):
    print(i)


# 对字典进行切片
def dict_slice(d, start, end):
    keys = list(d.keys())
    new_dict = {k: v for k, v in d.items() if k in keys[start:end]}
    del d, keys
    return new_dict


a = dict_slice({'a': 1, 'b': 2, 'c': 3, 'd': 4}, 2, 3)
print(a)


# 对字典进行排序是不可能的，只能将字典转化为另一种有序的表述，如列表、元组
import operator
x = {'a': 1, 'b': 1, 'c': 3, 'd': 4, 'c': 5}
# 按字典的value进行排序，注意得到的sorted_x是列表
sorted_x1 = sorted(x.items(), key=operator.itemgetter(1))
# 按字典的key进行排序，注意得到的sorted_x是列表
sorted_x2 = sorted(x.items(), key=operator.itemgetter(0))
# 可以将得到的有序列表转化为OrderedDict，这样得到的字典比一般字典大2倍
from collections import OrderedDict
order_dict = OrderedDict(sorted_x1) or OrderedDict(sorted_x2)
