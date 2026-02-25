---
title: Choose Correct Vector Types and Dimensions
impact: HIGH
impactDescription: "wrong type = garbage results; wrong dim = runtime error"
tags: [schema, vector, datatype, dimensions]
---

## Choose Correct Vector Types and Dimensions

Vector dimensions must exactly match your embedding model's output. Using the
wrong `DataType` wastes memory or degrades quality.

| DataType      | Bytes/Dim | Use Case                                    |
| ------------- | --------- | ------------------------------------------- |
| `VECTOR_FP32` | 4         | Default — highest precision                 |
| `VECTOR_FP16` | 2         | Memory-constrained, negligible quality loss |
| `VECTOR_BF16` | 2         | BF16-trained models                         |
| `VECTOR_INT8` | 1         | Max compression, ~1-3% recall loss          |

**Common embedding dimensions:**

| Model                           | Dimensions |
| ------------------------------- | ---------- |
| OpenAI `text-embedding-3-small` | 1536       |
| OpenAI `text-embedding-3-large` | 3072       |
| `all-MiniLM-L6-v2`              | 384        |
| `all-mpnet-base-v2`             | 768        |
| Qwen embedding                  | 1024       |

**Incorrect:**

```python
# BUG: OpenAI text-embedding-3-small outputs 1536 dims
schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)
# Will fail at insert time with dimension mismatch
```

**Correct:**

```python
schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 1536),
    # 1536 matches text-embedding-3-small
)
```

Reference: [Zvec Schema Docs](https://zvec.org/en/docs/)
