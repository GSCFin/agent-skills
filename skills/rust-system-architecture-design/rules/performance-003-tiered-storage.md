# Performance 003: Tiered Storage

## Context

High-performance systems often manage datasets that exceed available RAM (e.g., Blockchain state, Database indexes). Naive approaches (everything in RAM or everything on disk) fail on cost or latency.

## The Pattern

Implement a **Tiered Storage** architecture that segregates data based on access frequency and latency requirements.

### Layers

1.  **Hot (RAM)**:
    - **Content**: Indexes, Metadata, Recently Accessed Data.
    - **Structure**: `HashMap`, `BTreeMap`, `DashMap`.
    - **Rule**: Must be lock-free or highly granularly locked (`RwLock` sharding).
    - **Example**: `AccountsIndex` in Solana (Points to offset in AppendVec).

2.  **Warm (Mmap/SSD)**:
    - **Content**: Active Data, Append-Only Logs.
    - **Structure**: Memory-mapped files (`mmap`), Append-only vectors (`AppendVec`).
    - **Rule**: Sequential writes, Random reads. zero-copy deserialization.
    - **Example**: `AppendVec` files in Solana (Stores full Account data).

3.  **Cold (Disk/Blob)**:
    - **Content**: Historical Snapshots, Archives.
    - **Structure**: Compressed archives (`zstd`), Object Storage.
    - **Rule**: High throughput, High latency.

## Best Practices

- **Separation of Keys and Data**: Keep keys in RAM (Hot), Data on Disk (Warm).
- **Append-Only Writes**: Never mutate data on disk. extensive seeking kills performance. Append new versions, update Index to point to new location.
- **Garbage Collection**: Implement a background process to compact/purge old data (discarded `AppendVecs`).

## Example (Pseudo-Solana)

```rust
struct AccountsDb {
    // Level 1: Hot Index
    index: AccountsIndex<Pubkey, Offset>,

    // Level 2: Warm Storage (AppendVecs)
    storage: Vec<Arc<AppendVec>>,
}

impl AccountsDb {
    fn load_account(&self, pubkey: &Pubkey) -> Option<Account> {
        let offset = self.index.get(pubkey)?;
        // Zero-copy read from mmap
        self.storage.get_account(offset)
    }

    fn store_account(&self, account: Account) {
        // Sequential write to end of current AppendVec
        let offset = self.storage.append(account);
        // Update Index
        self.index.insert(account.pubkey, offset);
    }
}
```
