---
title: Zero-Cost Abstractions
impact: MEDIUM
impactDescription: high performance with high-level abstractions
tags: design, generics, traits, optimization
---

## Zero-Cost Abstractions

Use generics and traits to write abstract code that compiles to the same assembly as hand-written specialized code.

**Why this pattern exists:**

1.  **Performance**: No runtime overhead for abstraction (monomorphization).
2.  **Reusability**: Write logic once for many types.
3.  **Static Dispatch**: Compiler resolves function calls, allowing inlining.

**Explanation:**

Rust's generics use _monomorphization_, meaning the compiler generates a specialized copy of the function for each concrete type used.

**Example:**

```rust
// Generic function - simpler to read and maintain
fn process<T: Serialize>(item: T) -> Vec<u8> {
    serde_json::to_vec(&item).unwrap()
}

// usage
process(my_user);
process(my_order);

// Comparison to what compiler generates (Conceptual):
// fn process_user(item: User) -> Vec<u8> { ... }
// fn process_order(item: Order) -> Vec<u8> { ... }
```

**Guidelines:**

- Prefer **generics** (`fn foo<T: Trait>(arg: T)`) when the type is known at compile time and you want static dispatch/inlining.
- Use **static dispatch** by default for libraries where performance matters.
- Remember that heavy use of generics can increase binary size (code bloat) since code is duplicated for each type.

**Real-world example:**

`Iterator` adapters in Rust (`map`, `filter`, `fold`) are zero-cost abstractions. They compile down to efficient loops comparable to hand-written C code.
