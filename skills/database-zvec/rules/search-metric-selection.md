---
title: Match MetricType to Embedding Model
impact: HIGH
impactDescription: "wrong metric = irrelevant search results"
tags: [search, metric, cosine, ip, l2]
---

## Match MetricType to Embedding Model

Your chosen `MetricType` must align with how your embedding model was trained.
Using the wrong metric produces semantically meaningless rankings.

| Metric              | Best For                  | Notes                               |
| ------------------- | ------------------------- | ----------------------------------- |
| `MetricType.IP`     | Pre-normalized embeddings | OpenAI, most sentence-transformers  |
| `MetricType.L2`     | Raw unnormalized vectors  | Some custom/scientific models       |
| `MetricType.COSINE` | Any embeddings            | Auto-normalizes; universal fallback |

**Incorrect:**

```python
# BUG: OpenAI embeddings are normalized — L2 distance is suboptimal
collection.create_index("emb", zvec.HnswIndexParam(
    metric_type=zvec.MetricType.L2,  # Wrong for normalized embeddings
))
```

**Correct:**

```python
# OpenAI embeddings are L2-normalized → use IP or COSINE
collection.create_index("emb", zvec.HnswIndexParam(
    metric_type=zvec.MetricType.COSINE,  # Safe universal choice
))
```

**Best: use IP for pre-normalized vectors (slightly faster):**

```python
collection.create_index("emb", zvec.HnswIndexParam(
    metric_type=zvec.MetricType.IP,  # Fastest for normalized vectors
))
```

**Trade-off:** COSINE adds a normalization step per query. For pre-normalized
embeddings, IP is ~5-10% faster with identical results.

Reference: [Zvec Metrics](https://zvec.org/en/docs/)
