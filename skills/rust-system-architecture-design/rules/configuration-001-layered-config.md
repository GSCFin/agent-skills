---
id: configuration-001-layered-config
title: Implement Layered Configuration Priority
impact: MEDIUM
---

# Implement Layered Configuration Priority

## Context

Applications often need to run in various environments (Dev, Test, Prod) and accept configuration from multiple sources. Ad-hoc handling of `env::var` vs CLI args vs struct defaults leads to inconsistent behavior.

## Rule

Implement a **Layered Configuration** strategy with strict precedence.

1.  **Defaults** (Lowest priority, hardcoded).
2.  **Configuration File** (e.g., `config.toml`, user settings).
3.  **Environment Variables** (Docker/CI overrides).
4.  **CLI Arguments** (Highest priority, explicit user override).

Use a "Configuration Object" pattern to merge these layers into a final, immutable struct using `serde`.

## Examples

### Incorrect Code

Manual checking and shadowing.

```rust
let port = if let Some(p) = args.port {
    p
} else if let Ok(p) = env::var("PORT") {
    p.parse()?
} else {
    8080
};
```

### Correct Code

Layered merging (conceptual usage of `config` crate or similar).

```rust
let config = Config::builder()
    .set_default("port", 8080)?
    .add_source(File::with_name("app"))
    .add_source(Environment::with_prefix("APP"))
    .build()?;

let settings: AppSettings = config.try_deserialize()?;
```

## Champion Project: Deno

Deno uses a `Flags` struct (analyzed in `cli/args/flags.rs`) that consolidates CLI arguments, environment variables, and config files into a single source of truth for the runtime.
