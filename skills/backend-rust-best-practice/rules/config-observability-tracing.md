---
title: Structured Logging with Tracing
impact: HIGH
impactDescription: observability, debugging across async tasks, structured logs
tags: observability, tracing, logging, async, debugging
---

## Structured Logging with Tracing

Use the `tracing` ecosystem (instead of simple `log`) for structured, async-aware logging and diagnostics.

**Why this pattern exists:**

1.  **Async Awareness**: Standard loggers mix output from different async tasks. `tracing` preserves the concept of a "Span" (context) across async yield points.
2.  **Structured Data**: Logs key-value pairs (`user_id=123`), which are easier to query than unstructured strings.
3.  **Instrumentation**: `#[instrument]` macro automatically creates spans for function calls with arguments.

**Incorrect (std logging in async):**

```rust
// Basic logging loses context in async interleaving
async fn handler(user_id: u32) {
    log::info!("Handling request");
    // ... complicated async work ...
    log::info!("Finished"); // Which request finished?
}
```

**Correct (tracing):**

```rust
use tracing::{info, instrument};

#[instrument(skip(data), fields(request_id = %uuid::Uuid::new_v4()))]
async fn handler(data: web::Data<AppState>, user_id: u32) {
    info!("Handling request"); // Includes user_id and request_id automatically

    // ...
    db_query().await;
    // ...

    info!("Finished");
}

// Setup (usually in main)
fn init_telemetry() {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json() // Production: JSON logs
        .init();
}
```

**Guidelines:**

- **Spans**: Wrap units of work (HTTP requests, background jobs) in Spans.
- **Fields**: Attach data to spans/events (`info!(user.id = %user_id, "Logged in")`).
- **Environment**: Use `RUST_LOG=info,my_app=debug` to control verbosity dynamically.
- **Formatting**: Use JSON formatter for production (ingestion by ELK/Datadog), compact/pretty for local dev.
