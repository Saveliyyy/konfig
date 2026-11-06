"""Интерпретатор УВМ, вариант 3 (аккумуляторная машина). Дамп памяти — JSON.

Память команд и данных объединена: программа загружается с адреса 0,
данные лежат в той же памяти по адресам после кода.

Запуск:
    python interpreter.py <программа.bin> <дамп.json> <начало>:<конец>
Диапазон адресов включает обе границы, например 200:204.
"""

import argparse
import json

from isa import decode

MEM_SIZE = 1024


def sgn(x):
    return (x > 0) - (x < 0)


def run(binary, mem_size=MEM_SIZE):
    if len(binary) > mem_size:
        raise MemoryError('Программа не помещается в память')
    mem = list(binary) + [0] * (mem_size - len(binary))
    acc = 0
    pc = 0
    while pc < len(binary):
        name, f, size = decode(mem, pc)
        pc += size
        if name == 'load_const':
            acc = f['B']
        elif name == 'read':
            acc = mem[acc + f['B']]
        elif name == 'write':
            mem[f['B']] = acc
        elif name == 'sgn':
            acc = sgn(mem[f['B']])
    return mem, acc


def dump_json(mem, start, end, path):
    data = {'start': start, 'end': end,
            'memory': [{'address': a, 'value': mem[a]} for a in range(start, end + 1)]}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_range(s):
    start, end = (int(x, 0) for x in s.split(':'))
    if not 0 <= start <= end < MEM_SIZE:
        raise argparse.ArgumentTypeError(f'диапазон должен быть в пределах 0:{MEM_SIZE - 1}')
    return start, end


def main():
    ap = argparse.ArgumentParser(description='Интерпретатор УВМ (вариант 3)')
    ap.add_argument('binary', help='путь к двоичному файлу программы')
    ap.add_argument('dump', help='путь к файлу дампа (JSON)')
    ap.add_argument('range', type=parse_range, help='диапазон адресов: начало:конец')
    a = ap.parse_args()

    with open(a.binary, 'rb') as f:
        mem, _ = run(f.read())
    dump_json(mem, *a.range, a.dump)
    print(f'Дамп памяти {a.range[0]}..{a.range[1]} записан в {a.dump}')


if __name__ == '__main__':
    main()
