"""Задача 5. Стековая машина: вычисление дискриминанта D = b*b - 4*a*c."""

stack = [0] * 16
sp = 0


def push(x):
    global sp
    stack[sp] = x
    sp += 1


def pop():
    global sp
    sp -= 1
    return stack[sp]


def add():
    push(pop() + pop())


def sub():
    b = pop()
    a = pop()
    push(a - b)          # порядок важен: a - b


def mul():
    push(pop() * pop())


def dup():
    x = pop()
    push(x)
    push(x)


def print_():
    print(pop())


def execute(code):
    for op, *args in code:
        op(*args)


def discriminant_code(a, b, c):
    return [
        (push, b),
        (dup,),          # b b
        (mul,),          # b*b
        (push, 4),
        (push, a),
        (mul,),          # b*b 4a
        (push, c),
        (mul,),          # b*b 4ac
        (sub,),          # b*b - 4ac
        (print_,),
    ]


if __name__ == '__main__':
    # x^2 - 5x + 6: D = 25 - 24 = 1
    execute(discriminant_code(1, -5, 6))
    # 2x^2 + 3x + 4: D = 9 - 32 = -23
    execute(discriminant_code(2, 3, 4))
