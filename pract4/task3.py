"""Задача 3. Кодирование в числа: 2 старшие цифры — код операции,
3 младшие — аргумент (opcode * 1000 + arg)."""

import sys

from task1 import read_source
from task2 import assemble

OPCODES = {'const': 0, 'get': 1, 'put': 2, 'ld': 3, 'st': 4, 'add': 5,
           'sub': 6, 'jpos': 7, 'jz': 8, 'j': 9, 'halt': 10}


def encode(code):
    result = []
    for op, arg in code:
        if not 0 <= arg <= 999:
            raise ValueError(f'Аргумент вне диапазона 0..999: {arg}')
        result.append(OPCODES[op] * 1000 + arg)
    return result


if __name__ == '__main__':
    print(encode(assemble(read_source(sys.argv))))
