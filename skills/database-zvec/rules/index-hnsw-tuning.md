---
title: Tune HNSW Index Parameters
impact: MEDIUM
impactDescription: "proper tuning improves recall 5-15% or reduces latency 2-5x"
tags: [index, hnsw, tuning, recall, latency]
---

## Tune HNSW Index Parameters

HNSW is the recommended index for most use cases. Key parameters control the
recall vs. speed tradeoff.

| Parameter         | Range   | Effect                                                                              |
| ----------------- | ------- | ----------------------------------------------------------------------------------- |
| `M`               | 8-64    | Connections per node. Higher = better recall, more memory (~8 bytes × M per vector) |
| `ef_construction` | 100-500 | Build-time search width. Higher = better graph quality, slower indexing             |
| `ef` (query-time) | 50-500  | Search-time beam width. Higher = better recall, higher latency                      |

**Guidelines by dataset size:**

| Vectors | M   | ef_construction | ef (query) |
| ------- | --- | --------------- | ---------- |
| < 100K  | 16  | 200             | 100        |
| 100K-1M | 32  | 400             | 200        |
| 1M-10M  | 48  | 400             | 300        |
| > 10M   | 64  | 500             | 300-500    |

**Incorrect (defaults for large dataset):**

```python
# Suboptimal for 5M vectors — defaults too conservative
collection.create_index("emb", zvec.HnswIndexParam(
    metric_type=zvec.MetricType.COSINE,
    # m=16, ef_construction=200 (defaults) — recall ~92%
))
```

**Correct (tuned for 5M vectors):**

```python
collection.create_index("emb", zvec.HnswIndexParam(
    metric_type=zvec.MetricType.COSINE,
    m=48,
    ef_construction=400,
    # Recall ~98% with moderate memory increase
))

# At query time, increase ef for critical queries
results = collection.query(
    zvec.VectorQuery("emb", vector=q, param=zvec.HnswQueryParam(ef=300)),
    topk=10,
)
```

**When NOT to use HNSW:**

- Dataset > 100M vectors (consider IVF for memory efficiency)
- Need exact results (use Flat index)

Reference: [Zvec Index Docs](https://zvec.org/en/docs/)
