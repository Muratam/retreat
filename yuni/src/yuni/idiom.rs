use super::*;

/*
// とりあえず小学生レベルの算数から教えていきたい。
// 「~によると」があるので、軽率にstring literal を使ってもいいかも
- "1" := if "0" "succ"
- "2" := if "1" "succ"
- ...
- "9" := if "8" "succ"
- "10" := if "9" "succ"
- ...
- "101" := if "100" "succ"
- "+" := State
- <+> := Symbol // 動詞の引数には名前をつける。どういう意図で注釈するか。
- "3" := if "1" "+" <+> "2"
- "3" := if "2" "+" <+> "1"
- "" :=  if "1" + // "1" が足されているという状態にはなれるが、注意の先がないからあまり意味のない構文になっている。
...
("succ"_able という集合に "1" "2" ... は自動で入る)
- "5" := "4" "+" <+> ??
  - 絶対にそうではないが、多分そう。導けるはず。
  - 2桁の足し算などができるようになってきたら、そのうち内部i32とつなげる
  - 縮約規則もメタ的に覚えていく(疑問に抱く前に解決・推論できるようになる)。






*/
// そのシンボルが何の概念を表しているか
#[derive(std::fmt::Debug)]
pub enum Represent {
  Undefined,                  // とくに何も
  Word(String),               // 「単語」の場合 (人間とのAPI用)
  Instance(ptr::Ptr<Symbol>), // 特定のシンボルの1インスタンス
}

#[derive(std::fmt::Debug)]
pub struct Symbol {
  id: u64,
  represent: Represent,
}
impl Symbol {
  pub fn new(id: u64) -> Self {
    Self {
      id,
      represent: Represent::Undefined,
    }
  }
  pub fn get_id(&self) -> u64 {
    self.id
  }
}

// 近さ: グラフでの近さ(+関係性による重み) , 編集距離
#[derive(std::default::Default)]
pub struct SymbolManager {
  last_id: u64,
  word_memory: std::collections::HashMap<String, ptr::Ptr<Symbol>>,
}
impl SymbolManager {
  pub fn new() -> Self {
    Self::default()
  }
  pub fn new_symbol(&mut self) -> ptr::Ptr<Symbol> {
    let result = Symbol::new(self.last_id);
    self.last_id += 1;
    ptr::new(result)
  }
  pub fn find_symbol_by_word(&self, word: &str) -> Option<ptr::Ptr<Symbol>> {
    self.word_memory.get(word).map(|x| x.clone())
  }
}
