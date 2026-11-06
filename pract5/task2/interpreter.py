"""Интерпретатор УВМ, вариант 2 (стековая машина). Дамп памяти — CSV.

Память команд и данных объединена: программа загружается с адреса 0,
данные лежат в той же памяти по адресам после кода.

Запуск:
    python interpreter.py <программа.bin> <дамп.csv> <начало>:<конец>
Диапазон адресов включает обе границы, например 200:208.
"""

import argparse
import csv

from isa import decode

MEM_SIZE = 1024


def run(binary, mem_size=MEM_SIZE):
    if len(binary) > mem_size:
        raise MemoryError('Программа не помещается в память')
    mem = list(binary) + [0] * (mem_size - len(binary))
    stack = []

    def pop():
        if not stack:
            raise RuntimeError(f'Стек пуст (команда по адресу {pc_cmd})')
        return stack.pop()

    pc = 0
    while pc < len(binary):
        pc_cmd = pc
        name, f, size = decode(mem, pc)
        pc += size
        if name == 'load_const':
            stack.append(f['B'])
        elif name == 'read':
            stack.append(mem[f['B']])
        elif name == 'write':
            value = pop()
            addr = pop()
            mem[addr] = value
        elif name == 'pow':
            x = pop()
            base = pop()
            mem[base + f['B']] = x ** mem[base + f['C']]
    return mem, stack


def dump_csv(mem, start, end, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['address', 'value'])
        for addr in range(start, end + 1):
            w.writerow([addr, mem[addr]])


def parse_range(s):
    start, end = (int(x, 0) for x in s.split(':'))
    if not 0 <= start <= end < MEM_SIZE:
        raise argparse.ArgumentTypeError(f'диапазон должен быть в пределах 0:{MEM_SIZE - 1}')
    return start, end


def main():
    ap = argparse.ArgumentParser(description='Интерпретатор УВМ (вариант 2)')
    ap.add_argument('binary', help='путь к двоичному файлу программы')
    ap.add_argument('dump', help='путь к файлу дампа (CSV)')
    ap.add_argument('range', type=parse_range, help='диапазон адресов: начало:конец')
    a = ap.parse_args()

    with open(a.binary, 'rb') as f:
        mem, _ = run(f.read())
    dump_csv(mem, *a.range, a.dump)
    print(f'Дамп памяти {a.range[0]}..{a.range[1]} записан в {a.dump}')


if __name__ == '__main__':
    main()
