// Stmt
#[derive(Default)]
pub struct Stmt {
  stmt: String,
}

// Fn
#[derive(Default)]
pub struct Func {
  name: String,
  body: Vec<Stmt>,
}
impl Func {
  pub fn new(name: &str, body: &Vec<String>) -> Self {
    Self {
      name: String::from(name),
      body: body
        .iter()
        .map(|x| Stmt {
          stmt: String::from(x),
        })
        .collect::<Vec<Stmt>>(),
    }
  }
}
impl ToString for Func {
  fn to_string(&self) -> String {
    let mut result = String::new();
    let name = &self.name;
    result.push_str(&format!("fn {name}() {{\n"));
    for stmt in &self.body {
      result.push_str("  ");
      result.push_str(&stmt.stmt);
      result.push_str("\n");
    }
    result.push_str("}\n");
    result
  }
}

// Use
pub struct Use {
  name: String,
}
impl Use {
  pub fn new(symbol: &str) -> Self {
    Self {
      name: String::from(symbol),
    }
  }
}
impl ToString for Use {
  fn to_string(&self) -> String {
    format!("use {};\n", self.name)
  }
}

// Root
#[derive(Default)]
pub struct Root {
  uses: HashMap<String, Use>,
  funcs: HashMap<String, Func>,
}
impl Root {
  pub fn add_use(&mut self, symbol: Use) {
    self.uses.insert(symbol.name.clone(), symbol);
  }
  pub fn add_func(&mut self, func: Func) {
    self.funcs.insert(func.name.clone(), func);
  }
}
impl ToString for Root {
  fn to_string(&self) -> String {
    let mut result = String::new();
    for symbol in &self.uses {
      result.push_str(&symbol.1.to_string());
    }
    for func in &self.funcs {
      result.push_str(&func.1.to_string());
    }
    result
  }
}
