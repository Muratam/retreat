自分で自分を拡張できる「強いAI」を作るためのプログラミング言語がほしい。
そしてプログラミングの辛さをこの世から消し去りたい。
かつてのLISPが目指していた哲学を、今、実現したい。

## 構想

起動してスクリプトを食わせると逐次コンパイルし、自己を拡張しつつ実行する。
「体験」を入力として自分自身が実行するプログラムを生成し、「再起動せずに」ロードする。
自分自身が実行しているコードをAST(配列)として持っているので、拡張(縮小も)できる。
(依存関係を見て、安全に変更可能なら変更可能)
ほぼほぼスクリプト言語なので実行速度は遅い...
自分自身はRustかC言語か...。

## Specification
- type: {i,u}{8,16,32,64,size}, bool, f{32, 64}, char(unicode?), array
- dynamic loadable: C++, Python, Js

## 実行速度
通常: スクリプトなので柔軟だがまあまあ遅い
高速: 二重forでのsumとか高速にできるといいが...。なんかいい感じに?
超高速: GPGPUする(できるの？)

## Grammar
```
// Struct Trait Module 型は扱える.
// Impl型, If型, For型, Expr型, Stmt型 ...
math := fn () -> Module {
  Newable := trait { new := fn() -> &Self; }
  // priv / pub は無い(_から始まる)
  Vec2 := struct { x: f32, y: f32, _dummy: f32 }
  Vec3 := struct { x: f32, y: f32, z: f32 } impl {
    // 参照になる
    new := fn() -> &Self { &Self{ x: 0.0, y: 0.0, z: 0.0 } }
    // コピーになる(同名のbindはできない)
    new_a := fn(a: f32) -> Self { Self{ x: a, y: a, z: a } }
    `+` := fn(&self, r: &Self) -> Self { Self{} }
    count := fn() -> usize { 3 }
    count := fn(&self) -> usize { Self.count() }
    count := fn(offset: i32 := 0) -> usize { 3 }
    length := usize { 3 }
  }
  // 後から impl するので後読みはいらない
  Vec2 impl {
    to_vec3 := fn(&self) -> Vec3 { Vec3.new(self.x, self.y) }
    count := 2;
  }
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
```

## Grammar　（TODO）

マクロ生成が手間なのが悪い。これはLispでは楽。LL1で人間の書きやすさを無視できるため。
内部的にはLISPにしたほうがいいのでは？

```
# 機能
struct Bound {
  String name;
  String type;
}
struct Struct {
  Bound[] bounds;
}
struct Fn {
  String name;
  Struct inputs;
  Struct outputs;
}
struct Interface {
  Fn[] declares;
}


let x = (interface IListener (
  (fn new ())
  (fn name ())
  (fn get ())
  (fn set ())
))
```


```
// やりたいこと
// インターフェイスの宣言は欲しい
// IListener は trait 型の変数
IListener := mut trait {
  get := fn(&self) -> u64;
  set := fn(&mut self, v: u64);
  // fn version
  new := fn() -> Self;
  name := mut fn() -> u64 { 42 }
  // string version
  tag := mut String; // tag は lazy String 型
  tag2 := mut "";  // tag2 は "" に束縛されているString型
}

// Vec4 は Varying 型の変数
// インスタンスごとに異なる変数の宣言
Vec4Var := mut trait {
  x := f32; y := f32; z := f32; w := 0.0;
  name := fn() -> u64 { 0 }
}
Vec4Uni := mut trait {
  a := mut 0;
  new := mut fn() -> Self { Self {0,0,0,0, fn()->{0}} }
}
Vec4 := struct {
  varying := Vec4Var;
  uniform := Vec4Uni;  // 全て初期値が設定されているtraitのみ
  pod := trait { a := f32; b := f32; c := f32; }
}
// Global -> Uniform -> Varying
// Copy ? Ref ? Mutable ...?
v4 := Vec4.new()
x := v4.x
Vec4Uni.a = 10;



// bou は Bound 型の変数
bou := mut x := 4;
// boubou
boubou := bou := x := 4
main := fn();


// こういう相互依存が書けないと困るので、型の解決は遅延
A := interface { x := fn() -> B { B::create() } }
B := interface { x := fn() -> A; new := fn() -> Self; }

// 展開すると
A := interface { x := fn() -> interface { x := fn() -> A }; }

// 再代入
A = interface {}
// Shadowing
A := interface {}

// 宣言し直すとどうなる？
// というか前から順に実行なの？
IListener := interface {}

{ // priv な interface の宣言
  IPriv := interface {}
  import internal  // 子階層のモジュールのimport
}

fn main() {
  let II = interface {} // 関数内でも宣言できる
}



// コンパイル後、スクリプトとしても、実行可能libファイルとしても持つ
// lambda blessed
let hoge : [T:IListener, U](x:T, y:i32, z:U) -> bool {

}

if (let Some(x) = ) {

}

```


```

// パッケージシステム・構文はRustがいい
from rust import axios

// ライブラリの充実度はpythonがいい
from python import numpy as np

// ブラウザで実行できるといい
from nodejs import color

// Compute Shader で, 気軽にGpGpuできるといい
from compute import exec

// 内部的にはラッパになっている気がする
let x = np.random.seed(0)

// マルチスレッド・ComputeShader実行を気軽にしたい（速度がほしい）
// Webはどちらも向いてないのでむり...。仕方ない
// Webの資産も使えない。が、あれは仕組みがキモいのでいらん
// ライブ配信はできるし。というかこのひとにHTTP接続できればいいのでは？


// 並列コンパイル・高速(差分)コンパイルしたい。静的型付けでコンパイルできて
高速実行したい

// 自分で自分を拡張できるように、インタプリタ的に実行できる必要もある

# public(build for all)
pub pod X {
  i32 i;
  u32 u;
  u32 x;
}

# private(build effects only for current module !)
pub struct X {
  i32 i;
  u32 u;
  u32 x;
}

impl X {

}

# 内部的には C 言語とかになっていてほしい(zero overhead)
fn main() {

}
```
