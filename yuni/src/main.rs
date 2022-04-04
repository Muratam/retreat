use clap;
use std::env;
use std::fs;
use std::io::prelude::*;
use std::path::Path;
use std::process;

const DEFAULT_WORK_DIR: &'static str = "./work/";
const WORK_DIR_OPTION: &'static str = "work_dir";
fn parse_command_line_options() -> clap::ArgMatches {
  clap::Command::new("Yuni")
    .arg(
      clap::Arg::new(WORK_DIR_OPTION)
        .short('w')
        .help(&*format!("{WORK_DIR_OPTION} (default: {DEFAULT_WORK_DIR})")),
    )
    .get_matches()
}

fn setup_work_dir(work_dir: &Path) -> std::io::Result<()> {
  if !work_dir.exists() {
    fs::create_dir_all(work_dir)?;
  }
  env::set_current_dir(work_dir)?;
  Ok(())
}

fn generate_code() -> std::io::Result<()> {
  let mut file = fs::File::create("main.rs")?;
  file.write_all(b"fn main() { println!(\"Hello, world!\"); } \n")?;
  Ok(())
}

fn execute_code() {
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
  let matches = parse_command_line_options();
  let work_dir = Path::new(
    matches
      .value_of(WORK_DIR_OPTION)
      .unwrap_or(DEFAULT_WORK_DIR),
  );
  setup_work_dir(work_dir).ok();
  generate_code().ok();
  execute_code();
}
