---
title: Layered Middleware Architecture
impact: MEDIUM
impactDescription: separation of concerns, composability, reusability
tags: config, middleware, layers, service, transform
---

## Layered Middleware Architecture

Use middleware/layers to separate cross-cutting concerns (logging, auth, compression) from business logic. Compose middleware using the decorator pattern.

**Why this pattern exists:**

1. **Separation of Concerns**: Auth logic separate from business logic
2. **Composability**: Stack middleware in any order
3. **Reusability**: Same middleware across multiple services
4. **Testability**: Test layers independently

**Incorrect (cross-cutting concerns mixed in handlers):**

```rust
async fn get_user(req: HttpRequest, path: web::Path<i32>) -> impl Responder {
    // Auth check - duplicated in every handler
    let token = req.headers().get("Authorization")
        .ok_or(Error::Unauthorized)?;
    validate_token(token)?;

    // Logging - duplicated everywhere
    let start = Instant::now();

    // Actual business logic
    let user = db.find_user(path.into_inner()).await?;

    // More logging
    log::info!("get_user took {:?}", start.elapsed());

    Ok(web::Json(user))
}
```

**Correct (middleware layers):**

```rust
use actix_web::middleware::{from_fn, Logger, Next};

// Auth middleware
async fn auth_middleware<B: MessageBody>(
    req: ServiceRequest,
    next: Next<B>,
) -> Result<ServiceResponse<B>, Error> {
    // Check auth once, for all routes under this middleware
    let token = req.headers()
        .get("Authorization")
        .ok_or(Error::Unauthorized)?;

    validate_token(token)?;

    // Continue to next layer
    next.call(req).await
}

// Timing middleware
async fn timing_middleware<B: MessageBody>(
    req: ServiceRequest,
    next: Next<B>,
) -> Result<ServiceResponse<B>, Error> {
    let start = Instant::now();
    let path = req.path().to_string();

    let response = next.call(req).await?;

    log::info!("{} took {:?}", path, start.elapsed());
    Ok(response)
}

// Clean handler - only business logic
async fn get_user(path: web::Path<i32>) -> impl Responder {
    let user = db.find_user(path.into_inner()).await?;
    web::Json(user)
}

// Compose middleware stack
App::new()
    .wrap(from_fn(timing_middleware))   // Outermost: timing
    .wrap(from_fn(auth_middleware))     // Auth check
    .wrap(Logger::default())            // Built-in logging
    .route("/users/{id}", web::get().to(get_user))
```

**Service/Transform pattern (tower-style):**

```rust
use tower::{Service, Layer, ServiceBuilder};
use tower_http::{
    trace::TraceLayer,
    compression::CompressionLayer,
    timeout::TimeoutLayer,
};
use std::time::Duration;

// Build service with layers
let service = ServiceBuilder::new()
    .layer(TraceLayer::new_for_http())
    .layer(TimeoutLayer::new(Duration::from_secs(30)))
    .layer(CompressionLayer::new())
    .service(my_handler);

// Each layer wraps the inner service
// Request:  TraceLayer -> TimeoutLayer -> CompressionLayer -> Handler
// Response: Handler -> CompressionLayer -> TimeoutLayer -> TraceLayer
```

**Real-world example from Actix Web middleware:**

```rust
// actix-web/src/middleware/mod.rs

// Built-in middleware - all use Transform/Service pattern
use actix_web::middleware::{
    Compress,        // Response compression
    DefaultHeaders,  // Add headers to all responses
    Logger,          // Request logging
    NormalizePath,   // Path normalization
    ErrorHandlers,   // Custom error responses
};

// Compose in order - last wrapped = first executed on request
App::new()
    .wrap(NormalizePath::trim())         // 1st: normalize paths
    .wrap(Compress::default())           // 2nd: compress response
    .wrap(
        DefaultHeaders::new()
            .add(("X-Version", "1.0"))
    )                                    // 3rd: add headers
    .wrap(Logger::default())             // 4th: log (sees final state)
```

**Custom middleware with state:**

```rust
use std::rc::Rc;

pub struct RateLimiter {
    max_requests: u32,
    window_secs: u64,
}

impl RateLimiter {
    pub fn new(max_requests: u32, window_secs: u64) -> Self {
        Self { max_requests, window_secs }
    }

    pub fn into_middleware<S, B>(self) -> impl Transform<S, ServiceRequest>
    where
        S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
        B: MessageBody + 'static,
    {
        let this = Rc::new(self);
        from_fn(move |req, next| {
            let this = Rc::clone(&this);
            async move {
                if this.is_rate_limited(&req) {
                    return Err(Error::TooManyRequests);
                }
                next.call(req).await
            }
        })
    }
}

// Usage
App::new()
    .wrap(RateLimiter::new(100, 60).into_middleware())
```

**Guidelines:**

| Layer Type | Purpose             | Examples                  |
| ---------- | ------------------- | ------------------------- |
| Outer      | Observability       | Logging, tracing, metrics |
| Middle     | Request handling    | Auth, rate limiting, CORS |
| Inner      | Response processing | Compression, caching      |

Reference: [Tower Service Crate](https://docs.rs/tower) | [Actix Middleware](https://actix.rs/docs/middleware/)
