---
title: Object Safety (Dynamic Dispatch)
impact: MEDIUM
impactDescription: enables runtime polymorphism, trait objects
tags: trait, dynamic-dispatch, polymorphism, object-safe
---

## Object Safety

Design traits to be "object-safe" if you intend to use them for runtime polymorphism (e.g., `Box<dyn Trait>` or `Arc<dyn Trait>`).

**Why this pattern exists:**

1.  **Polymorphism**: Treat different types uniformly at runtime (e.g., a list of `Box<dyn Plugin>`).
2.  **Plugin Systems**: Load implementations dynamically.
3.  **Compile-Time Limits**: Avoid code bloat from over-monomorphization or when types are not known at compile time.

**Rules for Object Safety:**

A trait is object-safe if:

1.  It does not require `Sized` as a supertrait.
2.  All methods do NOT take `self` by value (receiver must be `&self`, `&mut self`, `Box<Self>`, etc.).
3.  All methods do NOT have generic type parameters.
4.  All methods do NOT use `Self` in return position.

**Incorrect (not object safe):**

```rust
trait Handler {
    // Problem 1: Generic parameter
    fn handle<R: Request>(&self, req: R) -> Response;

    // Problem 2: Returning Self
    fn clone_me(&self) -> Self;
}

// Cannot do this:
// let h: Box<dyn Handler> = ...; // Error!
```

**Correct (object safe):**

```rust
// Use dynamic dispatch for arguments when possible
trait Handler: Send + Sync {
    fn handle(&self, req: Box<dyn Request>) -> Response;
}

// Now safe to use:
fn register(handler: Box<dyn Handler>) {
    // ...
}
```

**Workaround for Generics:**
If a method needs to be generic, you can sometimes move it to a separate trait or use `erased-serde` style type erasure.
