"""
simple dispatcher
"""

import functools


class SnareDrum:
    """小鼓"""
    pass


class Cymbal:
    """铜钹"""
    pass


class Stick:
    """枯枝"""
    pass


class Brushes:
    """刷子"""
    pass


@functools.singledispatch
def play(instrument, accessory):
    """乐器和配件"""
    raise NotImplementedError("Cannot play these")


@play.register(SnareDrum)
@play.register(Cymbal)
def _(instrument, accessory):
    if isinstance(accessory, Stick):
        return "POC!"
    if isinstance(accessory, Brushes):
        return "SHHHH!"
    raise NotImplementedError("Cannot play these")


if __name__ == '__main__':
    print(play(SnareDrum(), Stick()))
    print(play(SnareDrum(), Brushes()))

    # 如果没有@play.register(Cymbal)，下面两行会出错。
    print(play(Cymbal(), Stick()))
    print(play(Cymbal(), Brushes()))
