---
title: Builder Pattern for Complex Configuration
impact: HIGH
impactDescription: ergonomic APIs, validation at build time, immutable results
tags: api, builder, configuration, ergonomics
---

## Builder Pattern for Complex Configuration

Use the builder pattern for types with many optional fields or complex construction logic. Return `Self` from methods for method chaining.

**Why this pattern exists:**

1. **Ergonomics**: Named methods clearer than positional arguments
2. **Optional Fields**: Some fields have defaults, some are required
3. **Validation**: Check invariants at build time, not runtime
4. **Immutability**: Final object can be immutable after construction

**Incorrect (too many constructor arguments):**

```rust
struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
    timeout_ms: u64,
    tls_enabled: bool,
    tls_cert_path: Option<String>,
    tls_key_path: Option<String>,
}

impl ServerConfig {
    // Unwieldy constructor - hard to remember argument order
    fn new(
        host: String,
        port: u16,
        max_connections: usize,
        timeout_ms: u64,
        tls_enabled: bool,
        tls_cert_path: Option<String>,
        tls_key_path: Option<String>,
    ) -> Self { ... }
}

// Calling code - which number is which?
let config = ServerConfig::new(
    "0.0.0.0".into(),
    8080,
    1000,
    30000,
    true,
    Some("/path/to/cert".into()),
    Some("/path/to/key".into()),
);
```

**Correct (builder pattern):**

```rust
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
    timeout_ms: u64,
    tls: Option<TlsConfig>,
}

pub struct TlsConfig {
    cert_path: String,
    key_path: String,
}

#[derive(Default)]
pub struct ServerConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    max_connections: usize,
    timeout_ms: u64,
    tls: Option<TlsConfig>,
}

impl ServerConfigBuilder {
    pub fn new() -> Self {
        Self {
            max_connections: 1000,  // sensible defaults
            timeout_ms: 30_000,
            ..Default::default()
        }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn max_connections(mut self, n: usize) -> Self {
        self.max_connections = n;
        self
    }

    pub fn timeout_ms(mut self, ms: u64) -> Self {
        self.timeout_ms = ms;
        self
    }

    pub fn tls(mut self, cert_path: impl Into<String>, key_path: impl Into<String>) -> Self {
        self.tls = Some(TlsConfig {
            cert_path: cert_path.into(),
            key_path: key_path.into(),
        });
        self
    }

    pub fn build(self) -> Result<ServerConfig, ConfigError> {
        Ok(ServerConfig {
            host: self.host.ok_or(ConfigError::MissingField("host"))?,
            port: self.port.ok_or(ConfigError::MissingField("port"))?,
            max_connections: self.max_connections,
            timeout_ms: self.timeout_ms,
            tls: self.tls,
        })
    }
}

// Calling code - clear and readable
let config = ServerConfigBuilder::new()
    .host("0.0.0.0")
    .port(8080)
    .max_connections(5000)
    .tls("/path/to/cert", "/path/to/key")
    .build()?;
```

**Real-world example from Actix Web:**

```rust
// actix-web App uses builder pattern
App::new()
    .app_data(web::Data::new(state))
    .wrap(middleware::Logger::default())
    .wrap(middleware::Compress::default())
    .service(
        web::scope("/api")
            .route("/users", web::get().to(list_users))
            .route("/users/{id}", web::get().to(get_user))
    )
    .default_service(web::to(not_found))

// HttpServer configuration
HttpServer::new(|| App::new())
    .workers(4)
    .keep_alive(Duration::from_secs(75))
    .client_request_timeout(Duration::from_secs(10))
    .bind("127.0.0.1:8080")?
    .run()
    .await
```

**Derive macro alternative (typed-builder crate):**

```rust
use typed_builder::TypedBuilder;

#[derive(TypedBuilder)]
pub struct ServerConfig {
    host: String,
    port: u16,
    #[builder(default = 1000)]
    max_connections: usize,
    #[builder(default = 30_000)]
    timeout_ms: u64,
    #[builder(default, setter(strip_option))]
    tls: Option<TlsConfig>,
}

// Auto-generated builder with compile-time required field checking
let config = ServerConfig::builder()
    .host("0.0.0.0".into())
    .port(8080)
    .tls(tls_config)
    .build();
```

**Guidelines:**

| Approach          | Use When                               |
| ----------------- | -------------------------------------- |
| Manual builder    | Complex validation, custom error types |
| typed-builder     | Simple structs, reduce boilerplate     |
| Default + setters | All fields optional with defaults      |

Reference: [Rust API Guidelines - Builders](https://rust-lang.github.io/api-guidelines/type-safety.html#c-builder)
