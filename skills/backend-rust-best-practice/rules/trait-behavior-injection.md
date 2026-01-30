---
title: Trait-Based Behavior Injection
impact: MEDIUM
impactDescription: testability, decoupling, extensibility
tags: trait, dependency-injection, testing, abstraction
---

## Trait-Based Behavior Injection

Define behavior via traits to enable dependency injection, mocking in tests, and decoupling implementations from interfaces.

**Why this pattern exists:**

1. **Testability**: Swap real services with mocks
2. **Decoupling**: Depend on behavior, not concrete types
3. **Extensibility**: Add new implementations without modifying consumers
4. **Compile-Time Dispatch**: Generic parameters for zero-cost abstraction

**Incorrect (hard-coded dependencies):**

```rust
struct UserService {
    // Hard-coded to specific database
    db: PostgresConnection,
}

impl UserService {
    pub async fn get_user(&self, id: UserId) -> Result<User, Error> {
        self.db.query_one("SELECT * FROM users WHERE id = $1", &[&id]).await
    }
}

// Test requires real database connection!
#[test]
fn test_get_user() {
    let service = UserService { db: connect_to_postgres() };  // 😢
    // ...
}
```

**Correct (trait-based abstraction):**

```rust
// Define behavior as trait
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error>;
    async fn save(&self, user: &User) -> Result<(), Error>;
}

// Service depends on trait, not implementation
pub struct UserService<R: UserRepository> {
    repo: R,
}

impl<R: UserRepository> UserService<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn get_user(&self, id: UserId) -> Result<User, Error> {
        self.repo.find_by_id(id).await?
            .ok_or(Error::NotFound(id))
    }
}

// Production implementation
pub struct PostgresUserRepository {
    pool: PgPool,
}

#[async_trait]
impl UserRepository for PostgresUserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id)
            .fetch_optional(&self.pool)
            .await
            .map_err(Into::into)
    }

    async fn save(&self, user: &User) -> Result<(), Error> {
        // ...
    }
}

// Test with mock
#[cfg(test)]
mod tests {
    use super::*;

    struct MockUserRepository {
        users: HashMap<UserId, User>,
    }

    #[async_trait]
    impl UserRepository for MockUserRepository {
        async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error> {
            Ok(self.users.get(&id).cloned())
        }

        async fn save(&self, _user: &User) -> Result<(), Error> {
            Ok(())
        }
    }

    #[tokio::test]
    async fn test_get_user() {
        let mut users = HashMap::new();
        users.insert(UserId(1), User { name: "Alice".into() });

        let repo = MockUserRepository { users };
        let service = UserService::new(repo);

        let user = service.get_user(UserId(1)).await.unwrap();
        assert_eq!(user.name, "Alice");
    }
}
```

**Real-world example from Actix Web (FromRequest trait):**

```rust
// actix-web defines behavior via traits
pub trait FromRequest: Sized {
    type Error: Into<Error>;
    type Future: Future<Output = Result<Self, Self::Error>>;

    fn from_request(req: &HttpRequest, payload: &mut Payload) -> Self::Future;
}

// Anyone can implement to create custom extractors
impl FromRequest for UserId {
    type Error = Error;
    type Future = Ready<Result<Self, Self::Error>>;

    fn from_request(req: &HttpRequest, _: &mut Payload) -> Self::Future {
        // Extract user ID from auth header, session, etc.
        let user_id = extract_user_id_from_request(req);
        ready(user_id.ok_or_else(|| Error::Unauthorized))
    }
}

// Handler automatically receives extracted UserId
async fn handler(user_id: UserId) -> impl Responder {
    format!("Hello, user {}", user_id.0)
}
```

**Trait objects for dynamic dispatch:**

```rust
// When you need runtime polymorphism
pub struct ServiceContainer {
    user_repo: Box<dyn UserRepository>,
    payment_service: Box<dyn PaymentService>,
}

impl ServiceContainer {
    pub fn new(
        user_repo: impl UserRepository + 'static,
        payment_service: impl PaymentService + 'static,
    ) -> Self {
        Self {
            user_repo: Box::new(user_repo),
            payment_service: Box::new(payment_service),
        }
    }
}
```

**Guidelines:**

| Approach             | Use When                                    |
| -------------------- | ------------------------------------------- |
| Generic `<T: Trait>` | Performance-critical, known at compile time |
| `Box<dyn Trait>`     | Runtime selection, plugin systems           |
| `Arc<dyn Trait>`     | Shared across threads + dynamic             |

Reference: [Rust Book - Traits](https://doc.rust-lang.org/book/ch10-02-traits.html)
