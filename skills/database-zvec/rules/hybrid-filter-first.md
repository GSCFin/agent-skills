---
title: Combine Vector Search with Scalar Filters
impact: MEDIUM
impactDescription: "unindexed filters cause full scans; indexed filters are 10-50x faster"
tags: [hybrid, filter, search, inverted-index]
---

## Combine Vector Search with Scalar Filters

Zvec supports SQL-like filters during vector queries. Always create inverted
indexes on filtered columns to avoid full scans.

**Incorrect (filter without index):**

```python
# No inverted index on "category" — Zvec scans ALL documents for filter
results = collection.query(
    zvec.VectorQuery("emb", vector=query_vec),
    topk=10,
    filter="category = 'tech'",
)
# Slow: full-scan filter on every query
```

**Correct (index + filter):**

```python
# Step 1: Create inverted index on filter columns
collection.create_index("category", zvec.InvertIndexParam())
collection.create_index("timestamp", zvec.InvertIndexParam())

# Step 2: Hybrid query is now fast
results = collection.query(
    zvec.VectorQuery("emb", vector=query_vec),
    topk=10,
    filter="category = 'tech' AND timestamp > 1706745600",
)
# 10-50x faster with indexed filters
```

**When NOT to index:**

- Columns rarely used in filters
- Columns with very low cardinality (e.g., boolean with 50/50 split)

Reference: [Zvec Hybrid Search](https://zvec.org/en/docs/)
