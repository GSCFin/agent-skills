---
id: performance-001-ecs-data-locality
title: Maximize Cache Locality with Data-Oriented Design
impact: HIGH
---

# Maximize Cache Locality with Data-Oriented Design

## Context

Object-Oriented approaches often scatter data across the heap (pointer chasing), leading to cache misses and poor performance in high-throughput components (like simulations or processing pipelines).

## Rule

Adopt a **Data-Oriented** approach (like ECS) for performance-critical hot paths.

1.  Separate Data (`Component`) from Logic (`System`).
2.  Store homogenous data in contiguous arrays (`Vec<Component>`).
3.  Process data in linear batches to maximize CPU cache prefetching.

## Examples

### Incorrect Code

Array of Structs (AoS) with pointer chasing.

```rust
struct GameObject {
    pos: Position,
    vel: Velocity,
    // ... many other fields
}

let objects: Vec<Box<GameObject>> = ...; // Heap allocations
for obj in objects {
    // Cache miss likely on every iteration
    obj.pos += obj.vel;
}
```

### Correct Code

Structure of Arrays (SoA) / ECS style.

```rust
struct PositionComponents(Vec<Position>);
struct VelocityComponents(Vec<Velocity>);

fn update(pos: &mut PositionComponents, vel: &VelocityComponents) {
    // Linear access, extremely cache efficient
    for (p, v) in pos.0.iter_mut().zip(vel.0.iter()) {
        p.x += v.x;
        p.y += v.y;
    }
}
```

## Champion Project: Bevy

Bevy's ECS archetype-based storage ensures that components accessed together are stored together, providing significant performance benefits over traditional OOP hierarchies.
