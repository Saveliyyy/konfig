"""Прогон всех этапов варианта 2: ассемблирование тестов спецификации
в режиме тестирования, затем сборка и запуск всех программ с дампом памяти.

Запуск из этой папки:  python run_all.py
Результаты: папка out/ (*.bin — машинный код, *.csv — дампы памяти).
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RANGES = {"copy":"200:214","alu":"200:204","vector":"200:210","example1":"200:210","example2":"200:210","example3":"200:210"}


def sh(*args):
    subprocess.run([sys.executable, *args], cwd=HERE, check=True)


os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
print('=== Этапы 1-2: тесты из спецификации')
sh('assembler.py', 'programs/test.json', 'out/test.bin', '--test')
for name, rng in RANGES.items():
    print(f'\n=== {name}')
    sh('assembler.py', f'programs/{name}.json', f'out/{name}.bin')
    sh('interpreter.py', f'out/{name}.bin', f'out/{name}.csv', rng)
