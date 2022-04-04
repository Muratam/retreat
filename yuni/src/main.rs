mod cli;
use cli::*;

fn main() {
  let args = cli::CommandLineArgs::parse();
  cli::setup_work_dir(&args.work_dir).ok();
  loop {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).ok();
    let content = input.trim();
    let code = format!("fn main() {{  println!(\"{content}\"); }}");
    println!("{}", code);
    cli::execute(&code);
  }
}
