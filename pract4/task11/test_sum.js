// Проверка в Node.js без браузера: prompt/alert подменены. node test_sum.js
const fs = require('fs');
const input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0];
const imports = { env: {
  get: () => { const x = input.shift(); console.log('<-', x); return x; },
  put: (x) => console.log('->', x),
}};
WebAssembly.instantiate(fs.readFileSync(__dirname + '/sum.wasm'), imports)
  .then(({ instance }) => instance.exports.run());
