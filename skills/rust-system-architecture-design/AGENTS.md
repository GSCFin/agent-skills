# Rust System Architecture Design - Comprehensive Guide

**Context**: Execution of asynchronous tasks.
**Solution**: A `Runtime` struct that owns the I/O driver (reactor) and the Task Scheduler. It provides the entry point `block_on` to bridge synchronous main code with async worlds.

```rust
// Extracted from Tokio
pub struct Runtime {
    /// Handle to the runtime functionality
    handle: Handle,
    /// Blocking pool handle
    blocking_pool: BlockingPool,
}

impl Runtime {
    pub fn new() -> io::Result<Runtime> {
        Builder::new_multi_thread().enable_all().build()
    }

    pub fn block_on<F: Future>(&self, future: F) -> F::Output {
        // Enters the runtime context
        let _enter = self.enter();
        self.block_on_inner(future)
    }
}
```

### Level 2: Domain Model (The Business Logic)

#### Pattern: App Configuration Object (`actix_web::App`)

**Context**: Configuring the main application entry point with routes, state, and extensions.
**Solution**: An `App` builder struct that accumulates state using the "Builder Pattern" before finalizing into a runner. Use `app_data` to inject dependency injection containers.

````rust
// Extracted from Actix
pub struct App<T> {
    services: Vec<Box<dyn ServiceFactory>>,
    extensions: HashMap<TypeId, Box<dyn Any>>,
}

impl<T> App<T> {
    pub fn service<F>(mut self, factory: F) -> Self {
        self.services.push(Box::new(factory));
        self
    }

    pub fn app_data<U: 'static>(mut self, data: U) -> Self {
        self.extensions.insert(data);
        self
    }
}

#### Pattern: App Builder (`bevy_app`)
**Context**: Constructing a complex application with modular components and plugins.
**Solution**: Use a builder pattern to Compose the `App`.
- **Plugin System**: `app.add_plugins(MyPlugin)` allows modular feature addition.
- **System Scheduling**: `app.add_systems(Update, my_system)` registers logic.
- **Runner**: `app.run()` executes the main loop (e.g., winit event loop).
- **Sub-Apps**: Support for isolated sub-applications (e.g., render graph execution).

#### Pattern: Archetypal ECS (`bevy_ecs`)
**Context**: High-performance game logic with thousands of entities.
**Solution**: Use Archetypal storage for cache locality and Sparse Sets for flexibility.
- **Tables**: Dense storage for common component combinations (Archetypes).
- **Sparse Sets**: fast insertion/removal for rare components, sacrificing some iteration speed.
- **Bundles**: `world.spawn((A, B))` guarantees atomic entity creation.
- **Component Hooks**: `on_add`, `on_remove` triggers for reactive logic (e.g., initializing physics bodies).


### Level 3: Interfaces & Contracts (The Boundaries)

#### Pattern: Poll-Based I/O Traits (`tokio::io::AsyncRead`)

**Context**: Creating a unified interface for asynchronous reading/writing that works across sockets, files, and streams.
**Solution**: Define traits that mirror `std::io` but return `Poll` results instead of blocking. Pass `Context` to support waker registration.

```rust
// Extracted from Tokio
pub trait AsyncRead {
    fn poll_read(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &mut ReadBuf<'_>
    ) -> Poll<io::Result<()>>;
}
````

#### Pattern: Parallel Visitor (`ripgrep::walk::ParallelVisitor`)

**Context**: traversing a file system or data structure in parallel.
**Solution**: decoupled `ParallelVisitorBuilder` (creates a visitor per thread) from `ParallelVisitor` (does the work).

```rust
// Extracted from Ripgrep
pub trait ParallelVisitorBuilder<'s> {
    fn build(&mut self) -> Box<dyn ParallelVisitor + 's>;
}

pub trait ParallelVisitor: Send {
    fn visit(&mut self, entry: Result<DirEntry, Error>) -> WalkState;
}
```

### Level 4: Critical Paths (Performance & Stability)

#### Pattern: Work-Stealing Parallel Search (`ripgrep::walk::WalkParallel`)

**Context**: Maximizing I/O and CPU throughput when scanning thousands of files.
**Solution**: Use a pool of worker threads. A main thread (or stealer) feeds a deque of "Work". Workers process items and can push new work (subdirectories) onto the stack.

```rust
// Extracted from Ripgrep
pub struct WalkParallel {
    pub fn run<'s, F>(self, mkf: F) {
        // Spawns threads
        // Each thread runs a worker loop popping from local stack or stealing
    }
}
```

### Level 5: Development Guide (Best Practices)

#### Testing Strategy

- **Unit Tests**: Colocated in `mod tests` within the same file for private access.
- **Integration Tests**: Located in `tests/` directory, treating the crate as an external dependency.
- **Property-Based Testing**: Use `proptest` for complex logic (found in Tokio).
- **Concurrency Testing**: Use `loom` to verify atomic ordering and preemption (found in Tokio).

#### Benchmarking Strategy

- **Dedicated Bench Crate**: Use a separate `benches` crate in the workspace (e.g., `bevy/benches`) to avoid bloating core crates.
- **Criterion Integration**: Use `criterion` for statistical analysis.
- **Granular Suites**: Organize benchmarks by crate (e.g., `benches/bevy_ecs`, `benches/bevy_reflect`).
- **Black Box**: Use `std::hint::black_box` to prevent compiler optimizations from eliminating code during benchmarks.

---

## Quick Reference Rules

### 1. Concurrency

- [Async Runtime Abstraction](rules/concurrency-001-async-runtime-abstraction.md)
- [Actor Model / Service Pipeline](rules/architecture-004-service-pipeline.md)

### 2. Modularity

- [Plugin Systems](rules/architecture-001-plugin-system.md)
- [Builder Pattern](rules/api-design-001-builder-pattern.md)

### 3. Performance

- [Parallel Search / Visitor](rules/performance-002-parallel-search.md)
- [ECS Data Locality](rules/performance-001-ecs-data-locality.md)
