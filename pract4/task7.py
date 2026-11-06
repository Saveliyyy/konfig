"""Задача 7. Регистровая машина: вычисление дискриминанта D = b*b - 4*a*c."""

regs = [0] * 16


def move(r, x):
    regs[r] = x


def add(rd, rs1, rs2):
    regs[rd] = regs[rs1] + regs[rs2]


def sub(rd, rs1, rs2):
    regs[rd] = regs[rs1] - regs[rs2]


def mul(rd, rs1, rs2):
    regs[rd] = regs[rs1] * regs[rs2]


def print_(r):
    print(regs[r])


def execute(code):
    for op, *args in code:
        op(*args)


def discriminant_code(a, b, c):
    return [
        (move, 0, a),       # r0 = a
        (move, 1, b),       # r1 = b
        (move, 2, c),       # r2 = c
        (move, 3, 4),       # r3 = 4
        (mul, 4, 1, 1),     # r4 = b*b
        (mul, 5, 3, 0),     # r5 = 4*a
        (mul, 5, 5, 2),     # r5 = 4*a*c
        (sub, 6, 4, 5),     # r6 = b*b - 4ac
        (print_, 6),
    ]


if __name__ == '__main__':
    execute(discriminant_code(1, -5, 6))    # 1
    execute(discriminant_code(2, 3, 4))     # -23
