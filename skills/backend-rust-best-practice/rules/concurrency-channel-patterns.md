---
title: Channel Patterns (Message Passing)
impact: HIGH
impactDescription: reduced complexity, actor model, safe state management
tags: concurrency, channels, mpsc, actor
---

## Channel Patterns

Prefer message passing (channels) over shared mutable state (mutexes) when synchronizing threads or concurrent tasks.

**Why this pattern exists:**

1.  **Simplicity**: "Do not communicate by sharing memory; instead, share memory by communicating." (Go proverb, applicable to Rust).
2.  **Decoupling**: Producers and consumers are decoupled.
3.  **Ownership**: Ownership of data is transferred between threads/tasks, preventing race conditions.

**Example (Actor Pattern):**

```rust
use tokio::sync::{mpsc, oneshot};

enum Command {
    Increment,
    Get(oneshot::Sender<u64>),
}

async fn counter_actor(mut rx: mpsc::Receiver<Command>) {
    let mut count = 0u64;
    while let Some(cmd) = rx.recv().await {
        match cmd {
            Command::Increment => count += 1,
            Command::Get(reply) => {
                let _ = reply.send(count);
            }
        }
    }
}

// Usage
#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::channel(100);
    tokio::spawn(counter_actor(rx));

    tx.send(Command::Increment).await.unwrap();

    let (resp_tx, resp_rx) = oneshot::channel();
    tx.send(Command::Get(resp_tx)).await.unwrap();

    let count = resp_rx.await.unwrap();
    println!("Count: {}", count);
}
```

**Guidelines:**

- Use `mpsc` (multi-producer, single-consumer) for work queues or actors.
- Use `oneshot` for returning a response from an actor.
- Use `broadcast` for fan-out (one sender, multiple receivers).
- Channels handle backpressure (bounded channels) which limits memory usage.
