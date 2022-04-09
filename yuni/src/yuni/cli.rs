use super::*;

use std::io::prelude::*;
use tempfile;

#[derive(clap::Parser, Debug)]
#[clap(name = "Yuni")]
pub struct CommandLineArgs {
  #[clap(short, long, default_value = "./work/")]
  pub work_dir: String,
}
impl CommandLineArgs {
  pub fn parse() -> Self {
    clap::Parser::parse()
  }
}

pub fn setup_work_dir(work_dir_str: &str) -> std::io::Result<()> {
  let work_dir = std::path::Path::new(work_dir_str);
  if !work_dir.exists() {
    std::fs::create_dir_all(work_dir)?;
  }
  std::env::set_current_dir(work_dir)?;
  Ok(())
}

pub fn execute(code: &str, stdin: &str) -> String {
  let file = std::fs::File::create("main.rs");
  file.unwrap().write_all(code.as_bytes()).ok();
  let compile = std::process::Command::new("rustc")
    .arg("main.rs")
    .output()
    .expect("failed to execute process");
  if !compile.status.success() {
    return String::from_utf8(compile.stderr).unwrap_or(String::from("failed to compile"));
  }
  print!(
    "{}",
    String::from_utf8(compile.stdout).unwrap_or(String::from(""))
  );
  let mut tmpfile = tempfile::tempfile().unwrap();
  write!(tmpfile, "{stdin}").unwrap();
  tmpfile.seek(std::io::SeekFrom::Start(0)).unwrap();
  let executed = std::process::Command::new("./main")
    .stdin(tmpfile)
    .output()
    .expect("failed to execute process");
  String::from_utf8(executed.stdout).unwrap_or(String::from(""))
}
