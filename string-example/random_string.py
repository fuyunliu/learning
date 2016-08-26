# -*- coding: utf-8 -*-
"""随机生成6位字符串，只包含字母和数字"""

import random
import string


# Answer in one line
''.join(random.choice(string.ascii_uppercase + string.digits)
        for _ in range(6))

# A more secure version
''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(6))
