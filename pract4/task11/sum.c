// Пример из задачи 1 на Си: сумма вводимых чисел до нуля.
// get и put импортируются из JS (там они реализованы через prompt и alert).
__attribute__((import_module("env"), import_name("get"))) int get(void);
__attribute__((import_module("env"), import_name("put"))) void put(int x);

void run(void) {
    int sum = 0;
    int x;
    while ((x = get()) != 0)
        sum += x;
    put(sum);
}
