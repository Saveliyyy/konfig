"""Интерпретатор УВМ, вариант 1. Дамп памяти — XML.

Память команд и данных объединена: программа загружается с адреса 0,
данные лежат в той же памяти по адресам после кода.
Регистров 128 (номер задаётся 7 битами).

Запуск:
    python interpreter.py <программа.bin> <дамп.xml> <начало>:<конец>
Диапазон адресов включает обе границы, например 300:315.
"""

import argparse
import xml.etree.ElementTree as ET

from isa import decode

MEM_SIZE = 1024
REG_COUNT = 128


def run(binary, mem_size=MEM_SIZE):
    if len(binary) > mem_size:
        raise MemoryError('Программа не помещается в память')
    mem = list(binary) + [0] * (mem_size - len(binary))
    reg = [0] * REG_COUNT
    pc = 0
    while pc < len(binary):
        name, f, size = decode(mem, pc)
        pc += size
        if name == 'load_const':
            reg[f['B']] = f['C']
        elif name == 'read':
            reg[f['B']] = mem[reg[f['C']]]
        elif name == 'write':
            mem[reg[f['C']] + f['B']] = reg[f['D']]
        elif name == 'abs':
            mem[reg[f['B']]] = abs(reg[f['C']])
    return mem, reg


def dump_xml(mem, start, end, path):
    root = ET.Element('memory', start=str(start), end=str(end))
    for addr in range(start, end + 1):
        ET.SubElement(root, 'cell', address=str(addr)).text = str(mem[addr])
    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write(path, encoding='utf-8', xml_declaration=True)


def parse_range(s):
    start, end = (int(x, 0) for x in s.split(':'))
    if not 0 <= start <= end < MEM_SIZE:
        raise argparse.ArgumentTypeError(f'диапазон должен быть в пределах 0:{MEM_SIZE - 1}')
    return start, end


def main():
    ap = argparse.ArgumentParser(description='Интерпретатор УВМ (вариант 1)')
    ap.add_argument('binary', help='путь к двоичному файлу программы')
    ap.add_argument('dump', help='путь к файлу дампа (XML)')
    ap.add_argument('range', type=parse_range, help='диапазон адресов: начало:конец')
    a = ap.parse_args()

    with open(a.binary, 'rb') as f:
        mem, _ = run(f.read())
    dump_xml(mem, *a.range, a.dump)
    print(f'Дамп памяти {a.range[0]}..{a.range[1]} записан в {a.dump}')


if __name__ == '__main__':
    main()
