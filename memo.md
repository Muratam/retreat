// 並列コンパイル・高速(差分)コンパイルしたい。静的型付けでコンパイルできて高速実行したい
// ボドゲ作ったり遊んだりできる？Gpuの実験もできる？言葉の解釈もできる？

## Grammar
コンピュータでも変更しやすくて、制御フローがわかりやすくて一貫性のある言語
```
std := import yuni.std[];
math := fn () Module {
  Newable := trait { new := fn() Self; };
  // priv / pub は無い(_から始まる)
  Vec2 := struct { x: f32; y: f32; _dummy: f32 };
  Vec3 := struct { x: f32; y: f32; z: f32;
  } impl {
    new := fn() Self { Self{ x: 0.0, y: 0.0, z: 0.0 } }
    `+` := fn(self, r: Self) Self { Self{} }
    count := fn(offset: i32 := 0) usize { 3 }
    length := usize { 3 }
  };
  // 後から impl できるので後読みはいらない
  Vec2 impl { to_vec3 := fn(self) Vec3 { Vec3.new(self.x, self.y) } };
  v2 := Vec2.new();
  // 実行すると一度だけprintされる
  Rect := fn(T: Type) Type {
    std.print("executed");
    struct {
      r:T,l:T,t:T,b:T
    } impl {
      fn new(a: T) Self { Self { r:a,l:a,t:a,b:a }}
    };
  }
  x = x + 10;  // どうせASTで見るので見かけのパースしやすさは気にしなくていい
  RRect := Rect;
  // []で呼び出すと一度生成した値をずっと参照して使用するので同一
  // メモ化としても使える. 参照カウントが0になると消える(のでDeallocできるし、更新できる)
  x := Array[Rect[f32]].new[0.0];
  y := Array[RRect[f32]].new(1.0);
  assert(typeof(x) == typeof(y));
  f := fn(T: Newable) &T { T.new() }
  v := f(Vec3);  // マクロいらない！
  module { Vec2, Vec3, Rect, Newable }
}[];

// 愚直に
sum := fn(T: Addable) fn(x: T, y: T) T {
  fn(x: T, y:T) T {
    result := T{0}
    for (i := range(x, y)) result += i;
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
y := for x := range(10) { print(x); break x > 4 { x * x } }
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
         "fn(..., ...) Type? {}" |
         Expr "(" ")" |
Bind ::= Token ":=" Stmt
Unicodes ::= /.*/
Token ::= /[_a-zA-Z0-9]+/ | "`" /.*/ "`"
```
