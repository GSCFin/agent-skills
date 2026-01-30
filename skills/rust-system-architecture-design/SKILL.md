---
name: rust-system-architecture-design
description: Design production-grade Rust systems using the "5+1 Information Tower" methodology. Apply proven architectural patterns (Service Pipeline, Tiered Storage, Gossip, Actor) extracted from champion projects like Jito-Solana, Tokio, and Actix.
---

# Rust System Architecture Design

This skill is grounded in the **5+1 Information Tower**, a structured approach to analyzing and designing complex systems:

1.  **Level 0: Workspace** (Project Layout, Build)
2.  **Level 1: System** (Service Pipelines, Actors)
3.  **Level 2: Data** (Storage Engines, Type Systems)
4.  **Level 3: Network** (P2P, RPC, Interfaces)
5.  **Level 4: Core** (State Machines, Consensus)
6.  **Level 5: Dev** (Benchmarks, Fuzzing)

Use this skill to:

- **Scaffold** new high-performance systems with the correct layer separation.
- **Refactor** monolithic code into testable, modular Service Pipelines.
- **Optimize** data access using Tiered Storage patterns.
- **Scale** utilizing Gossip and Cluster state patterns.

## When to Use This Skill

- **High-Level Design**: Determining the root architecture (Monolith vs. Microservices, Async vs. Thread-per-Core).
- **Concurrency**: Choosing between `tokio` runtimes, `actix` actors, or `rayon` parallelism.
- **Performance**: Designing high-throughput pipelines or parallel file walkers (`ripgrep` style).
- **API Design**: Creating ergonomic library APIs using Builders and Extenders.

## Skill Categories

### 1. Concurrency & Runtime

Patterns for managing async execution and parallel processing.

- **Async Runtime**: Leveraging `tokio::Runtime` and `AsyncRead`/`AsyncWrite`.
- **Service Pipeline**: Composable middleware chains (`actix-service`).
- **Parallel Visitor**: High-performance recursive directory/data walking (`ripgrep`).

### 2. Modularity & Extensibility

Patterns for decoupling components and enabling user extensions.

- **App Builder**: The "Builder Pattern" for application configuration (`actix-web::App`).
- **Plugin Architecture**: Dynamic loading and lifecycle management (`bevy`).

### 3. Data & State Management

Patterns for efficient and type-safe data handling.

- **Type-Safe DSL**: Utilizing the type system to enforce domain constraints.
- **Workspace-Based Monorepo**: Organizing large codebases with Cargo Workspaces.

## Quick Reference

### 1. Concurrency & Runtime

- [Service Pipeline (Actix)](rules/architecture-004-service-pipeline.md)
- [Parallel Search (Ripgrep)](rules/performance-002-parallel-search.md)
- [Async Runtime Abstraction](rules/concurrency-001-async-runtime-abstraction.md)
- [Task Pool (Bevy)](rules/concurrency-002-task-pool.md)
- [5+1 Information Tower](rules/architecture-005-tower-structure.md)

### 2. Modularity & Extensibility

- [Plugin System](rules/architecture-001-plugin-system.md)
- [App Builder (Bevy)](rules/architecture-006-app-builder.md)
- [CRDS Gossip Protocol](rules/network-001-crds-gossip.md)
- [Pipelined Rendering (Bevy)](rules/architecture-007-pipelined-rendering.md)

### 3. Performance

- [Archetypal ECS (Bevy)](rules/data-003-archetypal-ecs.md)
- [ECS Data Locality](rules/performance-001-ecs-data-locality.md)
- [Tiered Storage](rules/performance-003-tiered-storage.md)

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
