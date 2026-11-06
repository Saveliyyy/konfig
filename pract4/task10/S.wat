;; Ручной вариант того же модуля в текстовом формате Wasm
(module
  (func (export "S") (param $n i32) (result i32)
    local.get $n
    local.get $n
    i32.const 1
    i32.add
    i32.mul
    i32.const 2
    i32.div_s))
