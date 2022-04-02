# 実装サンプル
思想: 再帰を書けなくしているので、参照カウントで管理できるしDAG になる。変更しやすい

## math
```go
math := {
  ::Vec3 := mut struct(x: f32, y: f32, z: f32, opt: f32 = 0.0) {
    ::zero := fn() Self(0.0, 0.0, 0.0);
    ::one  := fn() Self(1.0, 1.0, 1.0, opt: 0.0);
    ::`+` := fn(self, rhs: Self) { self.x + rhs.x };
    ::`+=` := fn(mut self, rhs: Vec3) { self.x += rhs.x }
  }
  ::Vec4 := mut struct(x: f32, y: f32, z: f32, w: f32);
  ::
}
```
