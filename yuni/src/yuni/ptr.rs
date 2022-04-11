use super::*;
pub type Ptr<T> = std::sync::Arc<std::sync::RwLock<T>>;
pub type Weak<T> = std::sync::Weak<std::sync::RwLock<T>>;
pub fn new<T: Sized>(raw: T) -> Ptr<T> {
  std::sync::Arc::new(std::sync::RwLock::new(raw))
}
