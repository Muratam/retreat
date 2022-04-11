use super::*;

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

// I am happy to join [with you today] in [what will go down in history
//   as the greatest demonstration for freedom in the history of our nation].

// He ate the dog.
// -> "He" "Ate" "The" "Dog" のシンボルに関して(+ 時間があれば: 編集距離探索もしてスペルミスを見逃さないようにして)
//   -> 「「He」という単語が「一般的に」表しているなにか」にまずアクセスが入る / (新概念の場合は別処理?)
//   -> Ate -[過去形]- Eat
//     -> 「過去形」は、「過去」としてイメージするものが違うかもしれないのでシンボル生成させる
//   -> TODO: He と he は同じ単語で、あくまでも綴上の問題で最終的には認識して欲しいが、今はめんどうなので He Ate The Dog に ?
// -> SVO / SVOC にマッチするものを探す
//   -> S:He / V:Eat(<- [Ate, Eats]) / The Doc
// -> 前提知識モジュール(He == he) / eats == eat / ate = eat + 過去 :: ここらへんは前提知識辞書が必要
//
