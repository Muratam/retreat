// 並列コンパイル・高速(差分)コンパイルしたい。静的型付けでコンパイルできて高速実行したい
// ボドゲ作ったり遊んだりできる？Gpuの実験もできる？言葉の解釈もできる？

## Grammar
コンピュータでも変更しやすくて、制御フローがわかりやすくて一貫性のある言語
```
math := fn () -> Module {
  Newable := trait { new := fn() -> Self; }
  // priv / pub は無い(_から始まる)
  Vec2 := struct { x: f32; y: f32; _dummy: f32 }
  Vec3 := struct { x: f32; y: f32; z: f32;
  } impl {
    new := fn() -> Self { Self{ x: 0.0, y: 0.0, z: 0.0 } }
    `+` := fn(self, r: Self) -> Self { Self{} }
    count := fn(offset: i32 := 0) -> usize { 3 }
    length := usize { 3 }
  }
  // 後から impl できるので後読みはいらない
  Vec2 impl { to_vec3 := fn(self) -> Vec3 { Vec3.new(self.x, self.y) } }
  v2 := Vec2.new();
  // 実行すると一度だけprintされる
  Rect := fn(T: Type) -> Type {
    print("executed");
    struct {
      r:T,l:T,t:T,b:T
    } impl {
      fn new(a: T) -> Self { Self { r:a,l:a,t:a,b:a }}
    }
  }
  RRect := Rect;
  // []で呼び出すと一度生成した値をずっと参照して使用するので同一
  // メモ化としても使える. 参照カウントが0になると消える(のでDeallocできるし、更新できる)
  x := Array[Rect[f32]].new[0.0];
  y := Array[RRect[f32]].new(1.0);
  assert(typeof(x) == typeof(y));
  f := fn(T: Newable) -> &T { T.new() }
  v := f(Vec3);  // マクロいらない！
  module { Vec2, Vec3, Rect, Newable }
}[];

// 愚直に
sum := fn(T: Addable) -> fn(x: T, y: T) -> T {
  fn(x: T, y:T) -> T {
    result := T{0}
    for (i := range(x, y)) result += i;
    result
  }
}
res := sum[i32](0, 10)

// 一般的な if for while return がある
x := if x {} else {}
for x := range(10) {}
if x { return 10 }
while x { break; }

// 最終的なコードには存在しないが、解釈器には存在する型と構文
// コード(AST)を受け取ってコード(AST)を出力する所なので、変な状態になっても問題なし。
T := @token { "x" };
E := @expr {};
B := @bind { T , expr {} };
S := @stmt {};
SC := @scope {};
// return とか break とかやばい...
I := @if { };
F := @for { };
W := @while { };

// import
axis := import rust
np := import python.numpy
color := import nodejs.color

// 内部的にはラッパになっている気がする
x := np.random.seed(0)
// nullの場合も続けてCallできそう
```
