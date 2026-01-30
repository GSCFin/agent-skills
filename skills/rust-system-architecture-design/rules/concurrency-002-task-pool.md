---
id: concurrency-002-task-pool
title: Use Global Task Pools for CPU-Bound Concurrency
impact: MEDIUM
---

# Use Global Task Pools for CPU-Bound Concurrency

## Context

Creating threads is expensive (< 1ms but non-zero) and oversubscription causes context switching overhead.

## Rule

Use a **Global Task Pool** for parallelizing CPU-intensive work.

1.  **Compute Pool**: For short, CPU-bound tasks (e.g., entity updates, culling).
2.  **Async Pool**: For IO-bound or long-running tasks (e.g., asset loading).
3.  **Parallel Slicing**: Use divide-and-conquer helpers (`par_chunk_map`) for data parallelism.

## Examples

### Correct Code (Bevy Style)

```rust
fn massive_update_system(pool: Res<ComputeTaskPool>, mut data: Query<&mut Data>) {
    // Automatically splits work across available cores
    data.par_iter_mut().for_each(|mut item| {
        item.complex_calculation();
    });
}

fn parallel_sort(slice: &mut [i32], pool: &TaskPool) {
    slice.par_chunk_map(pool, 1000, |chunk| {
        chunk.sort();
    });
}
```
