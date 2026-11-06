"""Задача 9. Числовой формат команд стековой машины из задачи 6,
сохранение кода в файл и загрузка из него.

Формат файла (little-endian):
  заголовок: 4 байта  b'SVM1'
             2 байта  число команд N (uint16)
  команда:   1 байт   код операции (uint8)
             4 байта  аргумент (int32; 0 у команд без аргумента)
Итого: 6 + 5*N байт.
"""

import struct
import sys

import task6 as vm

MAGIC = b'SVM1'
OPS = [vm.push, vm.add, vm.sub, vm.mul, vm.dup, vm.drop, vm.load,
       vm.store, vm.get, vm.put, vm.j, vm.jz, vm.halt]
CODE_OF = {op: i for i, op in enumerate(OPS)}
HAS_ARG = {vm.push, vm.load, vm.store, vm.j, vm.jz}


def to_bytes(code):
    out = bytearray(MAGIC + struct.pack('<H', len(code)))
    for op, *args in code:
        out += struct.pack('<Bi', CODE_OF[op], args[0] if args else 0)
    return bytes(out)


def from_bytes(data):
    if data[:4] != MAGIC:
        raise ValueError('Неверный формат файла')
    (n,) = struct.unpack_from('<H', data, 4)
    code = []
    for i in range(n):
        opcode, arg = struct.unpack_from('<Bi', data, 6 + 5 * i)
        op = OPS[opcode]
        code.append((op, arg) if op in HAS_ARG else (op,))
    return code


def save(code, path):
    with open(path, 'wb') as f:
        f.write(to_bytes(code))


def load(path):
    with open(path, 'rb') as f:
        return from_bytes(f.read())


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'sum.bin'
    save(vm.sum_code, path)
    code = load(path)
    assert code == vm.sum_code, 'Загруженный код отличается от исходного'
    print(f'Сохранено в {path}:', to_bytes(vm.sum_code).hex(' '))
    print('Загружено и проверено, запуск:')
    vm.execute(code)
