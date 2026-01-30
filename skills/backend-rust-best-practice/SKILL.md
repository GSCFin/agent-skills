---
name: backend-rust-best-practice
description: Production-grade Rust engineering patterns for backend development. Covers Type-Driven Design, Builder Pattern, Structured Error Handling, Newtype Wrappers, Trait-Based Abstraction, and Thread-Safe Concurrency. Use when writing Rust backend code, libraries, or services requiring robust, idiomatic patterns.
license: MIT
metadata:
  author: agenticse
  version: "1.0.0"
---

# Backend Rust Best Practices

Production-grade patterns for writing idiomatic, performant, and maintainable Rust backend code.

## When to Apply

Reference these guidelines when:

- Designing Rust APIs and libraries
- Building backend services (HTTP, gRPC, message queues)
- Implementing error handling strategies
- Managing shared state in concurrent systems
- Creating extensible, testable architectures

## Rule Categories by Priority

| Priority | Category                 | Impact   | Prefix         |
| -------- | ------------------------ | -------- | -------------- |
| 1        | Type-Driven Design       | CRITICAL | `design-`      |
| 2        | Error Handling           | CRITICAL | `error-`       |
| 3        | Concurrency              | HIGH     | `concurrency-` |
| 4        | API Design               | HIGH     | `api-`         |
| 5        | Trait-Based Architecture | MEDIUM   | `trait-`       |
| 6        | Configuration            | MEDIUM   | `config-`      |

## Quick Reference

### 1. Type-Driven Design (CRITICAL)

- `design-newtype-wrapper` - Use newtype pattern for type safety and orphan rule workarounds
- `design-type-state` - Encode state transitions in the type system
- `design-zero-cost-abstraction` - Leverage generics and traits for zero-cost abstractions

### 2. Error Handling (CRITICAL)

- `error-typed-enums` - Use structured error enums with thiserror
- `error-context-propagation` - Add context when propagating errors
- `error-recovery-strategy` - Define explicit recovery strategies

### 3. Concurrency (HIGH)

- `concurrency-shared-state` - Use Arc + Mutex/RwLock for shared mutable state
- `concurrency-channel-patterns` - Prefer channels over shared state when possible
- `concurrency-async-mutex` - Use tokio::sync::Mutex for async code
- `concurrency-graceful-shutdown` - Implement coordinated shutdown patterns

### 4. API Design (HIGH)

- `api-builder-pattern` - Use builders for complex configuration
- `api-into-conversion` - Accept Into<T> for flexible APIs
- `api-method-chaining` - Return Self for fluent interfaces
- `api-custom-extractors` - Implement FromRequest for declarative APIs

### 5. Trait-Based Architecture (MEDIUM)

- `trait-behavior-injection` - Define behavior via traits for testability
- `trait-object-safety` - Design traits for dynamic dispatch when needed
- `trait-extension-traits` - Extend foreign types safely

### 6. Configuration (MEDIUM)

- `config-layered-middleware` - Use middleware/layers for cross-cutting concerns
- `config-environment-driven` - Load configuration from environment
- `config-observability-tracing` - Use structured logging with tracing

## How to Use

Read individual rule files for detailed explanations:

```
rules/design-newtype-wrapper.md
rules/error-typed-enums.md
rules/concurrency-shared-state.md
rules/api-builder-pattern.md
rules/trait-behavior-injection.md
rules/config-layered-middleware.md
rules/config-layered-middleware.md
rules/config-observability-tracing.md
rules/api-custom-extractors.md
rules/concurrency-graceful-shutdown.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
