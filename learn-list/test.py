# -*- coding: utf-8 -*-
"""收集列表操作方法"""

import pprint


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# pprint.pprint(list(chunks([{},{},{},{},{},{},{},{},{},{},{},{},{}], 2)))

for i in list(chunks([{},{},{},{},{},{},{},{},{},{},{},{},{}], 2)):
    print(i)
