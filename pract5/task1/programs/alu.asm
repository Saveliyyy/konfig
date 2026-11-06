; Этап 4: проверка abs(). Результаты в ячейках 300..305
load_const 1, -5
load_const 2, 300
abs        2, 1          ; mem[300] = abs(-5)
load_const 1, 7
load_const 2, 301
abs        2, 1          ; mem[301] = abs(7)
load_const 1, 0
load_const 2, 302
abs        2, 1          ; mem[302] = abs(0)
load_const 1, -123456
load_const 2, 303
abs        2, 1          ; mem[303] = abs(-123456)
load_const 1, 99
load_const 2, 304
abs        2, 1          ; mem[304] = abs(99)
load_const 1, -67108864
load_const 2, 305
abs        2, 1          ; mem[305] = abs(-67108864)
