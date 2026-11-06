"""Ассемблер УВМ, вариант 1.

Синтаксис (по одной команде в строке, ';' — комментарий):
    load_const B, C      ; reg[B] <- C
    read       B, C      ; reg[B] <- mem[reg[C]]
    write      B, C, D   ; mem[reg[C] + B] <- reg[D]
    abs        B, C      ; mem[reg[B]] <- abs(reg[C])

Запуск:
    python assembler.py <исходник.asm> <программа.bin> [--test]
"""

import argparse

from isa import COMMANDS, encode


def parse(text):
    """Этап 1: текст -> промежуточное представление [(имя, [поля]), ...]."""
    ir = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.split(';', 1)[0].strip()
        if not line:
            continue
        name, _, rest = line.partition(' ')
        name = name.lower()
        if name not in COMMANDS:
            raise SyntaxError(f'Строка {lineno}: неизвестная команда "{name}"')
        try:
            args = [int(a, 0) for a in rest.replace(',', ' ').split()]
        except ValueError:
            raise SyntaxError(f'Строка {lineno}: аргументы должны быть числами')
        if len(args) != len(COMMANDS[name]['fields']):
            raise SyntaxError(f'Строка {lineno}: у {name} должно быть '
                              f'{len(COMMANDS[name]["fields"])} аргумент(а)')
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
    ap = argparse.ArgumentParser(description='Ассемблер УВМ (вариант 1)')
    ap.add_argument('source', help='путь к исходному файлу')
    ap.add_argument('output', help='путь к двоичному файлу-результату')
    ap.add_argument('--test', action='store_true', help='режим тестирования')
    a = ap.parse_args()

    with open(a.source, encoding='utf-8') as f:
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
