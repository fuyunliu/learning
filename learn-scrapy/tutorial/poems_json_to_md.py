# -*- coding: utf-8 -*-
import json


template = """
### <font face="Consolas">{title}</font>
<font face="Consolas">
{content}
</font>

---
"""


def main():
    with open('poems.json', 'r') as fr:
        data = json.load(fr)
        data = sorted(data, key=lambda x: int(x['title']))
        with open('shakespeare_sonnets.md', 'a') as fw:
            for i in data:
                s = template.format(title=i['title'], content=i['content'])
                fw.write(s)


if __name__ == '__main__':
    main()
