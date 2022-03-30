// Webの資産も使えない。が、あれは仕組みがキモいのでいらん
// ライブ配信はできるし。というかこのひとにHTTP接続できればいいのでは？
// 並列コンパイル・高速(差分)コンパイルしたい。静的型付けでコンパイルできて高速実行したい

## Grammar
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

// 略記(↑に展開される(といいな))
sum := fn(T: Addable)(x: T, y: T) -> T {
  result := T{0}
  for (i := range(x, y)) result += i;
  result
}
res := sum(0, 10);


// bou は Bound 型の変数
bou := mut x := 4;
// boubou
boubou := bou := x := 4
main := fn();

// import
axis := import rust
np := import python.numpy
color := import nodejs.color

// 内部的にはラッパになっている気がする
if Some(x) := np.random.seed(0) {

}
```
