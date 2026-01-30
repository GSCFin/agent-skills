# Rust Pattern: Type-Safe DSL with Marker Traits

## Context

When building a Domain Specific Language (DSL) or a complex API (like an SQL Query Builder) where certain operations are valid only in specific contexts (e.g., you can't select a column that isn't in the GROUP BY clause).

## The Pattern

Use "Marker Traits" and generic bounds to enforce validity at compile time. These traits often have no methods and serve purely as compile-time "tags" or "proofs".

### Example: Diesel's ValidGrouping

Diesel ensures that you only select columns that are valid given the current `GROUP BY` clause.

```rust
// Marker trait: Types implementing this are "valid" to be used in the current group context.
pub trait ValidGrouping<GroupByClause> {
    type IsAggregate;
}

// A column is valid if it appears in the Group By clause...
impl<T> ValidGrouping<T> for T {
    type IsAggregate = is_aggregate::No;
}

// ...OR if it is an aggregate function (like count(*))
impl<T> ValidGrouping<T> for CountStar {
    type IsAggregate = is_aggregate::Yes;
}
```

## Benefits

1.  **Compile-Time Guarantees**: Invalid queries simply fail to compile, preventing runtime errors.
2.  **Zero Runtime Cost**: Since these traits (and often the structs wrapping them) are zero-sized types (ZSTs) or purely PhantomData-based, they disappear in the compiled binary.
3.  **Self-Documenting API**: The trait bounds clearly state the requirements for using an API.

## When to Use

- Building "Builders" that have strict state transition rules (State Pattern).
- Designing APIs where certain inputs are invalid based on prior configuration.
- Creating DSLs for external systems (SQL, GraphQL, etc.) to ensure correctness before sending.
