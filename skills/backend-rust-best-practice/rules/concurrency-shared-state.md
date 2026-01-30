---
title: Thread-Safe Shared State with Arc
impact: HIGH
impactDescription: safe concurrent access, proper synchronization
tags: concurrency, arc, mutex, rwlock, shared-state
---

## Thread-Safe Shared State with Arc

Use `Arc<Mutex<T>>` or `Arc<RwLock<T>>` for sharing mutable state across threads. Create shared state outside the worker closure to ensure single instance.

**Why this pattern exists:**

1. **Thread Safety**: Rust requires explicit synchronization for shared mutable state
2. **Reference Counting**: `Arc` enables multiple owners across threads
3. **Interior Mutability**: `Mutex`/`RwLock` provide synchronized mutable access
4. **Zero-Cost Ownership**: Compile-time checks, no runtime GC

**Incorrect (state not shared across workers):**

```rust
use std::sync::atomic::AtomicU64;

// Each worker thread gets its own counter!
HttpServer::new(|| {
    let counter = Arc::new(AtomicU64::new(0));  // Created per worker

    App::new()
        .app_data(counter)
        .route("/", web::get().to(handler))
})
.workers(4)  // 4 separate counters!
```

**Correct (shared state created outside closure):**

```rust
use std::sync::{atomic::{AtomicU64, Ordering}, Arc};

// Single counter shared by ALL workers
let counter = Arc::new(AtomicU64::new(0));

HttpServer::new(move || {
    App::new()
        .app_data(counter.clone())  // Arc::clone is cheap
        .route("/", web::get().to(handler))
})
.workers(4)  // All share the same counter
```

**Correct (Mutex for complex state):**

```rust
use std::sync::{Arc, Mutex};

struct AppState {
    users: Vec<User>,
    sessions: HashMap<String, Session>,
}

// Create outside closure for sharing
let state = Arc::new(Mutex::new(AppState {
    users: Vec::new(),
    sessions: HashMap::new(),
}));

HttpServer::new(move || {
    App::new()
        .app_data(state.clone())
        .route("/users", web::post().to(add_user))
})

async fn add_user(state: web::Data<Mutex<AppState>>, user: web::Json<User>) -> impl Responder {
    let mut state = state.lock().unwrap();
    state.users.push(user.into_inner());
    HttpResponse::Ok()
}
```

**Correct (RwLock for read-heavy workloads):**

```rust
use std::sync::{Arc, RwLock};

struct Cache {
    entries: HashMap<String, CacheEntry>,
}

let cache = Arc::new(RwLock::new(Cache::default()));

// Multiple readers can access simultaneously
async fn get_cached(cache: web::Data<RwLock<Cache>>, key: String) -> impl Responder {
    let cache = cache.read().unwrap();  // Read lock - shared
    match cache.entries.get(&key) {
        Some(entry) => HttpResponse::Ok().json(entry),
        None => HttpResponse::NotFound().finish(),
    }
}

// Writers get exclusive access
async fn set_cached(cache: web::Data<RwLock<Cache>>, entry: web::Json<CacheEntry>) -> impl Responder {
    let mut cache = cache.write().unwrap();  // Write lock - exclusive
    cache.entries.insert(entry.key.clone(), entry.into_inner());
    HttpResponse::Ok()
}
```

**Correct (tokio::sync::Mutex for async code):**

```rust
use tokio::sync::Mutex;

struct AsyncState {
    db: DatabaseConnection,
}

let state = Arc::new(Mutex::new(AsyncState { db: connect().await }));

async fn handler(state: web::Data<Mutex<AsyncState>>) -> impl Responder {
    // tokio::Mutex::lock() is async - won't block the runtime
    let mut state = state.lock().await;

    // Safe to hold lock across await points
    let result = state.db.query("SELECT ...").await;

    HttpResponse::Ok().json(result)
}
```

**When to use which:**

| Scenario                   | Type                         | Reason               |
| -------------------------- | ---------------------------- | -------------------- |
| Atomic counters            | `Arc<AtomicU64>`             | Lock-free, fastest   |
| Simple state, sync code    | `Arc<Mutex<T>>`              | Simple, sufficient   |
| Read-heavy workloads       | `Arc<RwLock<T>>`             | Multiple readers     |
| State held across `.await` | `Arc<tokio::sync::Mutex<T>>` | Async-safe           |
| Connection pools           | Dedicated pool type          | Pool handles locking |

**Real-world pattern from Actix Web:**

```rust
// actix-web/src/data.rs
pub struct Data<T: ?Sized>(Arc<T>);

impl<T> Data<T> {
    pub fn new(state: T) -> Data<T> {
        Data(Arc::new(state))
    }
}

impl<T: ?Sized> Clone for Data<T> {
    fn clone(&self) -> Data<T> {
        Data(Arc::clone(&self.0))
    }
}
```

Reference: [Rust Book - Shared State](https://doc.rust-lang.org/book/ch16-03-shared-state.html)
