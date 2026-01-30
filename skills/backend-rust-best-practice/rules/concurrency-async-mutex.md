---
title: Async-Safe Mutex
impact: HIGH
impactDescription: prevents deadlocks in async code, cleaner async flow
tags: concurrency, async, mutex, tokio, deadlock
---

## Async-Safe Mutex

Use `tokio::sync::Mutex` (or other async-aware mutexes) when you need to hold a lock across an `.await` point.

**Why this pattern exists:**

1.  **Deadlock Prevention**: Standard `std::sync::Mutex` blocks the **thread**. If you hold it across an `.await`, the runtime might schedule the same thread to acquire the lock again (deadlock) or starve other tasks.
2.  **Runtime Cooperation**: Async mutexes yield execution to the runtime instead of blocking the OS thread.

**Incorrect (blocking mutex across await):**

```rust
use std::sync::Mutex;

async fn handler(data: web::Data<Mutex<State>>) {
    let state = data.lock().unwrap(); // Blocks the worker thread!

    // BAD: Holding std::sync::Mutex across .await
    // While waiting for DB, this thread cannot do other work,
    // and if the DB call needs this thread to progress -> Deadlock.
    db.query(&state.query).await;
}
```

**Correct (async mutex):**

```rust
use tokio::sync::Mutex;

async fn handler(data: web::Data<Mutex<State>>) {
    let state = data.lock().await;  // Yields until lock acquired

    // SAFE: Holding async lock across await
    db.query(&state.query).await;
}
```

**Guidelines:**

- **Preferred**: Avoid locking across await points if possible. (e.g., Get data, release lock, _then_ await).
- **If needed**: Use `tokio::sync::Mutex`.
- **For simple data**: If not holding across await, `std::sync::Mutex` is often faster (less overhead) even in async code, but be very careful.
