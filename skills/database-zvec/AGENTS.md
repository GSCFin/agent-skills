# Zvec Vector Database Best Practices

**Version 1.0.0**
GSCFin

> **Note:**
> This document is optimized for AI agents and LLMs to follow when building,
> maintaining, or generating code that uses the Zvec vector database.
> Guidance here is derived from the official Zvec source code and API.

---

## Abstract

Zvec is an open-source, in-process vector database by Alibaba, built on the
Proxima engine. It embeds directly into Python/Node.js applications with zero
server overhead. This guide contains 10 rules across 8 categories, prioritized
by impact from CRITICAL to LOW. Includes detailed Incorrect vs. Correct
examples and impact metrics.

---

## Table of Contents

- [1. Initialization & Lifecycle](#1-initialization--lifecycle) — **CRITICAL**
- [2. Schema Design](#2-schema-design) — **HIGH**
- [3. CRUD Operations](#3-crud-operations) — **HIGH**
- [4. Vector Search & Retrieval](#4-vector-search--retrieval) — **HIGH**
- [5. Indexing Strategies](#5-indexing-strategies) — **MEDIUM**
- [6. Hybrid Search](#6-hybrid-search) — **MEDIUM**
- [7. Embedding Integration](#7-embedding-integration) — **MEDIUM**
- [8. Performance & Tuning](#8-performance--tuning) — **MEDIUM**

---

## 1. Initialization & Lifecycle

**Impact: CRITICAL**

### 1.1 Initialize Exactly Once

**Impact: CRITICAL (RuntimeError on double-init; silent failures if skipped)**

Zvec requires `zvec.init()` before any collection operation. It can only be
called once per process. Calling it again raises `RuntimeError`.

**Incorrect (no init):**

```python
import zvec

# BUG: No init() call — undefined behavior
schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)
collection = zvec.create_and_open("./data", schema)  # May crash silently
```

**Correct (init once at startup):**

```python
import zvec

# Initialize once at application startup
zvec.init()  # Uses defaults: console logging, auto-detect threads/memory

schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)
collection = zvec.create_and_open("./data", schema)
```

### 1.2 Lifecycle Functions

| Function                             | Purpose                  | Notes                                              |
| ------------------------------------ | ------------------------ | -------------------------------------------------- |
| `zvec.init()`                        | Global initialization    | Once per process, configure logging/threads/memory |
| `zvec.create_and_open(path, schema)` | Create new collection    | Errors if collection already exists at path        |
| `zvec.open(path)`                    | Open existing collection | Collection must exist                              |
| `collection.flush()`                 | Force writes to disk     | Ensures durability                                 |
| `collection.destroy()`               | Delete permanently       | **Irreversible** — all data lost                   |

**Container-friendly init:**

```python
zvec.init(
    log_type=zvec.LogType.FILE,
    log_dir="/var/log/zvec",
    memory_limit_mb=2048,    # Explicit limit for containers
    query_threads=4,         # Match cgroup CPU allocation
    optimize_threads=2,
)
```

---

## 2. Schema Design

**Impact: HIGH**

### 2.1 Choose Correct Vector Types and Dimensions

**Impact: HIGH (wrong type = garbage results; wrong dim = runtime error)**

Vector dimensions must exactly match your embedding model's output. DataType
determines precision and memory usage.

| DataType      | Bytes/Dim | When to Use                                   |
| ------------- | --------- | --------------------------------------------- |
| `VECTOR_FP32` | 4         | Default — highest precision                   |
| `VECTOR_FP16` | 2         | Memory-constrained, minimal quality loss      |
| `VECTOR_BF16` | 2         | ML-native (good for models trained with BF16) |
| `VECTOR_INT8` | 1         | Maximum compression, moderate quality loss    |

**Incorrect (wrong dimension):**

```python
# BUG: OpenAI text-embedding-3-small outputs 1536 dims, not 768
schema = zvec.CollectionSchema(
    name="openai_docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)
# Runtime error on insert when vector is 1536-dimensional
```

**Correct (match model output):**

```python
schema = zvec.CollectionSchema(
    name="openai_docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 1536),
    # 1536 matches text-embedding-3-small output
)
```

### 2.2 Add Scalar Fields for Metadata

Use `FieldSchema` to store filterable metadata alongside vectors:

```python
schema = zvec.CollectionSchema(
    name="articles",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
    fields=[
        zvec.FieldSchema("title", zvec.DataType.STRING),
        zvec.FieldSchema("category", zvec.DataType.STRING),
        zvec.FieldSchema("timestamp", zvec.DataType.INT64),
        zvec.FieldSchema("score", zvec.DataType.FLOAT),
    ],
)
```

### 2.3 Multi-Vector Collections

A single collection can contain multiple vector fields for different embedding
types (dense + sparse, multilingual, etc.):

```python
schema = zvec.CollectionSchema(
    name="hybrid_docs",
    vectors=[
        zvec.VectorSchema("dense_emb", zvec.DataType.VECTOR_FP32, 768),
        zvec.VectorSchema("sparse_emb", zvec.DataType.VECTOR_FP32, 30000),
    ],
    fields=[
        zvec.FieldSchema("title", zvec.DataType.STRING),
    ],
)
```

---

## 3. CRUD Operations

**Impact: HIGH**

### 3.1 Batch Operations for Throughput

**Impact: HIGH (single-doc inserts = 10-100x slower than batched)**

Always batch `insert()`, `upsert()`, and `update()` calls. Each call has
fixed overhead for index locking and buffer management.

**Incorrect (one-by-one insert):**

```python
for item in dataset:
    collection.insert(zvec.Doc(
        id=item["id"],
        vectors={"emb": item["embedding"]},
        fields={"title": item["title"]},
    ))
# N individual insert calls — very slow for large datasets
```

**Correct (batched insert):**

```python
BATCH_SIZE = 1000
docs = [
    zvec.Doc(
        id=item["id"],
        vectors={"emb": item["embedding"]},
        fields={"title": item["title"]},
    )
    for item in dataset
]

for i in range(0, len(docs), BATCH_SIZE):
    batch = docs[i : i + BATCH_SIZE]
    statuses = collection.insert(batch)
    # Check statuses for errors
    for status in statuses:
        if status.code != zvec.StatusCode.OK:
            print(f"Insert failed: {status}")
# ~100x faster than one-by-one
```

### 3.2 CRUD Method Reference

| Method                   | Purpose                              | Returns                    |
| ------------------------ | ------------------------------------ | -------------------------- |
| `insert(docs)`           | Insert new docs (error if ID exists) | `Status` or `list[Status]` |
| `upsert(docs)`           | Insert or update by ID               | `Status` or `list[Status]` |
| `update(docs)`           | Update existing docs only            | `Status` or `list[Status]` |
| `delete(ids)`            | Delete by ID                         | `Status` or `list[Status]` |
| `delete_by_filter(expr)` | Delete by SQL filter                 | `None`                     |
| `fetch(ids)`             | Retrieve docs by ID                  | `dict[str, Doc]`           |

### 3.3 Upsert vs Insert

```python
# Use upsert when you don't know if the doc already exists
collection.upsert(zvec.Doc(
    id="doc_123",
    vectors={"emb": [0.1, 0.2, 0.3, ...]},
    fields={"title": "Updated Title"},
))

# Use insert when you want to catch duplicates
status = collection.insert(zvec.Doc(id="doc_123", vectors={"emb": vec}))
if status.code != zvec.StatusCode.OK:
    print("Duplicate ID detected")
```

---

## 4. Vector Search & Retrieval

**Impact: HIGH**

### 4.1 Choose the Right Metric Type

**Impact: HIGH (wrong metric = irrelevant results)**

Your metric MUST match your embedding model's training objective:

| Metric                          | When to Use                       | Models                             |
| ------------------------------- | --------------------------------- | ---------------------------------- |
| `MetricType.IP` (Inner Product) | Normalized embeddings             | OpenAI, most sentence-transformers |
| `MetricType.L2` (Euclidean)     | Raw unnormalized embeddings       | Some custom models                 |
| `MetricType.COSINE`             | Auto-normalizes before comparison | Universal fallback                 |

> **Tip:** If unsure, use `COSINE` — it handles both normalized and
> unnormalized vectors correctly, with a small performance overhead.

### 4.2 Query by Vector

```python
results = collection.query(
    zvec.VectorQuery(
        field_name="emb",
        vector=[0.1, 0.2, 0.3, ...],  # Must match schema dimension
    ),
    topk=10,
)

for doc in results:
    print(f"ID: {doc.id}, Score: {doc.score}")
    print(f"Title: {doc.field('title')}")
```

### 4.3 Query by Document ID

Find similar documents to an existing one without providing a raw vector:

```python
results = collection.query(
    zvec.VectorQuery(field_name="emb", id="doc_123"),
    topk=10,
)
# Returns the 10 most similar documents to doc_123
```

### 4.4 Query with Index-Specific Parameters

```python
# HNSW: increase ef for higher recall at the cost of latency
results = collection.query(
    zvec.VectorQuery(
        field_name="emb",
        vector=query_vec,
        param=zvec.HnswQueryParam(ef=300),  # Default is usually ~100
    ),
    topk=10,
)

# IVF: increase nprobe for better recall
results = collection.query(
    zvec.VectorQuery(
        field_name="emb",
        vector=query_vec,
        param=zvec.IVFQueryParam(nprobe=64),  # Default is ~10
    ),
    topk=10,
)
```

---

## 5. Indexing Strategies

**Impact: MEDIUM**

### 5.1 HNSW Index (Recommended Default)

Best for datasets < 100M vectors. Provides excellent latency and recall.

| Parameter         | Default | Description              | Guideline                                    |
| ----------------- | ------- | ------------------------ | -------------------------------------------- |
| `M`               | 16      | Max connections per node | 16-64; higher = better recall, more memory   |
| `ef_construction` | 200     | Build-time beam width    | 100-500; higher = better graph, slower build |
| `ef` (query)      | 100     | Search-time beam width   | 100-500; tune at query time                  |

```python
collection.create_index(
    "emb",
    zvec.HnswIndexParam(
        metric_type=zvec.MetricType.COSINE,
        m=32,                # Good balance for 1M vectors
        ef_construction=400, # High quality graph
    ),
)
```

### 5.2 IVF Index (For Billion-Scale)

Partitions vectors into clusters. Better memory efficiency at massive scale.

| Parameter | Default | Description                | Guideline                         |
| --------- | ------- | -------------------------- | --------------------------------- |
| `nlist`   | —       | Number of clusters         | √N to 4√N where N = total vectors |
| `nprobe`  | 10      | Clusters searched at query | 1-20% of nlist                    |

```python
# For 10M vectors: nlist ~3162 (√10M)
collection.create_index(
    "emb",
    zvec.IVFIndexParam(
        metric_type=zvec.MetricType.IP,
        nlist=4096,
    ),
)
```

### 5.3 Inverted Index for Scalar Fields

Accelerate filter queries on scalar columns:

```python
collection.create_index("category", zvec.InvertIndexParam())
collection.create_index("timestamp", zvec.InvertIndexParam())
# Now filters on category/timestamp are index-accelerated
```

### 5.4 Flat Index (Baseline)

Brute-force exact search. Use only for testing or very small datasets (< 10K):

```python
collection.create_index("emb", zvec.FlatIndexParam(
    metric_type=zvec.MetricType.COSINE,
))
```

---

## 6. Hybrid Search

**Impact: MEDIUM**

### 6.1 Combine Vector + Scalar Filters

Zvec supports SQL-like filter expressions during vector queries:

```python
# Search for similar articles in the "tech" category from last 30 days
results = collection.query(
    zvec.VectorQuery(field_name="emb", vector=query_vec),
    topk=10,
    filter="category = 'tech' AND timestamp > 1706745600",
)
```

### 6.2 Delete by Filter

```python
# Delete all documents matching a filter condition
collection.delete_by_filter("category = 'deprecated'")
```

### 6.3 Filter Performance

> **Important:** Create inverted indexes on scalar fields used in filters.
> Without an index, Zvec must scan all documents for filter evaluation.

```python
# Step 1: Create inverted indexes on filter columns
collection.create_index("category", zvec.InvertIndexParam())
collection.create_index("timestamp", zvec.InvertIndexParam())

# Step 2: Now hybrid queries are fast
results = collection.query(
    zvec.VectorQuery(field_name="emb", vector=query_vec),
    topk=10,
    filter="category = 'tech'",
)
```

---

## 7. Embedding Integration

**Impact: MEDIUM**

### 7.1 Built-in Embedding Functions

Zvec provides ready-to-use embedding functions:

| Class                         | Provider             | Type   | Requirements                     |
| ----------------------------- | -------------------- | ------ | -------------------------------- |
| `OpenAIDenseEmbedding`        | OpenAI               | Dense  | `openai` pip package, API key    |
| `QwenDenseEmbedding`          | Alibaba DashScope    | Dense  | `dashscope` pip package, API key |
| `QwenSparseEmbedding`         | Alibaba DashScope    | Sparse | `dashscope` pip package, API key |
| `DefaultLocalDenseEmbedding`  | SentenceTransformers | Dense  | `sentence-transformers`          |
| `DefaultLocalSparseEmbedding` | SentenceTransformers | Sparse | `sentence-transformers`          |
| `BM25EmbeddingFunction`       | Local BM25           | Sparse | None (built-in)                  |

### 7.2 OpenAI Embedding Example

```python
import zvec

embedding_fn = zvec.OpenAIDenseEmbedding(
    model_name="text-embedding-3-small",  # 1536 dims
    api_key="sk-...",
)

# Generate embeddings
vectors = embedding_fn.encode(["Hello world", "How are you?"])
# vectors[0] is a 1536-dim list

# Schema must match the model's output dimension
schema = zvec.CollectionSchema(
    name="openai_docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 1536),
)
```

### 7.3 Local SentenceTransformer Example

```python
embedding_fn = zvec.DefaultLocalDenseEmbedding()
# Uses default model, typically 384 or 768 dims

vectors = embedding_fn.encode(["sample text"])
dim = len(vectors[0])  # Check actual dimension

schema = zvec.CollectionSchema(
    name="local_docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, dim),
)
```

### 7.4 Rerankers

Rerankers re-score initial results for higher precision:

```python
# RRF (Reciprocal Rank Fusion) — merge multiple result lists
reranker = zvec.RrfReRanker()

# Weighted — assign weights to different vector fields
reranker = zvec.WeightedReRanker(weights={"dense_emb": 0.7, "sparse_emb": 0.3})

# Qwen — neural reranker via DashScope API
reranker = zvec.QwenReRanker(api_key="sk-...")
```

---

## 8. Performance & Tuning

**Impact: MEDIUM**

### 8.1 Collection Optimization

After bulk inserts, call `optimize()` to merge segments and rebuild indexes:

```python
# After bulk loading, optimize for best query performance
collection.optimize(zvec.OptimizeOption())

# Always flush before closing to ensure durability
collection.flush()
```

**When to optimize:**

- After bulk insert of > 10,000 documents
- When query latency degrades over time
- Before switching from write-heavy to read-heavy workload

### 8.2 Thread Configuration

```python
zvec.init(
    query_threads=8,      # Match available CPU cores for queries
    optimize_threads=2,   # Background optimization (lower priority)
)
```

**Guidelines:**

- `query_threads`: Set to number of CPU cores dedicated to the application
- `optimize_threads`: 1-2 threads; runs in background
- In containers: if `None`, Zvec auto-detects from cgroup CPU limits

### 8.3 Memory Management

```python
zvec.init(
    memory_limit_mb=4096,  # 4GB soft limit
)
```

- If `None`, Zvec uses 80% of cgroup memory limit (container-friendly)
- Set explicitly when sharing a machine with other services

### 8.4 Quantization for Memory Reduction

Use lower-precision vector types to reduce memory footprint:

| Strategy    | Memory Reduction | Quality Impact              |
| ----------- | ---------------- | --------------------------- |
| FP32 → FP16 | 50%              | Negligible                  |
| FP32 → INT8 | 75%              | Moderate (1-3% recall loss) |

```python
# Define schema with FP16 vectors for 50% memory savings
schema = zvec.CollectionSchema(
    name="compact_docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP16, 768),
    # ~1.5KB per vector instead of ~3KB
)
```

### 8.5 Query Heuristic Tuning

Advanced scan ratio configuration:

```python
zvec.init(
    invert_to_forward_scan_ratio=0.95,   # Higher = more aggressive index skip
    brute_force_by_keys_ratio=0.05,      # Lower = prefer index over brute-force
)
```

---

## 9. Schema Evolution

### 9.1 Add a Column

```python
collection.add_column(
    zvec.FieldSchema("new_tag", zvec.DataType.STRING),
    expression="",  # Default value expression
)
```

### 9.2 Rename a Column

```python
collection.alter_column(old_name="tag", new_name="category")
```

### 9.3 Drop a Column

```python
collection.drop_column("deprecated_field")
```

### 9.4 Drop an Index

```python
collection.drop_index("emb")  # Remove the vector index
```

---

## 10. Complete RAG Pipeline Example

```python
import zvec

# 1. Initialize
zvec.init()

# 2. Set up embedding function
embedding_fn = zvec.OpenAIDenseEmbedding(
    model_name="text-embedding-3-small",
    api_key="sk-...",
)

# 3. Create collection
schema = zvec.CollectionSchema(
    name="knowledge_base",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 1536),
    fields=[
        zvec.FieldSchema("content", zvec.DataType.STRING),
        zvec.FieldSchema("source", zvec.DataType.STRING),
        zvec.FieldSchema("chunk_id", zvec.DataType.INT64),
    ],
)
collection = zvec.create_and_open("./kb_data", schema)

# 4. Create HNSW index
collection.create_index("emb", zvec.HnswIndexParam(
    metric_type=zvec.MetricType.COSINE,
    m=32,
    ef_construction=400,
))

# 5. Index documents
chunks = [{"id": f"c_{i}", "content": text, "source": "doc.pdf"} for i, text in enumerate(texts)]
vectors = embedding_fn.encode([c["content"] for c in chunks])

docs = [
    zvec.Doc(
        id=c["id"],
        vectors={"emb": vec},
        fields={"content": c["content"], "source": c["source"], "chunk_id": i},
    )
    for i, (c, vec) in enumerate(zip(chunks, vectors))
]
collection.insert(docs)
collection.optimize()

# 6. Query
query_vec = embedding_fn.encode(["What is the refund policy?"])[0]
results = collection.query(
    zvec.VectorQuery(
        field_name="emb",
        vector=query_vec,
        param=zvec.HnswQueryParam(ef=300),
    ),
    topk=5,
)

# 7. Use results as context for LLM
context = "\n".join([doc.field("content") for doc in results])
print(f"Retrieved {len(results)} chunks for RAG context")
```

---

Reference: [Zvec Documentation](https://zvec.org/en/docs/) | [GitHub](https://github.com/alibaba/zvec)
