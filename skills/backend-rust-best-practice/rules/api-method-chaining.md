---
title: Method Chaining
impact: MEDIUM
impactDescription: fluent interfaces, readable configuration
tags: api, builder, chaining, fluent
---

## Method Chaining

Return `Self` (or `&mut Self`) from setter methods to allow method chaining, creating a "fluent interface".

**Why this pattern exists:**

1.  **Readability**: Configuration reads like a sentence or a list of steps.
2.  **Conciseness**: Avoids repeating the variable name for every setting.

**Example (Query Builder):**

```rust
pub struct QueryBuilder {
    columns: Vec<String>,
    table: String,
    conditions: Vec<String>,
}

impl QueryBuilder {
    pub fn new() -> Self { ... }

    // Consuming builder (returns Self)
    pub fn select(mut self, columns: &[&str]) -> Self {
        self.columns = columns.iter().map(|s| s.to_string()).collect();
        self
    }

    pub fn from(mut self, table: &str) -> Self {
        self.table = table.to_string();
        self
    }

    pub fn where_eq(mut self, col: &str, val: &str) -> Self {
        self.conditions.push(format!("{} = '{}'", col, val));
        self
    }
}

// Usage
let query = QueryBuilder::new()
    .select(&["id", "name"])
    .from("users")
    .where_eq("status", "active")
    .build();
```

**Guidelines:**

- **Consuming builders** (`fn method(self) -> Self`) are preferred when the intermediate steps are not useful (typical configuration builders).
- **Non-consuming** (`fn method(&mut self) -> &mut Self`) are useful when modifying a long-lived object inline.
