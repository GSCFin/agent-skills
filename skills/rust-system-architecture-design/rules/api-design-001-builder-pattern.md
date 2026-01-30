---
id: api-design-001-builder-pattern
title: Use the Builder Pattern for Complex Configuration
impact: HIGH
---

# Use the Builder Pattern for Complex Configuration

## Context

Structs with many configuration options or optional parameters are difficult to initialize directly. Using `new()` with dozens of arguments is unreadable and fragile.

## Rule

Use the **Builder Pattern** to separate object construction from its representation.

1.  Create a `Builder` struct (or allow the main struct to act as its own builder).
2.  Provide fluent methods (returning `Self` or `&mut Self`) for setting options.
3.  Provide a `build()` or `finish()` method to validate state and produce the final object.

## Examples

### Incorrect Code

Functions with "boolean soup" or many `Option` arguments.

```rust
// BAD: Too many arguments
let cmd = Command::new(
    "my-prog",
    Some("1.0"),
    Some("A cool program"),
    true, // colors?
    false, // verbose?
    true, // async?
);
```

### Correct Code

Fluent Builder interface.

```rust
// GOOD: Clear, readable configuration
let cmd = Command::new("my-prog")
    .version("1.0")
    .about("A cool program")
    .color(ColorChoice::Auto)
    .verbose(false)
    .build();
```

## Champion Project: Clap

Clap extensively uses the Builder pattern for defining CLI arguments:

```rust
Command::new("git")
    .arg(Arg::new("verbose").short('v'))
    .subcommand(Command::new("commit"))
    .get_matches();
```
