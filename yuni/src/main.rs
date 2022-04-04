use clap::Parser;
use std::env;
use std::fs;
use std::io::prelude::*;
use std::path::Path;
use std::process;

#[derive(clap::Parser, Debug)]
#[clap(name = "Yuni")]
struct CommandLineArgs {
  #[clap(short, long, default_value = "./work/")]
  work_dir: String,
}

fn setup_work_dir(work_dir_str: &str) -> std::io::Result<()> {
  let work_dir = Path::new(work_dir_str);
  if !work_dir.exists() {
    fs::create_dir_all(work_dir)?;
  }
  env::set_current_dir(work_dir)?;
  Ok(())
}

fn execute(code: &str) {
  let file = fs::File::create("main.rs");
  file.unwrap().write_all(code.as_bytes()).ok();
  let compile = process::Command::new("rustc")
    .arg("main.rs")
    .output()
    .expect("failed to execute process");
  if !compile.status.success() {
    return;
  }
  let executed = process::Command::new("./main")
    .output()
    .expect("failed to execute process");
  println!("{:?}", String::from_utf8(executed.stdout));
}

fn main() {
  let args = CommandLineArgs::parse();
  setup_work_dir(&args.work_dir).ok();
  loop {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).ok();
    let content = input.trim();
    let code = format!("fn main() {{  println!(\"{content}\"); }}");
    println!("{}", code);
    execute(&code);
  }
}
