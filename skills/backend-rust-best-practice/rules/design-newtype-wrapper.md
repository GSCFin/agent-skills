---
title: Newtype Wrapper Pattern
impact: CRITICAL
impactDescription: type safety, orphan rule compliance, semantic clarity
tags: design, newtype, type-safety, orphan-rules
---

## Newtype Wrapper Pattern

Wrap primitive types or foreign types in single-field tuple structs to add type safety, implement external traits, or provide semantic meaning.

**Why this pattern exists:**

1. **Type Safety**: Prevents mixing up semantically different values of the same underlying type
2. **Orphan Rule**: Allows implementing external traits on external types
3. **Zero-Cost**: Compiled away - no runtime overhead
4. **Encapsulation**: Hide internal representation

**Incorrect (primitive types lose semantics):**

```rust
// What does this function do? Are both u64s the same thing?
fn transfer(from: u64, to: u64, amount: u64) -> Result<(), Error> {
    // Easy to accidentally swap `from` and `to`!
}

// Calling code - which is the user? which is the amount?
transfer(123, 456, 1000)?;  // Hard to verify correctness
```

**Correct (newtypes enforce semantics):**

```rust
// Define newtypes for distinct concepts
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(pub u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Amount(pub u64);

fn transfer(from: UserId, to: UserId, amount: Amount) -> Result<(), Error> {
    // Cannot accidentally swap UserId with Amount - compile error!
}

// Calling code - crystal clear
transfer(UserId(123), UserId(456), Amount(1000))?;
```

**Correct (orphan rule workaround - impl external trait on external type):**

```rust
use serde::{Deserialize, Serialize};

// Cannot impl Deserialize for external `http::Uri` directly
// But CAN impl for our wrapper!
#[derive(Debug, Clone)]
pub struct ApiEndpoint(pub http::Uri);

impl<'de> Deserialize<'de> for ApiEndpoint {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        let uri = s.parse().map_err(serde::de::Error::custom)?;
        Ok(ApiEndpoint(uri))
    }
}
```

**Correct (with Deref for transparent access):**

```rust
use std::ops::Deref;

#[derive(Debug, Clone)]
pub struct Json<T>(pub T);

impl<T> Deref for Json<T> {
    type Target = T;

    fn deref(&self) -> &T {
        &self.0
    }
}

impl<T> Json<T> {
    pub fn into_inner(self) -> T {
        self.0
    }
}

// Usage: access T's methods directly through Json<T>
let json = Json(MyData { name: "test".into() });
println!("{}", json.name);  // Deref allows direct access
```

**Real-world example from Actix Web:**

```rust
// actix-web/src/types/json.rs
#[derive(Debug)]
pub struct Json<T>(pub T);

impl<T> ops::Deref for Json<T> {
    type Target = T;
    fn deref(&self) -> &T { &self.0 }
}

impl<T> ops::DerefMut for Json<T> {
    fn deref_mut(&mut self) -> &mut T { &mut self.0 }
}

// Enables impl FromRequest for Json<T> - extracting JSON bodies
// Enables impl Responder for Json<T> - returning JSON responses
```

**Guidelines:**

| Use Case                                  | Pattern                           |
| ----------------------------------------- | --------------------------------- |
| Different semantics, same underlying type | Newtype without Deref             |
| Wrapper for trait impl                    | Newtype + implement needed traits |
| Transparent wrapper                       | Newtype + Deref/DerefMut          |
| Conversion-focused                        | Newtype + From/Into               |

Reference: [Rust Book - Newtype Pattern](https://doc.rust-lang.org/book/ch19-04-advanced-types.html#using-the-newtype-pattern)
