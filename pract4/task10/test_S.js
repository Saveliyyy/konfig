// Проверка в Node.js: node test_S.js
const fs = require('fs');
const bytes = fs.readFileSync(__dirname + '/S.wasm');
WebAssembly.instantiate(bytes).then(({ instance: wasmInstance }) => {
  console.log(wasmInstance.exports.S(10));
});
