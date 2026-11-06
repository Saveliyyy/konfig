"""Задача 8. Регистровая машина, достаточная для примера из задачи 1
(сумма вводимых чисел до нуля).

Добавлены: get/put (ввод/вывод регистра), j/jz (переходы), halt
и счётчик команд pc.
"""

regs = [0] * 16
pc = 0
running = False


def move(r, x):
    regs[r] = x


def add(rd, rs1, rs2):
    regs[rd] = regs[rs1] + regs[rs2]


def sub(rd, rs1, rs2):
    regs[rd] = regs[rs1] - regs[rs2]


def mul(rd, rs1, rs2):
    regs[rd] = regs[rs1] * regs[rs2]


def get(r):
    regs[r] = int(input('<- '))


def put(r):
    print('->', regs[r])


def j(addr):
    global pc
    pc = addr


def jz(r, addr):
    if regs[r] == 0:
        j(addr)


def halt():
    global running
    running = False


def resolve(code):
    """Строки вида 'имя:' — метки; аргументы-строки заменяются адресами."""
    labels, body = {}, []
    for item in code:
        if isinstance(item, str):
            labels[item.rstrip(':')] = len(body)
        else:
            body.append(item)
    return [(op, *[labels.get(a, a) if isinstance(a, str) else a for a in args])
            for op, *args in body]


def execute(code):
    global pc, running
    pc, running = 0, True
    while running:
        op, *args = code[pc]
        pc += 1
        op(*args)


sum_code = resolve([
    (move, 0, 0),        # r0 = sum = 0
    'loop:',
    (get, 1),            # r1 = ввод
    (jz, 1, 'done'),     # если r1 == 0 — выход
    (add, 0, 0, 1),      # sum += r1
    (j, 'loop'),
    'done:',
    (put, 0),
    (halt,),
])

if __name__ == '__main__':
    execute(sum_code)
