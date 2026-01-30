# Parallel Search Visitor Pattern

**Category**: Performance
**Context**: You need to traverse a large data structure (like a file system) and process items in parallel to maximize throughput.
**Source**: Extracted from **Ripgrep** (`ignore::walk`).

## The Pattern

Naive parallelism (e.g., submitting every file to a thread pool) invokes too much synchronization overhead. The "Parallel Visitor" pattern solves this by:

1.  **Work Stealing**: Use a decentralized stack of work (directories to visit).
2.  **Decoupling Builder/Visitor**: A `ParallelVisitorBuilder` creates a separate `ParallelVisitor` instance for each thread. This allows each thread to have its own mutable state (e.g., a buffer or regex engine) without locking.

### Core Structure

```mermaid
graph TD
    Main[WalkParallel] -->|Spawns| Worker1
    Main -->|Spawns| Worker2
    Main -->|Spawns| Worker3

    subgraph Thread 1
        Worker1 -->|Builder::build()| Visitor1
        Visitor1 -->|Process| FileA
    end

    subgraph Thread 2
        Worker2 -->|Builder::build()| Visitor2
        Visitor2 -->|Process| FileB
    end
```

## Implementation Guide

### 1. The Visitor Builder

Responsible for creating the thread-local state.

```rust
// Extracted from Ripgrep
pub trait ParallelVisitorBuilder<'s> {
    // Called once per thread
    fn build(&mut self) -> Box<dyn ParallelVisitor + 's>;
}
```

### 2. The Visitor

Performs the actual work on each item.

```rust
pub trait ParallelVisitor: Send {
    fn visit(&mut self, entry: Result<DirEntry, Error>) -> WalkState;
}

pub enum WalkState {
    Continue,
    Quit,
    Skip,
}
```

### 3. Execution

The runtime manages the thread pool and work distribution.

```rust
// Usage
let walker = WalkBuilder::new("./").threads(num_cpus::get()).build_parallel();
walker.run(|| {
    // This closure acts as the Builder
    let mut pattern = Regex::new("foo").unwrap(); // Created per thread!
    Box::new(move |entry| {
        // This closure acts as the Visitor
        if pattern.is_match(entry.path().to_str().unwrap()) {
             println!("Match!");
        }
        WalkState::Continue
    })
});
```

## Benefits

- **No Lock Contention**: Each thread writes to its own output buffer or uses its own regex engine.
- **Cache Locality**: Data remains local to the thread processing it.
- **Dynamic Load Balancing**: Work stealing ensures no thread sits idle if one directory is massive.
