---
title: Environment-Driven Configuration
impact: MEDIUM
impactDescription: 12-factor compliance, deployment flexibility
tags: config, environment, 12-factor, serialization
---

## Environment-Driven Configuration

Load configuration primarily from environment variables (compliant with 12-Factor App methodology), often supported by configuration files for defaults.

**Why this pattern exists:**

1.  **Deployment**: Docker/K8s/Cloud environments rely on env vars for secrets and config.
2.  **Security**: Secrets (DB passwords) should not be committed to code or static files.
3.  **Flexibility**: Change behavior without recompiling.

**Example (using `config` crate):**

```rust
use config::{Config, Environment, File};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Settings {
    pub database_url: String,
    pub port: u16,
    pub debug: bool,
}

impl Settings {
    pub fn new() -> Result<Self, config::ConfigError> {
        let env = std::env::var("RUN_MODE").unwrap_or_else(|_| "development".into());

        Config::builder()
            // 1. Start with generic default
            .add_source(File::with_name("config/default"))
            // 2. Add environment-specific config (e.g., config/production.toml)
            .add_source(File::with_name(&format!("config/{}", env)).required(false))
            // 3. Override with Environment Variables (APP_PORT=9090)
            .add_source(Environment::with_prefix("APP").separator("__"))
            .build()?
            .try_deserialize()
    }
}
```

**Guidelines:**

- **Hierarchical**: Defaults -> Config File -> Environment Variables (Highest priority).
- **Prefixing**: Use prefixes (e.g., `APP_`) to avoid collisions.
- **Separators**: Use `__` for nested structs (e.g., `APP__DATABASE__HOST` maps to `database.host`).
