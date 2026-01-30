---
title: Into Conversions
impact: MEDIUM
impactDescription: flexible API usage, reduced caller boilerplate
tags: api, traits, conversion, usability
---

## Into Conversions

Accept `impl Into<T>` in function arguments to allow callers to pass different compatible types without manual conversion.

**Why this pattern exists:**

1.  **Flexibility**: Callers can pass `String`, `&str`, `Box<str>`, `Cow<str>`, etc.
2.  **Cleanliness**: Removes `.into()` or `.to_string()` calls from the call site.

**Incorrect (rigid types):**

```rust
fn greet(name: String) {
    println!("Hello, {}", name);
}

// Caller code
greet("World".to_string()); // Annoying allocation/conversion
```

**Correct (flexible types):**

```rust
fn greet(name: impl Into<String>) {
    let name = name.into(); // Convert internally
    println!("Hello, {}", name);
}

// Caller code
greet("World"); // Clean, works with &str
greet(String::from("World")); // Works with String
```

**Guidelines:**

- Use for logic that _takes ownership_ of the data (consumers).
- Commonly used with `PathBuf` (argument `impl Into<PathBuf>`) and `String`.
- Don't use if the function simply needs a reference (use `&str` or `&Path` instead).
