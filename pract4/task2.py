"""Задача 2. Второй проход ассемблера: замена меток адресами."""

import sys

from task1 import pass1, read_source


def pass2(symtab, code):
    result = []
    for op, arg in code:
        if isinstance(arg, str):
            if arg not in symtab:
                raise NameError(f'Неизвестная метка: {arg}')
            arg = symtab[arg]
        result.append((op, arg))
    return result


def assemble(source):
    symtab, code = pass1(source)
    return pass2(symtab, code)


if __name__ == '__main__':
    for addr, instr in enumerate(assemble(read_source(sys.argv))):
        print(f'{addr}: {instr}')
