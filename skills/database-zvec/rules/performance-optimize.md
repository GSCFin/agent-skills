---
title: When and How to Optimize Collections
impact: MEDIUM
impactDescription: "skipping optimize after bulk load degrades query latency 2-5x"
tags: [performance, optimize, compaction, flush]
---

## When and How to Optimize Collections

`collection.optimize()` merges segments and rebuilds indexes for optimal query
performance. Skipping it after bulk operations leaves fragmented data.

**When to call `optimize()`:**

- After bulk insert of > 10,000 documents
- When query latency degrades over time
- Before switching from write-heavy to read-heavy workload
- Before creating a production snapshot/backup

**When NOT to call `optimize()`:**

- During active write-heavy streaming (adds overhead)
- After single-doc inserts (unnecessary)

**Incorrect (no optimize after bulk load):**

```python
for batch in batches:
    collection.insert(batch)
# Query performance is degraded — fragmented segments
results = collection.query(q, topk=10)  # 2-5x slower than necessary
```

**Correct (optimize after bulk load):**

```python
for batch in batches:
    collection.insert(batch)

collection.optimize(zvec.OptimizeOption())  # Merge segments, rebuild index
collection.flush()  # Ensure durability

results = collection.query(q, topk=10)  # Optimal performance
```

Reference: [Zvec Optimization](https://zvec.org/en/docs/)
