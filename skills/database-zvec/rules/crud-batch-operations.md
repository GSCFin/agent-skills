---
title: Always Batch Insert and Upsert Operations
impact: HIGH
impactDescription: "single-doc inserts 10-100x slower than batched"
tags: [crud, batch, insert, upsert, performance]
---

## Always Batch Insert and Upsert Operations

Each `insert()` / `upsert()` call has fixed overhead for index locking and
buffer management. Batching amortizes this cost.

**Incorrect (one-by-one):**

```python
for item in dataset:
    collection.insert(zvec.Doc(
        id=item["id"],
        vectors={"emb": item["embedding"]},
    ))
# N syscalls, N lock acquisitions — extremely slow
```

**Correct (batched):**

```python
BATCH_SIZE = 1000

docs = [
    zvec.Doc(id=item["id"], vectors={"emb": item["embedding"]})
    for item in dataset
]

for i in range(0, len(docs), BATCH_SIZE):
    statuses = collection.insert(docs[i : i + BATCH_SIZE])
    # ~100x faster for large datasets
```

**When NOT to use batching:**

- Single user-initiated insert (e.g., "save this document") — batch of 1 is fine
- Real-time streaming where latency per doc matters more than throughput

Reference: [Zvec Insert API](https://zvec.org/en/docs/)
