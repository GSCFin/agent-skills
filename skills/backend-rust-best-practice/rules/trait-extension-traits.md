---
title: Extension Traits
impact: MEDIUM
impactDescription: extending external types, standardizing utilities
tags: trait, extension, utility, external-types
---

## Extension Traits

Use extension traits to add methods to types you don't own (like standard library types or external crate types).

**Why this pattern exists:**

1.  **Orphan Rule**: You cannot implement an external trait for an external type.
2.  **Usability**: Adds convenience methods directly to the types ("dot usage") rather than utility functions.

**Example:**

```rust
// Define the extension trait
pub trait StringExt {
    fn truncate_ellipsis(&self, max_len: usize) -> String;
}

// Implement it for the target type
impl StringExt for str {
    fn truncate_ellipsis(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len - 3])
        }
    }
}

// Usage
fn main() {
    // Import the trait to see the method
    use crate::StringExt;

    let title = "This is a very long title that needs truncating";
    println!("{}", title.truncate_ellipsis(20));
    // "This is a very lo..."
}
```

**Guidelines:**

- Name extension traits with an `Ext` suffix (e.g., `ResultExt`, `StreamExt`).
- Keep them in scope only where needed to avoid pollution.
- Great for adding helper methods (e.g., specific `Result` handling) that feel native.
