# Network 001: CRDS Gossip Protocol

## Context

Distributed systems need to share metadata (configuration, liveness, load info) across a cluster where no single node has a complete view and nodes may fail or join dynamically.

## The Pattern

Use a **Cluster Replicated Data Store (CRDS)** propagated via a **Gossip Protocol**.

### Core Components

1.  **CRDS (The State)**: A local database containing the "World View".
    - **Versioned Data**: Every value has a wallclock timestamp or version counter.
    - **Conflict Resolution**: Last-Write-Wins (LWW) or Vector Clocks.
    - **Data Types**: Node Info (`ContactInfo`), Votes, Ledger Height.

2.  **Gossip (The Transport)**: A randomized propagation mechanism.
    - **Push**: Active nodes send updates to random peers.
    - **Pull**: Nodes periodically query peers for missing data (Bloom Filters).
    - **Pruning**: Old data is discarded to keep the working set small.

### Critical Rules

- **Convergence**: The protocol must guarantee that all nodes eventually reach the same state.
- **Bandwidth Control**: Limit gossip traffic to a fixed percentage of bandwidth. Use Bloom Filters to minimize redundant transfers.
- **Security**: Validate signatures on all gossip messages (SigVerify). Do not accept unsigned data.

## Example (Jito-Solana)

```rust
pub struct CrdsGossip {
    pub crds: RwLock<Crds>, // The Versioned Store
    pub push: CrdsGossipPush, // Active propagation logic
    pub pull: CrdsGossipPull, // Passive sync logic
}

impl Crds {
    /// Insert a value. Returns false if the new value is older than existing.
    pub fn insert(&mut self, value: CrdsValue, now: u64) -> bool {
        if let Some(existing) = self.table.get(&value.label()) {
            if existing.wallclock >= value.wallclock {
                return false; // Stale update
            }
        }
        self.table.insert(value.label(), value);
        true
    }
}
```
