---
title: Structured Error Enums with thiserror
impact: CRITICAL
impactDescription: exhaustive handling, context preservation, clean APIs
tags: error, thiserror, enum, result
---

## Structured Error Enums with thiserror

Define error types as enums with the `thiserror` crate for automatic Display/Error derives, source chaining, and exhaustive match handling.

**Why this pattern exists:**

1. **Exhaustive Matching**: Compiler enforces handling all error cases
2. **Type Safety**: Different errors have different types
3. **Context Preservation**: Chain underlying errors with `#[from]`
4. **Clean APIs**: Automatic `Display` and `Error` impls

**Incorrect (string errors lose information):**

```rust
fn load_config(path: &str) -> Result<Config, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| format!("Failed to read file: {}", e))?;

    let config: Config = serde_json::from_str(&content)
        .map_err(|e| format!("Failed to parse JSON: {}", e))?;

    Ok(config)
}

// Caller: No way to distinguish IO error from parse error
match load_config("app.json") {
    Ok(c) => use_config(c),
    Err(s) => println!("{}", s),  // String - no structured handling
}
```

**Correct (structured enum with thiserror):**

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("Failed to read config file: {path}")]
    IoError {
        path: String,
        #[source]
        source: std::io::Error,
    },

    #[error("Failed to parse config as JSON")]
    ParseError(#[from] serde_json::Error),

    #[error("Missing required field: {0}")]
    MissingField(String),

    #[error("Invalid value for {field}: expected {expected}, got {actual}")]
    InvalidValue {
        field: String,
        expected: String,
        actual: String,
    },
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|source| ConfigError::IoError {
            path: path.to_string(),
            source,
        })?;

    let config: Config = serde_json::from_str(&content)?;  // Auto-converts via #[from]

    Ok(config)
}

// Caller: Can handle specific error cases
match load_config("app.json") {
    Ok(c) => use_config(c),
    Err(ConfigError::IoError { path, .. }) => eprintln!("Check file: {}", path),
    Err(ConfigError::ParseError(e)) => eprintln!("Fix JSON syntax: {}", e),
    Err(ConfigError::MissingField(f)) => eprintln!("Add field: {}", f),
    Err(e) => eprintln!("Config error: {}", e),
}
```

**Correct (for library APIs - anyhow for applications):**

```rust
// For LIBRARIES: use thiserror with specific types
#[derive(Debug, Error)]
pub enum ServiceError {
    #[error("Database error")]
    Database(#[from] sqlx::Error),

    #[error("External API failed: {0}")]
    ExternalApi(String),

    #[error("Rate limit exceeded")]
    RateLimited,
}

// For APPLICATIONS: use anyhow for convenient error aggregation
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let config = load_config("app.json")
        .context("Failed to initialize application")?;

    run_server(config)
        .context("Server crashed")?;

    Ok(())
}
```

**Real-world example from Actix Web:**

```rust
// actix-web error pattern
#[derive(Debug, Display, Error)]
pub enum JsonPayloadError {
    #[display("Json deserialize error: {_0}")]
    Deserialize(serde_json::Error),

    #[display("Payload error: {_0}")]
    Payload(PayloadError),

    #[display("Content type error: {_0}")]
    ContentType(ContentTypeError),
}

impl ResponseError for JsonPayloadError {
    fn status_code(&self) -> StatusCode {
        match self {
            Self::Deserialize(_) => StatusCode::BAD_REQUEST,
            Self::Payload(e) => e.status_code(),
            Self::ContentType(_) => StatusCode::BAD_REQUEST,
        }
    }
}
```

**Guidelines:**

| Scenario         | Approach                                   |
| ---------------- | ------------------------------------------ |
| Library code     | `thiserror` with specific error enums      |
| Application code | `anyhow` with `.context()` for wrapping    |
| Mixed            | Library errors + anyhow at boundaries      |
| HTTP responses   | Impl `ResponseError` (or equivalent) trait |

Reference: [thiserror crate](https://docs.rs/thiserror) | [anyhow crate](https://docs.rs/anyhow)
