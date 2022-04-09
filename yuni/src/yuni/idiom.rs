use super::*;

// コサイン距離が欲しいが
#[derive(std::fmt::Debug)]
pub struct Symbol {
  id: u64,
  represent: Option<String>, // (運良く)特定の単語と同じ概念を表す場合
}
impl Symbol {
  pub fn new(id: u64) -> Self {
    Self {
      id,
      represent: None,
    }
  }
  pub fn get_id(&self) -> u64 {
    self.id
  }
}

pub struct SymbolManager {
  last_id: u64,
  memory: std::collections::HashMap<String, Ptr<Symbol>>,
}
impl SymbolManager {
  pub fn new() -> Self {
    Self {
      last_id: 0,
      memory: std::collections::HashMap::new(),
    }
  }
  pub fn new_symbol(&mut self) -> Ptr<Symbol> {
    let id = self.last_id;
    self.last_id += 1;
    std::sync::Arc::new(std::sync::RwLock::new(Symbol::new(id)))
  }
  pub fn find_symbol_by_word(&self, word: &str) -> Option<Ptr<Symbol>> {
    self.memory.get(word).map(|x| x.clone())
  }
}
// He ate the dog
// ->
