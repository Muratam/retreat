pub use clap::Parser;
use std::env;
use std::fs;
use std::io::prelude::*;
use std::path::Path;
use std::process;

#[derive(clap::Parser, Debug)]
#[clap(name = "Yuni")]
pub struct CommandLineArgs {
  #[clap(short, long, default_value = "./work/")]
  pub work_dir: String,
}

pub fn setup_work_dir(work_dir_str: &str) -> std::io::Result<()> {
  let work_dir = Path::new(work_dir_str);
  if !work_dir.exists() {
    fs::create_dir_all(work_dir)?;
  }
  env::set_current_dir(work_dir)?;
  Ok(())
}

pub fn execute(code: &str) -> String {
  let file = fs::File::create("main.rs");
  file.unwrap().write_all(code.as_bytes()).ok();
  let compile = process::Command::new("rustc")
    .arg("main.rs")
    .output()
    .expect("failed to execute process");
  if !compile.status.success() {
    return String::from("");
  }
  let executed = process::Command::new("./main")
    .output()
    .expect("failed to execute process");
  String::from_utf8(executed.stdout).unwrap_or(String::from(""))
}
