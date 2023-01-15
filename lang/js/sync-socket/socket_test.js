let socket = require('./build/Release/socket');
// console.log(socket.add(3, 5));
// console.log(socket.create("aa"))
// console.log(socket.func)
// console.log(socket.func())
// console.log(socket.func()())
// console.log(socket.add(1))
const obj = new socket.MyObject(10);
console.log(obj.plusOne());
console.log(obj.plusOne());
console.log(obj.plusOne());
