"""Ассемблер УВМ, вариант 3 (аккумуляторная машина). Синтаксис — CSV.

Каждая строка: op,B[,комментарий]. Первая строка — заголовок op,B,comment.
Пустые строки и строки, начинающиеся с '#', пропускаются.
    load_const,B     acc = B
    read,B           acc = mem[acc + B]
    write,B          mem[B] = acc
    sgn,B            acc = sgn(mem[B])

Запуск:
    python assembler.py <исходник.csv> <программа.bin> [--test]
"""

import argparse
import csv
import io

from isa import COMMANDS, encode


def parse(text):
    """Этап 1: CSV -> промежуточное представление [(имя, [поля]), ...]."""
    ir = []
    rows = csv.reader(io.StringIO(text))
    for lineno, row in enumerate(rows, 1):
        if not row or not row[0].strip() or row[0].lstrip().startswith('#'):
            continue
        name = row[0].strip().lower()
        if name == 'op':                      # строка заголовка
            continue
        if name not in COMMANDS:
            raise SyntaxError(f'Строка {lineno}: неизвестная команда "{name}"')
        nfields = len(COMMANDS[name]['fields'])
        try:
            args = [int(x.strip(), 0) for x in row[1:1 + nfields]]
        except ValueError:
            raise SyntaxError(f'Строка {lineno}: аргументы должны быть числами')
        if len(args) != nfields:
            raise SyntaxError(f'Строка {lineno}: у {name} должно быть {nfields} аргумент(а)')
        ir.append((name, args))
    return ir


def format_ir(name, args):
    spec = COMMANDS[name]
    parts = [f'A={spec["A"]}'] + [f'{f[0]}={v}' for f, v in zip(spec['fields'], args)]
    return ', '.join(parts)


def assemble(ir):
    """Этап 2: промежуточное представление -> список машинных команд (bytes)."""
    return [encode(name, args) for name, args in ir]


def main():
    ap = argparse.ArgumentParser(description='Ассемблер УВМ (вариант 3)')
    ap.add_argument('source', help='путь к исходному файлу (CSV)')
    ap.add_argument('output', help='путь к двоичному файлу-результату')
    ap.add_argument('--test', action='store_true', help='режим тестирования')
    a = ap.parse_args()

    with open(a.source, encoding='utf-8', newline='') as f:
        ir = parse(f.read())
    code = assemble(ir)
    binary = b''.join(code)
    with open(a.output, 'wb') as f:
        f.write(binary)

    if a.test:
        print('Промежуточное представление:')
        for name, args in ir:
            print(f'  {format_ir(name, args)}')
        print('Машинный код:')
        for (name, _), cmd in zip(ir, code):
            print(f'  {name:<11}', ', '.join(f'0x{b:02X}' for b in cmd))
    print(f'Размер двоичного файла: {len(binary)} байт')


if __name__ == '__main__':
    main()
