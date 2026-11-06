"""Прогон всех этапов варианта 1: ассемблирование тестов спецификации
в режиме тестирования, затем сборка и запуск всех программ с дампом памяти.

Запуск из этой папки:  python run_all.py
Результаты: папка out/ (*.bin — машинный код, *.xml — дампы памяти).
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RANGES = {"copy":"300:324","alu":"300:305","vector":"300:317","example1":"300:317","example2":"300:317","example3":"300:317"}


def sh(*args):
    subprocess.run([sys.executable, *args], cwd=HERE, check=True)


os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
print('=== Этапы 1-2: тесты из спецификации')
sh('assembler.py', 'programs/test.asm', 'out/test.bin', '--test')
for name, rng in RANGES.items():
    print(f'\n=== {name}')
    sh('assembler.py', f'programs/{name}.asm', f'out/{name}.bin')
    sh('interpreter.py', f'out/{name}.bin', f'out/{name}.xml', rng)
