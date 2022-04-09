mod yuni;

fn main() {
  let mut symbol_manager = yuni::idiom::SymbolManager::new();
  let symbol = symbol_manager.new_symbol();
  println!("{symbol:?}");
  let args = yuni::cli::CommandLineArgs::parse();
  yuni::cli::setup_work_dir(&args.work_dir).ok();
  println!("{args:?}");
  loop {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).ok();
    // solve_abs_1();
  }
}
