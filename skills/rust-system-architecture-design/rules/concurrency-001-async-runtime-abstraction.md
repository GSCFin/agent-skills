# Async Runtime Abstraction

**Category**: Concurrency
**Context**: Your library needs to spawn tasks or perform I/O, but you don't want to force a specific runtime (Tokio, async-std, smol) on your users.
**Source**: Extracted from **Tokio** and generic Rust async patterns.

## The Problem

Rust's `Future` is runtime-agnostic, but `spawn`, `machine-local I/O` traits (`AsyncRead`), and `Timer` facilities often depend on a specific reactor (e.g., Tokio's global reactor). Hardcoding `tokio::spawn` limits your library's usability.

## The Solution

### 1. Abstracting Spawning

Require the user to provide a spawner via a trait, or return the Future for the user to spawn.

**Preferred**: Return the Future (Let the caller decide how to run it).

```rust
// Good: Runtime agnostic
pub async fn process_data() -> Result<(), Error> { ... }

// Usage
tokio::spawn(process_data());
// OR
smol::spawn(process_data());
```

### 2. Abstracting I/O Traits

Use the `futures-io` or `tokio-util` compatibility layers if you need to support multiple concrete I/O traits, but prefer purely polling interfaces where possible.

### 3. Feature-Flagged Runtimes

If you _must_ use specific runtime features (like `input handling`), expose them via Cargo features.

```toml
[features]
default = []
runtime-tokio = ["tokio", "tokio-util"]
runtime-async-std = ["async-std"]
```

```rust
#[cfg(feature = "runtime-tokio")]
pub fn run() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(async_main());
}
```

## Reference Patterns (Tokio)

Tokio uses a `Handle` to abstract access to the reactor.

```rust
// tokio/src/runtime/handle.rs
pub struct Handle {
    pub(super) inner: scheduler::Handle,
}

impl Handle {
    pub fn current() -> Self {
        // Panics if no runtime is set
        context::current()
    }

    pub fn spawn<F>(&self, future: F) -> JoinHandle<F::Output> {
        self.inner.spawn(future, ...)
    }
}
```
