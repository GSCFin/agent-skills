# Backend Rust Best Practices

**Version 1.0.0**  
AgenticSE  
January 2026

> **Note:**  
> This document is for agents and LLMs to follow when maintaining, generating, or refactoring Rust backend applications. Patterns are derived from production codebases including Actix Web.

---

## Abstract

Comprehensive best practices guide for building production-grade Rust backend applications. Contains 19 rules across 6 categories, prioritized by impact from CRITICAL (Type-Driven Design, Error Handling) to MEDIUM (Configuration). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and references to production codebases.

---

## Table of Contents

1. [Type-Driven Design](#1-type-driven-design) — **CRITICAL**
   - 1.1 [Newtype Wrapper Pattern](#11-newtype-wrapper-pattern)
   - 1.2 [Type-State Pattern](#12-type-state-pattern)
   - 1.3 [Zero-Cost Abstractions](#13-zero-cost-abstractions)
2. [Error Handling](#2-error-handling) — **CRITICAL**
   - 2.1 [Structured Error Enums](#21-structured-error-enums)
   - 2.2 [Error Context Propagation](#22-error-context-propagation)
   - 2.3 [Recovery Strategies](#23-recovery-strategies)
3. [Concurrency](#3-concurrency) — **HIGH**
   - 3.1 [Shared State with Arc](#31-shared-state-with-arc)
   - 3.2 [Channel Patterns](#32-channel-patterns)
   - 3.3 [Async-Safe Mutex](#33-async-safe-mutex)
   - 3.4 [Graceful Shutdown](#34-graceful-shutdown)
4. [API Design](#4-api-design) — **HIGH**
   - 4.1 [Builder Pattern](#41-builder-pattern)
   - 4.2 [Into Conversions](#42-into-conversions)
   - 4.3 [Method Chaining](#43-method-chaining)
   - 4.4 [Custom Extractors](#44-custom-extractors)
5. [Trait-Based Architecture](#5-trait-based-architecture) — **MEDIUM**
   - 5.1 [Behavior Injection](#51-behavior-injection)
   - 5.2 [Object Safety](#52-object-safety)
   - 5.3 [Extension Traits](#53-extension-traits)
6. [Configuration](#6-configuration) — **MEDIUM**
   - 6.1 [Layered Middleware](#61-layered-middleware)
   - 6.2 [Environment-Driven Config](#62-environment-driven-config)
   - 6.3 [Observability & Tracing](#63-observability--tracing)

---

## 1. Type-Driven Design

**Impact: CRITICAL**

Use Rust's type system to encode domain constraints and prevent invalid states at compile time.

### 1.1 Newtype Wrapper Pattern

**Impact: CRITICAL (type safety, orphan rule compliance)**

Wrap primitive types in single-field structs to add semantic meaning, implement external traits, or prevent accidental misuse.

**Incorrect:**

```rust
// Easy to swap arguments - both are u64
fn transfer(from: u64, to: u64, amount: u64) -> Result<(), Error> { ... }
transfer(123, 456, 1000)?;  // Which is which?
```

**Correct:**

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(pub u64);

#[derive(Debug, Clone, Copy)]
pub struct Amount(pub u64);

fn transfer(from: UserId, to: UserId, amount: Amount) -> Result<(), Error> { ... }
transfer(UserId(123), UserId(456), Amount(1000))?;  // Crystal clear
```

**Real-world example (Actix Web):**

```rust
// actix-web wraps types to implement FromRequest/Responder
pub struct Json<T>(pub T);
pub struct Data<T: ?Sized>(Arc<T>);

impl<T> ops::Deref for Json<T> {
    type Target = T;
    fn deref(&self) -> &T { &self.0 }
}
```

---

### 1.2 Type-State Pattern

**Impact: HIGH (compile-time state machine validation)**

Encode allowed state transitions in the type system to prevent invalid operations.

**Incorrect:**

```rust
struct Connection {
    state: ConnectionState,  // Runtime check
}

impl Connection {
    fn send(&self, data: &[u8]) -> Result<(), Error> {
        if self.state != ConnectionState::Open {
            return Err(Error::NotConnected);  // Runtime error
        }
        // ...
    }
}
```

**Correct:**

```rust
struct Closed;
struct Open;

struct Connection<State> {
    inner: TcpStream,
    _state: PhantomData<State>,
}

impl Connection<Closed> {
    fn connect(addr: &str) -> Result<Connection<Open>, Error> {
        let stream = TcpStream::connect(addr)?;
        Ok(Connection { inner: stream, _state: PhantomData })
    }
}

impl Connection<Open> {
    fn send(&mut self, data: &[u8]) -> Result<(), Error> {
        self.inner.write_all(data)?;
        Ok(())
    }

    fn close(self) -> Connection<Closed> {
        Connection { inner: self.inner, _state: PhantomData }
    }
}

// Compile error: Connection<Closed> doesn't have send()
// let conn = Connection::new();
// conn.send(b"hello");  // Error!
```

---

### 1.3 Zero-Cost Abstractions

**Impact: MEDIUM (performance with abstraction)**

Use generics and traits to write abstract code that compiles to the same assembly as hand-written specialized code.

```rust
// Generic - compiles to specialized versions per type
fn process<T: Serialize>(item: T) -> Vec<u8> {
    serde_json::to_vec(&item).unwrap()
}

// Monomorphization creates:
// fn process_user(item: User) -> Vec<u8>
// fn process_order(item: Order) -> Vec<u8>
```

---

## 2. Error Handling

**Impact: CRITICAL**

Structured error handling with proper context and recovery strategies.

### 2.1 Structured Error Enums

**Impact: CRITICAL (exhaustive handling, type safety)**

Use `thiserror` for library errors, `anyhow` for application errors.

**Incorrect:**

```rust
fn load_config(path: &str) -> Result<Config, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| format!("Failed to read: {}", e))?;
    // String errors - no structured handling
}
```

**Correct:**

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("Failed to read config: {path}")]
    IoError {
        path: String,
        #[source]
        source: std::io::Error,
    },

    #[error("Invalid JSON")]
    ParseError(#[from] serde_json::Error),

    #[error("Missing field: {0}")]
    MissingField(String),
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|source| ConfigError::IoError {
            path: path.into(),
            source
        })?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}
```

---

### 2.2 Error Context Propagation

**Impact: HIGH (debugging, error messages)**

Add context when propagating errors using `anyhow::Context`.

```rust
use anyhow::{Context, Result};

fn initialize_app() -> Result<()> {
    let config = load_config("app.json")
        .context("Failed to load application configuration")?;

    let db = connect_database(&config.db_url)
        .with_context(|| format!("Failed to connect to database: {}", config.db_url))?;

    Ok(())
}
```

---

### 2.3 Recovery Strategies

**Impact: MEDIUM (resilience)**

Define explicit strategies for recoverable vs unrecoverable errors.

```rust
async fn fetch_with_retry<T, F, Fut>(mut f: F, retries: u32) -> Result<T, Error>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, Error>>,
{
    let mut last_err = None;
    for attempt in 0..retries {
        match f().await {
            Ok(result) => return Ok(result),
            Err(e) if e.is_transient() => {
                last_err = Some(e);
                tokio::time::sleep(Duration::from_millis(100 * 2u64.pow(attempt))).await;
            }
            Err(e) => return Err(e),  // Non-transient: fail fast
        }
    }
    Err(last_err.unwrap())
}
```

---

## 3. Concurrency

**Impact: HIGH**

Safe patterns for concurrent and parallel Rust code.

### 3.1 Shared State with Arc

**Impact: CRITICAL (thread safety)**

Create shared state outside worker closures to ensure single instance across threads.

**Incorrect:**

```rust
HttpServer::new(|| {
    let counter = Arc::new(AtomicU64::new(0));  // Per-worker!
    App::new().app_data(counter)
})
```

**Correct:**

```rust
let counter = Arc::new(AtomicU64::new(0));  // Single instance

HttpServer::new(move || {
    App::new().app_data(counter.clone())  // Arc clone is cheap
})
```

---

### 3.2 Channel Patterns

**Impact: HIGH (avoiding shared state complexity)**

Prefer message passing over shared state when feasible.

```rust
use tokio::sync::mpsc;

enum Command {
    Increment,
    Get(oneshot::Sender<u64>),
}

async fn counter_actor(mut rx: mpsc::Receiver<Command>) {
    let mut count = 0u64;
    while let Some(cmd) = rx.recv().await {
        match cmd {
            Command::Increment => count += 1,
            Command::Get(reply) => { let _ = reply.send(count); }
        }
    }
}

// Usage
let (tx, rx) = mpsc::channel(100);
tokio::spawn(counter_actor(rx));

tx.send(Command::Increment).await?;
```

---

### 3.3 Async-Safe Mutex

**Impact: HIGH (avoiding deadlocks)**

Use `tokio::sync::Mutex` when holding locks across `.await` points.

**Incorrect:**

```rust
use std::sync::Mutex;

async fn handler(data: web::Data<Mutex<State>>) {
    let state = data.lock().unwrap();
    // Holding std::sync::Mutex across await - BAD!
    db.query(&state.query).await;
}
```

**Correct:**

```rust
use tokio::sync::Mutex;

async fn handler(data: web::Data<Mutex<State>>) {
    let state = data.lock().await;  // Async-aware
    db.query(&state.query).await;   // Safe to hold across await
}
```

---

### 3.4 Graceful Shutdown

**Impact: HIGH (data integrity)**

Implement coordinated shutdown using cancellation tokens and signal handling.

```rust
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let token = CancellationToken::new();
    let cloned_token = token.clone();

    tokio::spawn(async move {
        tokio::select! {
            _ = cloned_token.cancelled() => println!("Shutting down worker"),
            _ = do_work() => {},
        }
    });

    tokio::signal::ctrl_c().await.unwrap();
    token.cancel();
    // Wait for tasks to finish...
}
```

---

## 4. API Design

**Impact: HIGH**

Ergonomic and flexible API patterns.

### 4.1 Builder Pattern

**Impact: HIGH (ergonomics, validation)**

Use builders for types with many optional fields.

```rust
pub struct ServerConfig { /* ... */ }

impl ServerConfigBuilder {
    pub fn new() -> Self { Self::default() }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn build(self) -> Result<ServerConfig, Error> {
        Ok(ServerConfig {
            host: self.host.ok_or(Error::MissingField("host"))?,
            port: self.port.unwrap_or(8080),
        })
    }
}

// Usage
let config = ServerConfigBuilder::new()
    .host("0.0.0.0")
    .port(8080)
    .build()?;
```

---

### 4.2 Into Conversions

**Impact: MEDIUM (API flexibility)**

Accept `impl Into<T>` for more flexible APIs.

```rust
// Rigid
fn greet(name: String) { println!("Hello, {}", name); }
greet("World".to_string());  // Must convert

// Flexible
fn greet(name: impl Into<String>) { println!("Hello, {}", name.into()); }
greet("World");  // &str works
greet(String::from("World"));  // String works too
```

---

### 4.3 Method Chaining

**Impact: MEDIUM (fluent APIs)**

Return `Self` for fluent interfaces.

```rust
impl QueryBuilder {
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

// Fluent usage
let query = QueryBuilder::new()
    .select(&["id", "name"])
    .from("users")
    .where_eq("status", "active")
    .build();
```

---

### 4.4 Custom Extractors

**Impact: HIGH (clean handlers)**

Implement `FromRequest` to extract data declaratively, keeping handlers clean.

**Incorrect:**

```rust
async fn handler(req: HttpRequest) {
    let token = req.headers().get("Authorization").unwrap(); // Logic in handler
    // ...
}
```

**Correct:**

```rust
struct AuthenticatedUser(UserId);

impl FromRequest for AuthenticatedUser {
    // ... impl from_request ...
}

async fn handler(user: AuthenticatedUser) {
    // Logic starts immediately
}
```

---

## 5. Trait-Based Architecture

**Impact: MEDIUM**

Using traits for abstraction and extensibility.

### 5.1 Behavior Injection

**Impact: HIGH (testability, decoupling)**

Define behavior via traits for dependency injection.

```rust
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error>;
}

// Production
struct PostgresRepo { pool: PgPool }

#[async_trait]
impl UserRepository for PostgresRepo {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id.0)
            .fetch_optional(&self.pool)
            .await
            .map_err(Into::into)
    }
}

// Test
struct MockRepo { users: HashMap<UserId, User> }

#[async_trait]
impl UserRepository for MockRepo {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error> {
        Ok(self.users.get(&id).cloned())
    }
}
```

---

### 5.2 Object Safety

**Impact: MEDIUM (dynamic dispatch)**

Design traits for `dyn Trait` when runtime polymorphism needed.

```rust
// Object-safe: can use Box<dyn Handler>
trait Handler: Send + Sync {
    fn handle(&self, req: Request) -> Response;
}

// NOT object-safe: has generic method
trait Handler {
    fn handle<R: Request>(&self, req: R) -> Response;  // Can't use dyn
}
```

---

### 5.3 Extension Traits

**Impact: MEDIUM (extending foreign types)**

Add methods to foreign types via extension traits.

```rust
pub trait StringExt {
    fn truncate_ellipsis(&self, max_len: usize) -> String;
}

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
let title = "Very long title here".truncate_ellipsis(10);
```

---

## 6. Configuration

**Impact: MEDIUM**

Configuration and middleware patterns.

### 6.1 Layered Middleware

**Impact: MEDIUM (separation of concerns)**

Use middleware layers for cross-cutting concerns.

```rust
App::new()
    .wrap(NormalizePath::trim())      // 1st: normalize paths
    .wrap(Compress::default())        // 2nd: compress
    .wrap(Logger::default())          // 3rd: log
    .wrap(from_fn(auth_middleware))   // 4th: auth
```

---

### 6.2 Environment-Driven Config

**Impact: MEDIUM (12-factor compliance)**

Load configuration from environment variables.

```rust
use config::{Config, Environment, File};

#[derive(Deserialize)]
pub struct Settings {
    pub database_url: String,
    pub port: u16,
}

impl Settings {
    pub fn new() -> Result<Self, config::ConfigError> {
        Config::builder()
            .add_source(File::with_name("config/default"))
            .add_source(File::with_name(&format!("config/{}", env)).required(false))
            .add_source(Environment::with_prefix("APP"))
            .build()?
            .try_deserialize()
    }
}
```

---

### 6.3 Observability & Tracing

**Impact: HIGH (debugging, monitoring)**

Use the `tracing` ecosystem for structured, async-aware logging.

```rust
use tracing::{info, instrument};

#[instrument(skip(data), fields(request_id = %uuid::Uuid::new_v4()))]
async fn handler(data: web::Data<AppState>, user_id: u32) {
    info!("Handling request"); // Includes user_id and request_id

    // ...
    db_query().await;

    info!("Finished");
}

// Setup
fn init_telemetry() {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json()
        .init();
}
```

---

## References

1. [Rust Book](https://doc.rust-lang.org/book/)
2. [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
3. [Actix Web Source](https://github.com/actix/actix-web)
4. [thiserror crate](https://docs.rs/thiserror)
5. [Tokio Documentation](https://tokio.rs/)
