# Rust Pattern: Trait-Based Abstraction

## Context

When designing system components that need to support multiple implementations (like database backends, storage layers, or runtime environments) without sacrificing static type safety or performance.

## The Pattern

Define a core trait that captures the essential behavior of the component. Use associated types to capture implementation-specific details that usually vary between implementations (e.g., Transaction types, Backend-specific constructs).

### Example: Diesel Connection

Diesel's `Connection` trait is a prime example of this pattern. It doesn't just define methods; it defines _types_ that the implementation must provide.

```rust
pub trait Connection: SimpleConnection + Sized + Send {
    // The specific Backend this connection talks to (Pg, Sqlite, Mysql)
    type Backend: Backend;

    // The transaction manager logic, which might vary by backend capability
    type TransactionManager: TransactionManager<Self>;

    fn establish(database_url: &str) -> ConnectionResult<Self>;
    fn execute(&mut self, query: &str) -> QueryResult<usize>;
    fn transaction<T, E, F>(&mut self, f: F) -> Result<T, E>
    where
        F: FnOnce(&mut Self) -> Result<T, E>,
        E: From<Error>;
}
```

## Benefits

1.  **Static Dispatch**: Users can write generic code `fn run<C: Connection>(conn: &mut C)` that is monomorphized and optimized for the specific backend.
2.  **Type Safety**: Associated types ensure that you don't accidentally mix incompatible types (e.g., using a Postgres query builder with a SQLite connection).
3.  **Extensibility**: Third-party crates can implement defining traits to add support for new backends (e.g., `diesel-oci`).

## When to Use

- Designing the core interface of a library that supports multiple "drivers".
- When you need high performance and want to avoid `Box<dyn Trait>` (dynamic dispatch).
- When implementations have different internal types that need to be exposed to the caller (via associated types).
