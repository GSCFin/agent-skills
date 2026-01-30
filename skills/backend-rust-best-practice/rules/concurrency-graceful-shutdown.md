---
title: Graceful Shutdown Patterns
impact: HIGH
impactDescription: zero-downtime deployments, data integrity, proper resource cleanup
tags: concurrency, shutdown, signal, kubernetes, tokio
---

## Graceful Shutdown Patterns

Implement coordinated shutdown to stop accepting new requests, finish active tasks, and release resources properly.

**Why this pattern exists:**

1.  **Data Integrity**: Don't kill active database writes or jobs mid-flight
2.  **Zero-Downtime**: Load balancers need time to drain connections
3.  **Resource Cleanup**: Flush logs, close sockets, commit transactions
4.  **Orchestration**: Kubernetes sends SIGTERM and expects clean exit

**Incorrect (hard exit):**

```rust
#[tokio::main]
async fn main() {
    let app = start_app().await;

    // ❌ Ctrl+C or SIGTERM kills process immediately
    // Active requests are dropped!
    // Database connections may remain open!
    // Logs may be lost!
    tokio::signal::ctrl_c().await.unwrap();
    std::process::exit(0);
}
```

**Correct (Token-based cancellation):**

Use `tokio_util::sync::CancellationToken` for coordinated shutdown of background tasks.

```rust
use tokio_util::sync::CancellationToken;
use tokio::signal;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let token = CancellationToken::new();
    let cloned_token = token.clone();

    // Spawn background worker
    let worker_handle = tokio::spawn(async move {
        loop {
            tokio::select! {
                _ = cloned_token.cancelled() => {
                    println!("Worker shutting down...");
                    break;
                }
                _ = do_work() => {}
            }
        }
        println!("Worker exited cleanly.");
    });

    // Wait for signal
    match signal::ctrl_c().await {
        Ok(()) => println!("Signal received, starting shutdown..."),
        Err(err) => eprintln!("Unable to listen for shutdown signal: {}", err),
    }

    // Trigger cancellation
    token.cancel();

    // Wait for worker to finish (with timeout)
    let _ = tokio::time::timeout(Duration::from_secs(5), worker_handle).await;
    println!("Shutdown complete.");
    Ok(())
}
```

**Correct (Actix Web automatic shutdown):**

Actix Web handles HTTP draining automatically, but you must handle your custom background tasks.

```rust
#[tokio::main]
async fn main() -> std::io::Result<()> {
    let db_pool = create_pool().await;
    let (tx, mut rx) = mpsc::channel(100);

    let server = HttpServer::new(move || {
        App::new().app_data(db_pool.clone())
    })
    .bind("127.0.0.1:8080")?
    .run();

    // Handle signals manually to coordinate other tasks
    let srv_handle = server.handle();
    tokio::spawn(async move {
        signal::ctrl_c().await.unwrap();

        // 1. Stop accepting new HTTP requests
        srv_handle.stop(true).await; // true = graceful

        // 2. Signal background tasks to stop
        // ...
    });

    server.await
}
```

**Signal Handling Logic:**

1.  **Listen**: `tokio::signal::ctrl_c()` (SIGINT) or `unix::SignalKind::terminate()` (SIGTERM)
2.  **Broadcast**: Notify all components (CancellationToken, broadcast channel, or AtomicBool)
3.  **Drain**: Components finish current unit of work and stop looping
4.  **Wait**: Main thread waits for all JoinHandles (often using `JoinSet`)
5.  **Force**: Set a hard timeout (e.g., 30s) to `std::process::exit` if tasks are stuck

**Guidelines:**

| Component   | Shutdown Action                                        |
| ----------- | ------------------------------------------------------ |
| HTTP Server | Stop listener, wait for active requests to complete    |
| Consumers   | Stop pulling from queue, finish current job            |
| Producers   | Flush buffers, close channels                          |
| Database    | Return connections to pool (automatic on drop usually) |
