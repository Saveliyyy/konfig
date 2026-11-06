"""Задача 1. Первый проход ассемблера.

Строит таблицу символов (метка -> адрес) и промежуточный код
в символической форме: список кортежей (операция, аргумент).
"""

import sys


def parse_arg(arg):
    """Числовой аргумент -> int, метка остаётся строкой, нет аргумента -> 0."""
    if arg is None:
        return 0
    try:
        return int(arg)
    except ValueError:
        return arg


def pass1(source):
    symtab = {}
    code = []
    for line in source.splitlines():
        line = line.split('#', 1)[0]          # убираем комментарий
        if not line.strip():
            continue
        fields = line.split()
        if not line[0].isspace():             # строка начинается с метки
            symtab[fields[0]] = len(code)
            fields = fields[1:]
        op = fields[0]
        arg = fields[1] if len(fields) > 1 else None
        code.append((op, parse_arg(arg)))
    return symtab, code


def read_source(argv):
    path = argv[1] if len(argv) > 1 else 'sum.asm'
    with open(path, encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    symtab, code = pass1(read_source(sys.argv))
    print('Таблица символов:')
    print(symtab)
    print('Промежуточный код:')
    for instr in code:
        print(instr)
