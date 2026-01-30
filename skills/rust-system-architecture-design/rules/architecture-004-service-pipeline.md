# Service Pipeline Architecture

**Category**: Architecture
**Context**: You need to process requests through a series of composable, asynchronous stages (middleware), such as authentication, logging, and compression, before reaching the final handler.
**Source**: Extracted from **Actix Web** (`actix-service`).

## The Pattern

The Service Pipeline pattern models every operation as a `Service`: a trait that takes a Request and asynchronously produces a Response. Services can be layered using `Transform` (Middleware) to build complex processing chains.

### Core Traits

```rust
pub trait Service<Req> {
    type Response;
    type Error;
    type Future: Future<Output = Result<Self::Response, Self::Error>>;

    // Backpressure mechanism
    fn poll_ready(&self, ctx: &mut Context<'_>) -> Poll<Result<(), Self::Error>>;

    // The execution logic
    fn call(&self, req: Req) -> Self::Future;
}

pub trait Transform<S, Req> {
    type Response;
    type Error;
    type InitError;
    type Transform: Service<Req, Response = Self::Response, Error = Self::Error>;
    type Future: Future<Output = Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future;
}
```

## Implementation Guide

### 1. Defining a Service

A service encapsulates a single unit of logic.

```rust
struct LoggerService<S> {
    service: S,
}

impl<S, Req> Service<Req> for LoggerService<S>
where
    S: Service<Req>,
    S::Future: 'static,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    fn poll_ready(&self, ctx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.service.poll_ready(ctx)
    }

    fn call(&self, req: Req) -> Self::Future {
        println!("Request started");
        let fut = self.service.call(req);
        Box::pin(async move {
            let res = fut.await;
            println!("Request finished");
            res
        })
    }
}
```

### 2. Composing the Pipeline

Use the `App` builder or a generic `ServiceBuilder` to stack middlewares.

```rust
// In Actix Web
App::new()
    .wrap(Logger::default()) // Wraps the entire outer layer
    .service(
        web::resource("/test")
            .wrap(CheckAuth) // Wraps only this resource
            .route(web::get().to(my_handler))
    )
```

## Benefits

- **Composability**: Middleware can be reused across different applications.
- **Separation of Concerns**: Auth, logging, and logic are decoupled.
- **Asynchronous**: Fully supports non-blocking I/O at every stage.
