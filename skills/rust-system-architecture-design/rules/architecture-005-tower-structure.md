# Architecture 005: 5+1 Information Tower

## Context

When designing or analyzing complex systems, it is difficult to maintain a mental model of all components. Flattening the architecture leads to spaghetti code and poor separation of concerns.

## The Pattern

Organize the system into **6 distinct levels** (5 Layers + 1 Vertical Slice). This is the "5+1 Information Tower".

### Level 0: Workspace (The Foundation)

- **Focus**: Build system, dependency graph, project layout.
- **Artifacts**: `Cargo.toml`, `rust-toolchain.toml`, `build.rs`, Directory structure.
- **Rule**: Enforce strict dependency boundaries (e.g., `core` cannot depend on `app`).

### Level 1: System (The Executor)

- **Focus**: Lifecycle, Concurrency, Actor supervision.
- **Artifacts**: `main.rs`, Service Supervisors (`BankingStage`), Thread Pools, Event Loops.
- **Rule**: Isolate "running" the code from the "logic" of the code.

### Level 2: Data (The State)

- **Focus**: Persistence, Data Structures, Serialization.
- **Artifacts**: Database Schemas (`AccountsDb`), File Formats (`AppendVecs`), Type Definitions.
- **Rule**: Optimize for access patterns (Read vs Write). Use Zero-Copy where possible.

### Level 3: Network (The Boundary)

- **Focus**: Communication, Interfaces, Protocols.
- **Artifacts**: RPC Handlers, P2P Protocols (`Gossip`), Serializers (`inc_bincode`).
- **Rule**: Treat all input as untrusted. Define strict Interface Definition Languages (IDLs).

### Level 4: Core (The Brain)

- **Focus**: Domain Logic, Invariants, State Transitions.
- **Artifacts**: State Machines (`Bank`), Consensus Algorithms (`Tower BFT`), Business Rules.
- **Rule**: Pure functions where possible. Deterministic execution. No IO allowed here.

### Level 5: Dev (The Experience) +1

- **Focus**: Developer Experience, Testing, Operability.
- **Artifacts**: Benchmarks (`bench-tps`), Fuzz targets, Metrics, Genesis Config.
- **Rule**: Make the system observable and testable by default.

## Examples

- **Jito-Solana**: Uses this exact structure (`workspace`, `banking_stage`, `accounts_db`, `tpu_client`, `bank`, `bench-tps`).
- **Tokio**: `workspace`, `runtime`, `sync` primitives, `net`, `time`, `bench`.
