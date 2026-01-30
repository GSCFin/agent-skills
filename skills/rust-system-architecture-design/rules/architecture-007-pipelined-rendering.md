---
id: architecture-007-pipelined-rendering
title: Decouple Logic and Rendering with Pipelined Architecture
impact: HIGH
---

# Decouple Logic and Rendering with Pipelined Architecture

## Context

Rendering often requires high-throughput data processing and API calls that can block the main game logic. Safe concurrent access to data is difficult.

## Rule

Use a **Pipelined Rendering** architecture (`Extract` -> `Prepare` -> `Render`).

1.  **Main App**: Runs game logic (CPU).
2.  **Render App**: Runs rendering logic (often on a separate thread/stage).
3.  **Extract**: Synchronize data from Main World to Render World at a specific sync point.
4.  **Double Buffering**: Use extracted data to prevent race conditions.

## Examples

### Correct Code (Bevy Style)

```rust
// 1. Component in Main World
#[derive(Component)]
struct MeshData { ... }

// 2. Component in Render World
#[derive(Component)]
struct GpuMesh { ... }

// 3. Extraction
fn extract_meshes(
    mut commands: Commands,
    query: Extract<Query<(Entity, &MeshData)>>
) {
    for (entity, mesh_data) in &query {
        commands.get_or_spawn(entity).insert(mesh_data.clone());
    }
}
```
