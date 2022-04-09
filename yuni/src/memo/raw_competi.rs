mod raw_competi {
  enum VarType {
    Integer { min: i64, max: i64 },
    String { len_min: i64, len_max: i64 },
    Unknown,
  }
  struct Var {
    name: String,
    var_type: VarType,
  }
  struct Operation {
    name: String,
    inputs: Vec<VarType>,
    outputs: Vec<VarType>,
  }
  enum Parse {
    Var(Var),
    Delimiter(String),
  }
  fn test() {
    // ["1≤a,b,c≤1,000", "1≤∣s∣≤100"];
    // "a
    // b c
    // s"
    let raw_input = vec![
      Parse::Var(Var {
        name: String::from("a"),
        var_type: VarType::Integer { min: 1, max: 1000 },
      }),
      Parse::Delimiter(String::from("\n")),
      Parse::Var(Var {
        name: String::from("b"),
        var_type: VarType::Integer { min: 1, max: 1000 },
      }),
      Parse::Delimiter(String::from(" ")),
      Parse::Var(Var {
        name: String::from("c"),
        var_type: VarType::Integer { min: 1, max: 1000 },
      }),
      Parse::Delimiter(String::from("\n")),
      Parse::Var(Var {
        name: String::from("s"),
        var_type: VarType::String {
          len_min: 1,
          len_max: 100,
        },
      }),
    ];
    // "a+b+c" と "s" を 空白区切り
    let output = vec![
      Parse::Var(Var {
        name: String::from("`+`(`+`(a,b),c)"),
        var_type: VarType::Unknown,
      }),
      Parse::Delimiter(String::from(" ")),
      Parse::Var(Var {
        name: String::from("s"),
        var_type: VarType::Unknown,
      }),
    ];
    // a+b+c を構築する
    let add = Operation {
      name: String::from("`+`"),
      inputs: vec![
        VarType::Integer {
          min: i64::MIN,
          max: i64::MAX,
        },
        VarType::Integer {
          min: i64::MIN,
          max: i64::MAX,
        },
      ],
      outputs: vec![VarType::Integer {
        min: i64::MIN,
        max: i64::MAX,
      }],
    };
    // 積が奇数なら Odd と、 偶数なら Even と出力せよ。
  }
}
fn solve_abs_1() {
  let mut root: raw_rust_code::Root = Default::default();
  root.add_use(raw_rust_code::Use::new("std::io"));
  let main_fn = raw_rust_code::Func::new(
    "main",
    &vec![
      format!("let mut input = String::new();"),
      format!("std::io::stdin().read_line(&mut input).ok();"),
      format!("print!(\"{{input}}\");"),
    ],
  );
  root.add_func(main_fn);
  let code = root.to_string();
  println!("{code}");

  let tests = [
    ("1 2 3 test", "6 test"),
    ("72 128 256 myonmyon", "456 myonmyon"),
  ];
  for (input, output) in &tests {
    println!("{}", cli::execute(&code, input));
    println!("{output}");
  }
}
