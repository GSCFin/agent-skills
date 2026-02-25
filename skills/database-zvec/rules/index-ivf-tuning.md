---
title: Tune IVF Index for Billion-Scale
impact: MEDIUM
impactDescription: "proper nlist/nprobe tuning critical for billion-scale recall"
tags: [index, ivf, nlist, nprobe, scale]
---

## Tune IVF Index for Billion-Scale

IVF (Inverted File) partitions vectors into clusters. Better memory efficiency
than HNSW at massive scale, but requires careful tuning.

| Parameter | Description                 | Guideline                     |
| --------- | --------------------------- | ----------------------------- |
| `nlist`   | Number of clusters          | √N to 4√N (N = total vectors) |
| `nprobe`  | Clusters to search at query | 1-20% of nlist                |

**Incorrect (poor nlist for 100M vectors):**

```python
# nlist=100 for 100M vectors = 1M vectors per cluster — very slow
collection.create_index("emb", zvec.IVFIndexParam(
    metric_type=zvec.MetricType.IP,
    nlist=100,
))
```

**Correct (scaled nlist):**

```python
import math
n_vectors = 100_000_000
nlist = int(math.sqrt(n_vectors))  # ~10,000

collection.create_index("emb", zvec.IVFIndexParam(
    metric_type=zvec.MetricType.IP,
    nlist=nlist,  # 10,000 clusters
))

# At query time: search ~1-5% of clusters
results = collection.query(
    zvec.VectorQuery("emb", vector=q, param=zvec.IVFQueryParam(nprobe=128)),
    topk=10,
)
# nprobe=128 out of 10,000 clusters = 1.3% → good recall/speed balance
```

**When NOT to use IVF:**

- Dataset < 1M vectors (HNSW is faster and simpler)
- Need very high recall > 99% (HNSW or Flat is better)

Reference: [Zvec Index Docs](https://zvec.org/en/docs/)
