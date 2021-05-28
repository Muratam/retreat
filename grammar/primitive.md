# Primitive Types

- プリミティブ型は bool, number であり、そのまま変換可能
  - bool型：
    - `true false` のいずれか
    - `and or xor not` ができる
    - 演算子の優先順位は Retreat と同等になるように変換する
  - number型：
    - `-?\d+(\.\d+)?` が数値であり、そのまま変更せず渡す？
      - 自然な書き方を優先するため、処理系によって内部的な型が代わる。つまり、結果が変わりうる。
      - どの言語でも同じ結果がでる書き方、は不可能なため。
        2**100は、PythonとC++で明らかに結果が異なるだろう
    - Retreat では `-?\d+` と書くと int64 であり、
      `-?\d+\.\d+` と書くと float64 であるので、
      int64型変数にfloat64を代入するコードは書けない
    - `+ - * / % div mod shl shr and xor not > >= == <= <` ができる
    - https://emscripten.org/docs/porting/connecting_cpp_and_javascript/embind.html

## Retreat / Nim
```nim
let x = not false and true
var y = 10.0 # float64
var z1 = 3 # int64
# z1 = y # error (invalid type)
var z2 = 3.0 # float64
z2 = y # ok (same type)
```

## C++
```C++
const auto x = !false && true;
auto y = 10.0; // double
auto z1 = 3ll; // long long int
```


- Nim
- C++
- Rust
- C#
- Go
- Java
- Lua
- Python
- Ruby
- js(NodeJs)
- PHP
- Perl5
- Haskell
