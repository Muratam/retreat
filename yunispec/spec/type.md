- Yuni言語は「実行中に」自分で自分を変更できる言語なので、全ての文法に型があり、動的に変更できる。

## 型一覧
- Primitive: {i,u}{8,16,32,64,size}, bool, f{32, 64}, char(unicode)
  - これらは Copy, ほかは全てRef. nullptrは無いよ.
- Constructed: Struct Enum Trait Function Tuple?
- Expression:
- Statement: If While For Return Match
- Std: Array String
- デフォルト引数は文法変えたらOK！ f := fn(x:i32, left?: i32 := 0) に f(0, left: 1) と明示的に書く
