---
id: data-003-archetypal-ecs
title: Prefer Archetypal Storage for Homogeneous Data
impact: HIGH
---

# Prefer Archetypal Storage for Homogeneous Data

## Context

Naive ECS implementations (or AoS) often suffer from cache misses when iterating over entities with varying component sets.

## Rule

Use **Archetypal Storage** (`TableStored`) for common, hot-path components to ensure cache locality.

1.  **Archetypes**: Group entities by their unique set of components.
2.  **Tables**: Store components for an archetype in contiguous column arrays.
3.  **Sparse Sets**: Use sparse storage ONLY for rare or frequently added/removed components to avoid archetype fragmentation (moves).
4.  **Bundles**: Define component groups (`Bundle`) to ensure atomic archetype transitions.

## Examples

### Correct Code (Bevy Style)

```rust
// Archetypal (Dense) - Good for Position, Velocity
#[derive(Component)]
struct Position(Vec3);

// Sparse - Good for "Selected", "Frozen" (Flags)
#[derive(Component)]
#[component(storage = "SparseSet")]
struct Selected;

fn system(query: Query<(&Position, &Velocity)>) {
    // Iterates 2 linear arrays in lockstep.
    // Zero branching per entity (except iteration bounds).
    for (pos, vel) in query.iter() {
        // ...
    }
}
```
