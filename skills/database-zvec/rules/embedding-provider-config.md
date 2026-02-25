---
title: Configure Embedding Functions Correctly
impact: MEDIUM
impactDescription: "dimension mismatch or wrong API config causes runtime failures"
tags: [embedding, openai, qwen, sentence-transformer, bm25]
---

## Configure Embedding Functions Correctly

Zvec provides built-in embedding integrations. Each requires specific
dependencies and configuration. Schema dimensions MUST match the model output.

| Provider | Class                        | Dims      | Requires                |
| -------- | ---------------------------- | --------- | ----------------------- |
| OpenAI   | `OpenAIDenseEmbedding`       | 1536/3072 | `openai`, API key       |
| Qwen     | `QwenDenseEmbedding`         | 1024      | `dashscope`, API key    |
| Local    | `DefaultLocalDenseEmbedding` | varies    | `sentence-transformers` |
| BM25     | `BM25EmbeddingFunction`      | sparse    | built-in                |

**Incorrect (dimension mismatch):**

```python
embedding_fn = zvec.OpenAIDenseEmbedding(
    model_name="text-embedding-3-small",  # 1536 dims
    api_key="sk-...",
)

schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),  # WRONG
)
# Runtime error: vector dimension 1536 ≠ schema dimension 768
```

**Correct (verify dimension):**

```python
embedding_fn = zvec.OpenAIDenseEmbedding(
    model_name="text-embedding-3-small",
    api_key="sk-...",
)

# Verify dimension by encoding a test string
test_vec = embedding_fn.encode(["test"])[0]
dim = len(test_vec)  # 1536

schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, dim),
)
```

**Local model (no API key needed):**

```python
embedding_fn = zvec.DefaultLocalDenseEmbedding()
test_vec = embedding_fn.encode(["test"])[0]
dim = len(test_vec)  # e.g., 384 for all-MiniLM-L6-v2
```

Reference: [Zvec Embedding Docs](https://zvec.org/en/docs/)
