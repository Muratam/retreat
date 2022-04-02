// 並列コンパイル・高速(差分)コンパイルしたい。静的型付けでコンパイルできて高速実行したい
// ボドゲ作ったり遊んだりできる？Gpuの実験もできる？言葉の解釈もできる？

## Grammar
コンピュータでも変更しやすくて、制御フローがわかりやすくて一貫性のある言語
```
// 再帰が書けないので依存関係がDAGになる
std := import yuni.std;
// Module, Struct, Trait と大雑把な型になって、次の型検査時にValidationされる
math := {
  // right  ) x := i32 { y := 5 * { 1 + 3 } / 100; y };
  // invalid) x := 5 * (1 + 3);
  // priv / pub は無い(_から始まる)
  f := fn (x: f32, opt :f32 := 0.0) f32 { 0.0 };
  f := fn (x: f32, opt :f32 := 0.0) { 1; 0.0 };
  f := fn (x: f32, opt :f32 := 0.0) 0.0;
  // :: はシンボル定義可能
  Vec3 := mut struct (x: f32, y: f32, opt :f32 := 0.0);
  Vec3::`+` := fn(self, rhs: Vec3) { self.x + rhs.x }
  Vec3::`+=` := fn(mut self, rhs: Vec3) { self.x += rhs.x }
  Vec3::new := fn() { Vec3(0.0, 0.0, 0.0) };
  // 後から impl できるので後読みはいらない

  f2 := fn (b: bool) { if b { if c 0.0 else 1.0 } else 1.0 };
  v2 := Vec2 (x: 0.0, y: 1.0);  // optional 以外は書いても書かなくてもいい
  v2 := Vec2 (0.0, 1.0);  // fn とおなじ。順序と名前が大事？
  f(0.0, opt: 1.0);
  // Self は Newable
  ::Newable := trait (newa: fn() Self, del: fn(), count: usize := 0.0);
  // :: でなく this. にすると、a と this.a が違って内部スコープで参照しにくく見える

  if x {} elif y {} elif z {} else {}
  // [] で実行すると一度だけprintされる
  ::Rect := (T: Type) Newable {
    std.print("executed");
    struct (fuhaha: i32) as Newable
  }
  x = x + 10;  // どうせASTで見るので見かけのパースしやすさは気にしなくていい
  RRect := Rect;
  // []で呼び出すと一度生成した値をずっと参照して使用するので同一
  // メモ化としても使える. 参照カウントが0になると消える(のでDeallocできるし、更新できる)
  x := Array[Rect[f32]].new[0.0];
  y := Array[RRect[f32]].new(1.0);
  assert(typeof(x) == typeof(y));
  f := (T: Newable) { T.new() }
  v := f(Vec3);  // マクロいらない！
  :: // 今まで::で定義したものが入る特殊シンボル
}

// 返り値を書かないメリット
sum := (T: Addable) {
  (x: T, y:T) {
    result := mut T{0}
    for i in range(x, y) { result += i; }
    result
  }
}
res := sum[i32](0, 10)

// import
axis := import rust;
np := import python.numpy;
color := import nodejs.color;
// 内部的にはラッパになっている気がする
x := np.random.seed(0)
// nullの場合も続けてCallできそう

// 制御構文： if for loop + break型
// break <> {} は、<> の条件を満たした時に Break[<>] 型の値を返す(違う場合はUnit).
// for や loop は Break[<>] を受け取った場合(not Unit), ループを終了する
x := if x { x := { 3 }; { 3 }; { 4 }; <> } else { ; ; ; <> }
y := for x in range(10) { print(x); break }
y := {
  r := range(10);
  rx := mut r.begin();
  loop {
    break rx != r.end
    if rx != r.end() {
      x := *rx;
      print(x);
      break x > 4 { x * x }
      rx ++;
    }
  }
}
{ x := 0 ; loop { print(x); b := break x <= 4 {}; x += 1; b} }


// 0. コア部分はRustで書く
// 1. 欲望&解釈器(つまり初期値)&API を我々がYuni言語でプログラムする
// 2. 実行すると「自己が実行するコードを生成、解釈器・APIも適宜更新(git commit も)」。チューニングされていく。
// 3. 大量のデータと、ただの評価関数の二乗誤差でやる場合は Deep Learning が必要。

// // まずはプログラミングの才能を伸ばしたい
// 例) 特定のA問題解く器
// - API: 標準入出力(不変)
// - 欲望: 問題概要Tokenとサンプル列とテストケース列を受け取って
//        テストケース列への答えを正答するコードを生成したい(不変)
// - 解釈器の更新器：プログラミングのコツを与える(不変)
// - 解釈器: 更新器に従ってよしなに自己を変えていく(生成コードがよくなっていくはず)
// 例2) 一般的なA問題解く器
// - 例1の一般化が進むに従ってメタ度が上がっていき、やがて一般的なA問題解く器ができるはず
// 例3) A問題の問題文を与えると解く器
// - 言語パース欲望を強くしていくとできそう。

// 最終的なコードには存在しないが、解釈器には存在する型と構文
// コード(AST)を受け取ってコード(AST)を出力する所なので、変な状態になっても問題なし。
// 依存関係や参照関係を見て...
Code ::= Stmt Code
Stmt ::= "{" Stmt "}" | Expr ";" Stmt | Expr
Expr ::= "" | Token | """ Unicodes """
         "if" Stmt "{" Stmt "}" "else" "{" Stmt "}" |
         "if" Stmt "{" Stmt "}" |
         "for" Bind "{" Stmt "}" | "loop" "{" Stmt "}" |
         "break" Stmt "{" Stmt "}" | "import" Stmt |
         Bind | Token "=" Stmt |
         "module" "{" ___ "}" |
         "struct" "{" ___ "}" | Stmt "impl" |
         "(..., ...) Type? {}" |
         Expr "(" ")" |
Bind ::= Token ":=" Stmt
Unicodes ::= /.*/
Token ::= /[_a-zA-Z0-9]+/ | "`" /.*/ "`"
```

```
ip := struct {
  v4 := option { struct { i32, i32, i32, i32 } }
  v6 := option { struct { i32, i32, i32, i32, i32, i32 } }
}
std := import yuni.std[];
read_int := () i32 {
  some { std.io.input.int() }
  else { std.io.output.error("invalid std.io.input.int") ; 0 }
}
write_int := std.io.output.int;
x := read_int();
y := read_int();
write_int(x + y);
```
