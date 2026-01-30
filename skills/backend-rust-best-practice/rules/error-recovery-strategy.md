---
title: Error Recovery Strategies
impact: MEDIUM
impactDescription: resilience, fault tolerance, graceful degradation
tags: error-handling, retry, fallback, resilience
---

## Recovery Strategies

Define explicit strategies for handling errors, distinguishing between transient faults (recoverable) and permanent failures (unrecoverable).

**Why this pattern exists:**

1.  **Resilience**: Systems should withstand transient network blips or timeouts.
2.  **Reliability**: Automatic recovery reduces manual intervention.

**Strategies:**

1.  **Retry**: For transient errors (network timeout, rate limit). Use exponential backoff.
2.  **Fallback**: Return a default value or cached data if the primary source fails.
3.  **Fail Fast**: For configuration errors or invariant violations.

**Example (Retry with Backoff):**

```rust
use std::time::Duration;
use tokio::time::sleep;

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
                // Exponential backoff: 100ms, 200ms, 400ms...
                sleep(Duration::from_millis(100 * 2u64.pow(attempt))).await;
            }
            Err(e) => return Err(e),  // Non-transient: fail fast
        }
    }
    Err(last_err.unwrap())
}
```

**Example (Fallback):**

```rust
async fn get_user_config(user_id: Uuid) -> UserConfig {
    match fetch_remote_config(user_id).await {
        Ok(config) => config,
        Err(e) => {
            log::warn!("Config fetch failed for {}, using default: {}", user_id, e);
            UserConfig::default()
        }
    }
}
```

**Guidelines:**

- **Idempotency**: Ensure retried operations are safe to execute multiple times.
- **Jitter**: Add random jitter to retry delays to prevent thundering herd effect.
- **Circuit Breaker**: Stop retrying if a service is down to prevent cascading failures.
