"""Задача 6. Стековая машина, достаточная для примера из задачи 1
(сумма вводимых чисел до нуля).

Добавлены: память (load/store), ввод/вывод (get/put), переходы (j/jz),
остановка (halt) и счётчик команд pc вместо простого цикла for.
"""

stack = [0] * 16
sp = 0
mem = [0] * 16
pc = 0
running = False


# --- стек ---
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
    push(pop() - b)


def mul():
    push(pop() * pop())


def dup():
    x = pop()
    push(x)
    push(x)


def drop():
    pop()


# --- память ---
def load(addr):
    push(mem[addr])


def store(addr):
    mem[addr] = pop()


# --- ввод/вывод ---
def get():
    push(int(input('<- ')))


def put():
    print('->', pop())


# --- управление ---
def j(addr):
    global pc
    pc = addr


def jz(addr):
    if pop() == 0:
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
    global pc, running, sp
    pc, sp, running = 0, 0, True
    while running:
        op, *args = code[pc]
        pc += 1
        op(*args)


SUM = 0   # адрес переменной sum

sum_code = resolve([
    (push, 0),
    (store, SUM),       # sum = 0
    'loop:',
    (get,),             # x
    (dup,),             # x x
    (jz, 'done'),       # x       (если x == 0 — на выход)
    (load, SUM),        # x sum
    (add,),             # x+sum
    (store, SUM),       # sum = x + sum
    (j, 'loop'),
    'done:',
    (drop,),            # убрать оставшийся 0
    (load, SUM),
    (put,),
    (halt,),
])

if __name__ == '__main__':
    execute(sum_code)
