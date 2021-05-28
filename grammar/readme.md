# Retreat文法

RetreatはNim言語のサブセットで、以下の全てに変換可能。

- Nim : サブセットなのでコードはそもそも変換されない。
- C++ : GCが無いことに依存する箇所が引っ張られる
- Rust : 寿命に依存する箇所が引っ張られる
- C# : 特に障壁なし
- Java : 特に障壁なし
- Go : class, generics の設計がこれに引っ張られる
- Lua :
- Python : 変なスコープ, BigInt, ラムダ式
- Ruby
- js(NodeJs) : Number しかない...
- PHP
- Perl5
- Haskell : 手続き的な処理をそのまま書けるんか...?


# table of contents

ref: https://en.wikibooks.org/wiki/Java_Programming/Language_Fundamentals

- [Comments](./comment.md)
- [Primitive Types](./primitive.md)
- [String](./string.md)
- [Array](./array.md)
- [Table](./table.md)
- [Object](./object.md)
- [Function](./function.md)
- [Statement](./statement.md)

- Standard Libraries
  - [Print](./print.md)
  - [StandardIO](./stdio.md)
  - [Argv](/argv.md)
  - [Math](./math.md)
  - [File](./file.md)
  - [OS](./os.md)
