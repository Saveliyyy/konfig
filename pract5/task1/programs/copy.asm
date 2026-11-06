; Этап 3: копирование массива из 5 элементов
; источник 300..304, приёмник 320..324
; --- инициализация: записать [10, 20, 30, 40, 50] в память с адреса 300
load_const 2, 300       ; r2 = 300
load_const 1, 10
write      0, 2, 1       ; mem[300+0] = r1
load_const 1, 20
write      1, 2, 1       ; mem[300+1] = r1
load_const 1, 30
write      2, 2, 1       ; mem[300+2] = r1
load_const 1, 40
write      3, 2, 1       ; mem[300+3] = r1
load_const 1, 50
write      4, 2, 1       ; mem[300+4] = r1
; --- копирование
load_const 5, 320       ; r5 = адрес приёмника
load_const 3, 300
read       4, 3          ; r4 = mem[r3]
write      0, 5, 4       ; mem[320+0] = r4
load_const 3, 301
read       4, 3          ; r4 = mem[r3]
write      1, 5, 4       ; mem[320+1] = r4
load_const 3, 302
read       4, 3          ; r4 = mem[r3]
write      2, 5, 4       ; mem[320+2] = r4
load_const 3, 303
read       4, 3          ; r4 = mem[r3]
write      3, 5, 4       ; mem[320+3] = r4
load_const 3, 304
read       4, 3          ; r4 = mem[r3]
write      4, 5, 4       ; mem[320+4] = r4
