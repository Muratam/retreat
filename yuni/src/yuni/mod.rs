pub mod cli;
pub mod idiom;

type Ptr<T> = std::sync::Arc<std::sync::RwLock<T>>;
type WeakPtr<T> = std::sync::Weak<std::sync::RwLock<T>>;
