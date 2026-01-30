# Architecture: The Parallel Pipeline (Ripgrep Style)

**Context**: Processing large streams of data (files, logs) where order might not matter but throughput does.
**Rule**: Decompose the work into independent units. Use a "Work Stealing" approach or "Sender/Receiver" channel architecture to keep all cores busy. Avoid shared mutable state (locks) in the hot path.

## Implementation

```rust
// Parallel Walk
use rayon::prelude::*;
use walkdir::WalkDir;

pub fn search_parallel(path: &Path, pattern: &str) {
    WalkDir::new(path)
        .into_iter()
        .par_bridge() // Turn iterator into parallel iterator
        .filter_map(|e| e.ok())
        .for_each(|entry| {
            if is_match(&entry, pattern) {
                println!("Found in {:?}", entry.path());
            }
        });
}
```
