"""Ассемблер УВМ, вариант 2 (стековая машина). Синтаксис — JSON.

Программа — JSON-массив команд. Каждая команда — объект с ключом "op"
и полями команды; ключ "comment" допускается и игнорируется:
    {"op": "load_const", "B": 38}         push(B)
    {"op": "read", "B": 309}              push(mem[B])
    {"op": "write"}                       value = pop(); addr = pop(); mem[addr] = value
    {"op": "pow", "B": 180, "C": 1}       x = pop(); base = pop();
                                          mem[base + B] = pow(x, mem[base + C])

Запуск:
    python assembler.py <исходник.json> <программа.bin> [--test]
"""

import argparse
import json

from isa import COMMANDS, encode


def parse(text):
    """Этап 1: JSON -> промежуточное представление [(имя, [поля]), ...]."""
    program = json.loads(text)
    if not isinstance(program, list):
        raise SyntaxError('Программа должна быть JSON-массивом команд')
    ir = []
    for i, cmd in enumerate(program):
        name = cmd.get('op')
        if name not in COMMANDS:
            raise SyntaxError(f'Команда №{i}: неизвестная операция "{name}"')
        names = [f[0] for f in COMMANDS[name]['fields']]
        extra = set(cmd) - set(names) - {'op', 'comment'}
        missing = [n for n in names if n not in cmd]
        if extra or missing:
            raise SyntaxError(f'Команда №{i} ({name}): нужны поля {names}')
        ir.append((name, [int(cmd[n]) for n in names]))
    return ir


def format_ir(name, args):
    spec = COMMANDS[name]
    parts = [f'A={spec["A"]}'] + [f'{f[0]}={v}' for f, v in zip(spec['fields'], args)]
    return ', '.join(parts)


def assemble(ir):
    """Этап 2: промежуточное представление -> список машинных команд (bytes)."""
    return [encode(name, args) for name, args in ir]


def main():
    ap = argparse.ArgumentParser(description='Ассемблер УВМ (вариант 2)')
    ap.add_argument('source', help='путь к исходному файлу (JSON)')
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
