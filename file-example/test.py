# 向文件追加内容
with open("test.txt", "at") as f:
    f.write("appended text")

# 按行读取文件内容并保存到数组
with open('test.txt', 'rt') as f:
    content = [line.rstrip('\n') for line in f]
