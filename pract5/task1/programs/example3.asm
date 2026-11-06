; Этап 5, пример 3: большие значения и границы 27-битной константы
; abs() над вектором длины 8: 300..307 -> новый вектор 310..317
; --- исходный вектор: записать [-1000000, 999999, -1, 1, 0, -67108864, 67108863, -12345] в память с адреса 300
load_const 2, 300       ; r2 = 300
load_const 1, -1000000
write      0, 2, 1       ; mem[300+0] = r1
load_const 1, 999999
write      1, 2, 1       ; mem[300+1] = r1
load_const 1, -1
write      2, 2, 1       ; mem[300+2] = r1
load_const 1, 1
write      3, 2, 1       ; mem[300+3] = r1
load_const 1, 0
write      4, 2, 1       ; mem[300+4] = r1
load_const 1, -67108864
write      5, 2, 1       ; mem[300+5] = r1
load_const 1, 67108863
write      6, 2, 1       ; mem[300+6] = r1
load_const 1, -12345
write      7, 2, 1       ; mem[300+7] = r1
; --- поэлементный abs()
load_const 3, 300
read       4, 3          ; r4 = x[i]
load_const 5, 310
abs        5, 4          ; y[0] = abs(x[0])
load_const 3, 301
read       4, 3          ; r4 = x[i]
load_const 5, 311
abs        5, 4          ; y[1] = abs(x[1])
load_const 3, 302
read       4, 3          ; r4 = x[i]
load_const 5, 312
abs        5, 4          ; y[2] = abs(x[2])
load_const 3, 303
read       4, 3          ; r4 = x[i]
load_const 5, 313
abs        5, 4          ; y[3] = abs(x[3])
load_const 3, 304
read       4, 3          ; r4 = x[i]
load_const 5, 314
abs        5, 4          ; y[4] = abs(x[4])
load_const 3, 305
read       4, 3          ; r4 = x[i]
load_const 5, 315
abs        5, 4          ; y[5] = abs(x[5])
load_const 3, 306
read       4, 3          ; r4 = x[i]
load_const 5, 316
abs        5, 4          ; y[6] = abs(x[6])
load_const 3, 307
read       4, 3          ; r4 = x[i]
load_const 5, 317
abs        5, 4          ; y[7] = abs(x[7])
