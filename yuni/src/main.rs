mod cli;
use cli::*;
mod rust_code;

// fn solve_abs_1() {
//   let test1 = ["1 2 3 test", "6 test"];
//   let test2 = ["72 128 256 myonmyon", "456 myonmyon"];
// }

fn main() {
  let args = cli::CommandLineArgs::parse();
  cli::setup_work_dir(&args.work_dir).ok();
  loop {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).ok();
    let content = input.trim();
    let mut root: rust_code::Root = Default::default();
    root.add_use(rust_code::Use::new("std::io"));
    let main_fn = rust_code::Func::new(
      "main",
      &vec![
        format!("let mut input = String::new();"),
        format!("std::io::stdin().read_line(&mut input).ok();"),
        format!("println!(\"input: {{input}}\");"),
        format!("println!(\"content: {content}\");"),
      ],
    );
    root.add_func(main_fn);
    let code = root.to_string();
    println!("{code}");
    println!("{}", cli::execute(&code, "input kamone"));
  }
}
