"""Спецификация команд УВМ (вариант 3) и общее кодирование/декодирование.

Поле задаётся как (имя, младший бит, старший бит, знаковое).
Команда занимает size байт, порядок байт — little-endian.
"""

OPCODE_BITS = 8          # поле A: биты 0–7

COMMANDS = {
    # acc <- B
    'load_const': dict(A=143, size=5, fields=[('B', 8, 38, True)]),
    # acc <- mem[acc + B]
    'read':       dict(A=227, size=3, fields=[('B', 8, 18, False)]),
    # mem[B] <- acc
    'write':      dict(A=251, size=5, fields=[('B', 8, 38, False)]),
    # acc <- sgn(mem[B])
    'sgn':        dict(A=48, size=5, fields=[('B', 8, 38, False)]),
}

BY_OPCODE = {spec['A']: name for name, spec in COMMANDS.items()}


def encode(name, values):
    """values — список значений полей B, C, ... в порядке спецификации."""
    spec = COMMANDS[name]
    if len(values) != len(spec['fields']):
        raise ValueError(f'{name}: ожидается {len(spec["fields"])} аргумент(а), '
                         f'получено {len(values)}')
    word = spec['A']
    for (fname, lo, hi, signed), v in zip(spec['fields'], values):
        width = hi - lo + 1
        vmin, vmax = (-(1 << width - 1), (1 << width - 1) - 1) if signed else (0, (1 << width) - 1)
        if not vmin <= v <= vmax:
            raise ValueError(f'{name}: поле {fname}={v} вне диапазона [{vmin}, {vmax}]')
        word |= (v & ((1 << width) - 1)) << lo
    return word.to_bytes(spec['size'], 'little')


def decode(mem, pc):
    """Возвращает (имя, {поле: значение}, размер) для команды по адресу pc."""
    opcode = mem[pc] & ((1 << OPCODE_BITS) - 1)
    if opcode not in BY_OPCODE:
        raise RuntimeError(f'Неизвестный код операции {opcode} по адресу {pc}')
    name = BY_OPCODE[opcode]
    spec = COMMANDS[name]
    word = int.from_bytes(bytes(mem[pc:pc + spec['size']]), 'little')
    fields = {}
    for fname, lo, hi, signed in spec['fields']:
        width = hi - lo + 1
        v = (word >> lo) & ((1 << width) - 1)
        if signed and v >> (width - 1):
            v -= 1 << width
        fields[fname] = v
    return name, fields, spec['size']
