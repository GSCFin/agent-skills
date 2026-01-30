---
id: architecture-001-plugin-system
title: Implement a Plugin Architecture for Extensibility
impact: CRITICAL
---

# Implement a Plugin Architecture

## Context

Large systems often grow to be monolithic and difficult to maintain. Adding new features requires modifying the core application initialization logic, leading to merge conflicts and spaghetti code.

## Rule

Implement a **Plugin System** to decouple feature implementation from application assembly.

1.  Define a `Plugin` trait with a `build(&self, app: &mut App)` method.
2.  Each feature area (Audio, Rendering, Physics, User) should be its own struct implementing this trait.
3.  The main application entry point should only consist of registering these plugins.

## Examples

### Incorrect Code

All initialization logic is crammed into `main.rs`.

```rust
// BAD: Monolithic initialization
fn main() {
    let mut app = App::new();

    // Physics Init
    app.init_resource::<PhysicsConfig>();
    app.add_system(gravity_system);

    // Audio Init
    app.init_resource::<AudioSettings>();
    app.add_system(sound_system);

    // Rendering Init
    app.init_resource::<WindowSettings>();
    app.add_system(render_system);

    app.run();
}
```

### Correct Code

Initialization is modularized into Plugins.

```rust
// GOOD: Modular Plugin Architecture
pub struct PhysicsPlugin;
impl Plugin for PhysicsPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<PhysicsConfig>()
           .add_system(gravity_system);
    }
}

pub struct AudioPlugin;
impl Plugin for AudioPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<AudioSettings>()
           .add_system(sound_system);
    }
}

fn main() {
    App::new()
        .add_plugin(PhysicsPlugin)
        .add_plugin(AudioPlugin)
        .add_plugin(RenderPlugin)
        .run();
}
```

## Champion Project: Bevy

Bevy uses this pattern exclusively. The entire game engine is a collection of plugins (`RenderPlugin`, `InputPlugin`, `WindowPlugin`) that are composed together.
