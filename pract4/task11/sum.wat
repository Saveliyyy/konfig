;; Тот же модуль, написанный вручную в текстовом формате Wasm.
;; Логика повторяет программу из задачи 1 (аккумулятор + переменная sum).
(module
  (import "env" "get" (func $get (result i32)))
  (import "env" "put" (func $put (param i32)))
  (func (export "run")
    (local $acc i32)
    (local $sum i32)
    i32.const 0            ;; ld zero
    local.set $sum         ;; st sum
    (block $done
      (loop $loop
        call $get          ;; get
        local.tee $acc
        i32.eqz
        br_if $done        ;; jz done
        local.get $acc
        local.get $sum
        i32.add            ;; add sum
        local.set $sum     ;; st sum
        br $loop))         ;; j loop
    local.get $sum         ;; done: ld sum
    call $put))            ;; put ; halt
