"""Python算法实战系列之栈

栈(stack)又称之为堆栈是一个特殊的有序表，其插入和删除操作都在栈顶进行操作，并且按照先进后出，后进先出的规则进行运作。

原文出处：http://python.jobbole.com/87581/
"""

# 三种括号()[]{}以任意顺序嵌套，编写一个函数判断字符串括号匹配是否正确
LEFT = {'(', '[', '{'}
RIGHT = {')', ']', '}'}


def match(expr):
    """判断表达式字符串括号是否匹配

    Args:
        expr: 表达式字符串

    Returns:
        bool
    """
    stack = []  # 创建一个空栈
    for bracket in expr:
        if bracket in LEFT:
            stack.append(bracket)  # 遇左括号入栈
        elif bracket in RIGHT:
            if not stack or not 1 <= ord(bracket) - ord(stack[-1]) <= 2:
                # 栈为空或者右括号减去左括号的值不是1或者2
                return False
            stack.pop()  # 右括号匹配到左括号，出栈一个左括号
    return not stack


if __name__ == '__main__':
    expr = '[(){()}]'
    print(match(expr))
