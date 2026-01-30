---
id: architecture-006-app-builder
title: Use App Builder for Modular Application Construction
impact: HIGH
---

# Use App Builder for Modular Application Construction

## Context

Complex applications (like games or engines) require assembling disparate systems (rendering, physics, input) into a cohesive runtime without tight coupling.

## Rule

Use a **Builder Pattern** (`App::new()`) combined with a **Plugin System** to compose the application.

1.  **Plugins**: Encapsulate feature sets (Systems, Resources, Events) into `Plugin` structs.
2.  **Builder**: Use fluent interfaces (`.add_plugins()`, `.add_systems()`) to configure the app.
3.  **Runner**: Decouple configuration from execution (`app.run()`).

## Examples

### Correct Code (Bevy Style)

```rust
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(PhysicsPlugin)
        .add_systems(Update, (player_movement, collision_detection))
        .run();
}

struct PhysicsPlugin;
impl Plugin for PhysicsPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(PhysicsConfig::default())
           .add_systems(FixedUpdate, step_physics);
    }
}
```
