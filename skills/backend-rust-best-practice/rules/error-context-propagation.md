---
title: Error Context Propagation
impact: HIGH
impactDescription: improved debugging, better error messages, clear causal chain
tags: error-handling, anyhow, context, debugging
---

## Error Context Propagation

Add context when propagating errors up the stack, typically using `anyhow::Context` for applications, to answer "what was being attempted when the error occurred?"

**Why this pattern exists:**

1.  **Debuggability**: A low-level error like `No such file or directory` is useless without knowing _which_ file and _why_ it was being read.
2.  **User Experience**: Provides a chain of context leading to the root cause.

**Incorrect (blind propagation):**

```rust
fn initialize_app() -> Result<()> {
    let config = load_config("app.json")?; // If this fails, we just get "IO Error"
    let db = connect_database(&config.db_url)?;
    Ok(())
}
```

**Correct (adding context):**

```rust
use anyhow::{Context, Result};

fn initialize_app() -> Result<()> {
    let config = load_config("app.json")
        .context("Failed to load application configuration")?;

    let db = connect_database(&config.db_url)
        .with_context(|| format!("Failed to connect to database at {}", config.db_url))?;

    Ok(())
}
```

**Output difference:**

- _Without context:_ `Error: No such file or directory (os error 2)`
- _With context:_ `Error: Failed to load application configuration caused by: No such file or directory (os error 2)`

**Guidelines:**

- Use `anyhow` for **applications** (binaries).
- Use `thiserror` for **libraries** (where you want structured errors).
- Only add context that adds _new_ information. Don't add "failed to read file" if the function name is `read_file` unless you add the _path_.
