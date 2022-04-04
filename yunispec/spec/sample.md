# 実装サンプル
- 思想: 再帰を書けなくしているので、参照カウントで管理できるしDAG になる。変更しやすい

## math
```rust
// axis := use lang.rust.axis;
// np := use lang.python.numpy;
// color := use lang.nodejs.color;
// x := np.random.seed(0) // nullの場合も続けてCallできそう. Option[]
io := use yuni.std.io; // 再帰が書けないので依存関係がDAGになる(ようにuse)
math := struct () impl {
  f1 := mut fn () {};
  // ループ。相互参照でわない
  f2 := fn () { f1(); };
  f1 = mut fn () { f2(); };
  // 再帰が書けてしまわない
  f3 := mut fn (x: i32) i32 { 0 };
  f3 = mut fn (x: i32) i32 { f3(10) };
  pub Vec3 := struct (x: f32, y: f32, z: f32, _opt: f32) impl {
    // Self はここの定義 + データ(x,y,z) の型.
    // impl句は Self で囲う. { Self := @magic; impl{} ; Self }
    pub new := fn (x: f32, y: f32, z: f32, _opt: f32 = 0.0) Self(x, y, z, _opt: _opt);
    pub zero := new(0.0, 0.0, 0.0);
    pub one := new(1.0, 1.0, 1.0);
    // [type]? { } 形式でも, 好きな方法で。
    pub add := fn (self: Self, rhs: Self) { lhs.x + rhs.x };
    pub sub := fn (self: Self, rhs: Self) f32 { 0; lhs.x - rhs.x };
    pub mul := fn (self: Self, rhs: Self) lhs.x * rhs.x;
    pub `+` := add;
    pub `+=` := fn (self: mut Self, rhs: Self) { lhs.x += rhs.x; };
    // x += y; -> x@type.`+=`(x, y); と解釈される(型情報を持っているので可能)
    // x.add(y) -> x@type.add(x, y);
  };
  pub Vec4 := struct (x, y, z: f32, _opt: f32 = 0.0) impl {
    pub new := fn (x, y, z, w: f32) Self(x, y, z, w);
  };
  // 循環参照になるので後から定義できない(必要ならY-Convと同様にimplに分ければいい)
  // ::Vec3::toVec4 := fn (lhs: Self) Vec4::new(lhs.x, lhs.y, lhs.z, 0.0);

  // trait. Self は AddableだがSuperのものを指す
  pub Addable := trait (
    `+`: fn (self: Self, rhs: Self) Self,
    count: usize := 0.0
  );
  // 返り値を書かないメリット
  // []で呼び出すと一度生成した値をずっと参照して使用できる
  sum := fn (T: ::Addable) fn (x, y : T) T {
    result := mut x;
    for i in range(x, y) result += i;
    result
  };
  // 無への代入式
  io.print(sum[i32](0, 10));
  // []で呼び出すと一度生成した値をずっと参照して使用するので同一
  // メモ化としても使える. 参照カウントが0になると消える(のでDeallocできるし、更新できる)
  pub Rect := fn (T: Type) {
    // [] で実行すると新規追加時一度だけprintされる
    io.print("executed");
    struct (x: T) {} impl {}
  };
  RRect := Rect;
  x := Array[Rect[f32]](0.0);
  y := Array[RRect[f32]](1.0);
  // assert(typeof (x) == typeof (y));
  // o) x := i32 { y := 5 * { 1 + 3 } / 100; y };
  // x) x := 5 * (1 + 3);

  // 制御式
  x := if x 0.0 else if y 0.0 else { 3.0 };
  // [break xor continue] 型. break is [[nodiscard]] !
  assert(continue == {});
  for x in range(10) { print(x); if x == 10 break };
  {
    r := range(10); rx := mut r.begin();
    loop {
      if rx == r.end break
      else {
        { x := *rx; print(x); }
        if x <= 4 { rx ++; } else break
      }
    }
  };
  XxorY := union (x: i32, y: i32);
  x_xor_y := XxorY(x: 10);
  Option := fn (T:Type) union (none: Unit, some: T) impl {
    pub has := fn (self: Self) bool {
      match self {
      }
    }
    pub None := Self(none: {});
    pub Some := fn(some: T) Self(some: T);
  };
  x := Option[i32]::Some(0);
  x = Option[i32]::None;

  Color := enum (
    Red = 0,
    Blue,
    Green = 0, // invalid ?
    Unknown,
  );
  // todo: list, tree, ...
}
```

## 競プロコード例
```rust
std := use yuni.std;
read_int := () i32 {
  some { std.io.input.int() }
  else { std.io.output.error("invalid std.io.input.int") ; 0 }
}
write_int := std.io.output.int;
x := read_int();
y := read_int();
write_int(x + y);
```
