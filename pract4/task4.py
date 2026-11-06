"""Задача 4. Интерпретатор закодированного кода одноадресной машины.

Семантика команд (AWK Programming Language, разд. 6.1):
  get   acc <- ввод          put  вывод acc
  ld M  acc <- mem[M]        st M mem[M] <- acc
  add M acc += mem[M]        sub M acc -= mem[M]
  jpos M если acc > 0: pc <- M
  jz M   если acc == 0: pc <- M
  j M    pc <- M              halt  остановка
  const C — ячейка данных со значением C
"""

import sys

from task1 import read_source
from task2 import assemble
from task3 import encode, OPCODES

NAMES = {v: k for k, v in OPCODES.items()}


def run(mem, inp=None, out=None):
    inp = inp or (lambda: int(input('<- ')))
    out = out or (lambda x: print('->', x))
    mem = list(mem) + [0] * (1000 - len(mem))   # память на 1000 ячеек
    acc = pc = 0
    while True:
        op, addr = NAMES[mem[pc] // 1000], mem[pc] % 1000
        pc += 1
        if op == 'get':
            acc = inp()
        elif op == 'put':
            out(acc)
        elif op == 'ld':
            acc = mem[addr]
        elif op == 'st':
            mem[addr] = acc
        elif op == 'add':
            acc += mem[addr]
        elif op == 'sub':
            acc -= mem[addr]
        elif op == 'jpos':
            if acc > 0:
                pc = addr
        elif op == 'jz':
            if acc == 0:
                pc = addr
        elif op == 'j':
            pc = addr
        elif op == 'halt':
            return
        else:
            raise RuntimeError(f'Недопустимая команда {mem[pc - 1]} по адресу {pc - 1}')


if __name__ == '__main__':
    run(encode(assemble(read_source(sys.argv))))
