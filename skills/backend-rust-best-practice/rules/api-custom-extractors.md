---
title: Custom Extractors for Clean Handlers
impact: HIGH
impactDescription: cleaner handlers, declarative data access, reusable logic
tags: api, extractor, from_request, actix-web, injection
---

## Custom Extractors for Clean Handlers

Implement the `FromRequest` trait to extract and validate request data (headers, auth tokens, state) declaratively, keeping handlers focused on business logic.

**Why this pattern exists:**

1.  **Separation of Concerns**: Validation logic lives in the extractor, not the handler
2.  **Declarative API**: Handlers declare _what_ they need, not _how_ to get it
3.  **Reusability**: Use the same extractor across many handlers
4.  **Testability**: Extractors can be tested independently

**Incorrect (manual extraction in handler):**

```rust
async fn create_order(
    req: HttpRequest,
    body: web::Json<OrderPayload>,
    db: web::Data<DbPool>,
) -> impl Responder {
    // ❌ Validation logic mixed with business logic
    let auth_header = match req.headers().get("Authorization") {
        Some(h) => h,
        None => return HttpResponse::Unauthorized().finish(),
    };

    let token_str = match auth_header.to_str() {
        Ok(s) => s,
        Err(_) => return HttpResponse::BadRequest().finish(),
    };

    let user_id = match verify_token(token_str) {
        Ok(id) => id,
        Err(_) => return HttpResponse::Unauthorized().finish(),
    };

    // Actual business logic starts here...
    db.create_order(user_id, body.into_inner()).await
}
```

**Correct (custom extractor):**

```rust
use actix_web::{FromRequest, HttpMessage, dev::Payload};
use std::future::{ready, Ready};

// 1. Define the type
struct AuthenticatedUser {
    id: UserId,
}

// 2. Implement FromRequest
impl FromRequest for AuthenticatedUser {
    type Error = Error;
    type Future = Ready<Result<Self, Self::Error>>;

    fn from_request(req: &HttpRequest, _payload: &mut Payload) -> Self::Future {
        let token = match req.headers().get("Authorization") {
            Some(h) => h.to_str().unwrap_or(""),
            None => return ready(Err(ErrorUnauthorized("No auth header"))),
        };

        match verify_token(token) {
            Ok(id) => ready(Ok(AuthenticatedUser { id })),
            Err(_) => ready(Err(ErrorUnauthorized("Invalid token"))),
        }
    }
}

// 3. Clean Handler
async fn create_order(
    user: AuthenticatedUser,       // ✅ Declarative: "I need an auth user"
    body: web::Json<OrderPayload>,
    db: web::Data<DbPool>,
) -> impl Responder {
    // Logic starts immediately
    db.create_order(user.id, body.into_inner()).await
}
```

**Advanced: Async Extractor (e.g., Database Lookup):**

For async extraction, use `std::future::Future` (or `BoxFuture` alias).

```rust
use std::pin::Pin;
use std::future::Future;

impl FromRequest for UserProfile {
    type Error = Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self, Self::Error>>>>;

    fn from_request(req: &HttpRequest, _: &mut Payload) -> Self::Future {
        let user_id = req.headers().get("X-User-ID").cloned(); // Simplified
        let db = req.app_data::<web::Data<DbPool>>().cloned();

        Box::pin(async move {
            let db = db.ok_or(ErrorInternalServerError("No DB"))?;
            let id = user_id.ok_or(ErrorBadRequest("Missing ID"))?;

            // Async DB call inside extractor
            let profile = db.get_profile(id).await.map_err(ErrorInternalServerError)?;
            Ok(profile)
        })
    }
}
```

**When to use:**

| Scenario       | Pattern                                 |
| -------------- | --------------------------------------- |
| Auth tokens    | `FromRequest` (Sync or Async)           |
| Request ID     | `FromRequest` (Header access)           |
| Validated JSON | Custom struct wrapping `web::Json`      |
| Feature Flags  | Middleware sets ext, Extractor reads it |

**Real-world example from Actix Web:**

```rust
// Built-in extractors are just FromRequest implementations:
// - web::Json<T>
// - web::Path<T>
// - web::Query<T>
// - web::Header<T>

// You can combine them in one handler:
async fn index(
    path: web::Path<(u32, String)>,
    json: web::Json<MyObj>,
    user: AuthenticatedUser,
) -> impl Responder { ... }
```
