# Comment

一行コメントと複数行コメントが有り、全てそのまま変換する。
ネストは

## Retreat / Nim
```nim
# a comment
#[ multiline
comments ]#
```

## C++ / C# / Java / Rust / Go / js / PHP
```c++
// a comment
/* multiline
comments */
```

## Lua
```lua
-- a comment
--[[ multiline
comments ]]
```

## Python
```py
# a comment
''' multiline
comments '''
```

## Ruby / Perl5
```rb
# a comment
=begin
multiline
comments
=end
```

## Haskell
```haskell
- a comment
{- multiline
comments -}
```
