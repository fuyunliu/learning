# -*- coding: utf-8 -*-

import os
import pathlib


# 判断文件是否存在，pathlib.Path是面向对象的实现
my_file = pathlib.Path('/path/to/file')
print(my_file.is_file())

# 也可以用os模块
print(os.path.isfile('/path/to/file'))

# 向文件追加内容
with open('test1.txt', 'at') as f:
    f.write('appended text')

# 按行读取文件内容并保存到数组
with open('test1.txt', 'rt') as f:
    content = [line.rstrip('\n') for line in f]

# 用一个with语句打开多个文件
with open('test1.txt', 'r') as f1, open('test2.txt', 'w') as f2:
    f2.write(f1.read())

# 打开大文件，使用这种方式会像生成器那样对待文件
with open('test1.txt', 'rt') as f:
    for line in f:
        pass  # do something with line


base_dir = pathlib.Path(__file__).parent
print(base_dir / 'test.txt')
