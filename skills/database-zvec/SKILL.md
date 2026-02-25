---
name: database-zvec
description: "Expert in Zvec, Alibaba's open-source in-process vector database
  built on Proxima. Covers schema design, dense/sparse vector operations,
  hybrid search with filters, HNSW/IVF/Flat indexing, embedding integrations
  (OpenAI, Qwen, SentenceTransformer, BM25), reranking, and performance tuning.
  Use PROACTIVELY for vector similarity search, RAG pipelines, or embedding
  storage tasks."
metadata:
  model: sonnet
  license: Apache-2.0
  version: "1.0.0"
risk: low
source: community
---

## Use this skill when

- Building vector similarity search into an application (RAG, recommendation, semantic search)
- Working with dense or sparse embeddings and need an embedded database (no server)
- Designing schemas for vector collections with scalar metadata fields
- Choosing and tuning vector indexes (HNSW, IVF, Flat)
- Integrating embedding providers (OpenAI, Qwen, SentenceTransformer, BM25)
- Performing hybrid search combining vector similarity with SQL-like filters
- Optimizing Zvec performance (threading, memory, quantization, compaction)

## Do not use this skill when

- You need a client-server vector database (use Milvus, Qdrant, Weaviate skills instead)
- Working with relational SQL databases (use `database-design` or `database-admin`)
- The task is unrelated to vector search or embeddings

## Instructions

- Clarify the use case: semantic search, RAG, recommendation, deduplication, etc.
- Apply the relevant rules from the categories below.
- Provide complete, runnable code examples using the Zvec Python SDK.
- If deep reference is needed, open `AGENTS.md` for the comprehensive manual.

## Rule Categories by Priority

| #   | Category                   | Impact       | Rules | Prefix         |
| --- | -------------------------- | ------------ | ----- | -------------- |
| 1   | Lifecycle & Initialization | **CRITICAL** | 1     | `lifecycle-`   |
| 2   | Schema Design              | **HIGH**     | 1     | `schema-`      |
| 3   | CRUD Operations            | **HIGH**     | 1     | `crud-`        |
| 4   | Search & Retrieval         | **HIGH**     | 1     | `search-`      |
| 5   | Indexing                   | **MEDIUM**   | 3     | `index-`       |
| 6   | Hybrid Search              | **MEDIUM**   | 1     | `hybrid-`      |
| 7   | Embedding Integration      | **MEDIUM**   | 1     | `embedding-`   |
| 8   | Performance                | **MEDIUM**   | 2     | `performance-` |

## Quick Reference

| Rule                                                            | Impact   | Description                                                         |
| --------------------------------------------------------------- | -------- | ------------------------------------------------------------------- |
| [lifecycle-init-once](rules/lifecycle-init-once.md)             | CRITICAL | `zvec.init()` must be called exactly once before any operation      |
| [schema-vector-types](rules/schema-vector-types.md)             | HIGH     | Choose correct DataType, dimensions, and metric for your embeddings |
| [crud-batch-operations](rules/crud-batch-operations.md)         | HIGH     | Always batch insert/upsert for 10-100x throughput                   |
| [search-metric-selection](rules/search-metric-selection.md)     | HIGH     | Match MetricType to your embedding model's training objective       |
| [index-hnsw-tuning](rules/index-hnsw-tuning.md)                 | MEDIUM   | Tune HNSW M, ef_construction, ef for recall/speed tradeoff          |
| [index-ivf-tuning](rules/index-ivf-tuning.md)                   | MEDIUM   | Tune IVF nlist/nprobe for billion-scale datasets                    |
| [hybrid-filter-first](rules/hybrid-filter-first.md)             | MEDIUM   | Combine vector search with scalar filters effectively               |
| [embedding-provider-config](rules/embedding-provider-config.md) | MEDIUM   | Configure embedding functions (OpenAI, Qwen, local models)          |
| [performance-optimize](rules/performance-optimize.md)           | MEDIUM   | When and how to call `collection.optimize()`                        |
| [performance-threading](rules/performance-threading.md)         | LOW      | Thread and memory configuration for containers/production           |

## Capabilities

### Core Database Operations

- **Schema**: `CollectionSchema`, `VectorSchema`, `FieldSchema` with typed columns
- **Lifecycle**: `zvec.init()`, `zvec.create_and_open()`, `zvec.open()`, `collection.flush()`, `collection.destroy()`
- **CRUD**: `insert()`, `upsert()`, `update()`, `delete()`, `delete_by_filter()`, `fetch()`

### Vector Search

- **Dense vectors**: FP32, FP16, BF16, INT8
- **Sparse vectors**: Native sparse embedding support
- **Multi-vector**: Multiple vector fields per document
- **Metrics**: Inner Product, L2, Cosine similarity
- **Query modes**: By vector or by document ID

### Indexing

- **HNSW**: Graph-based ANN for low-latency search
- **IVF**: Inverted file index for billion-scale datasets
- **Flat**: Brute-force exact search (baseline)
- **Inverted**: Scalar field indexing for filter acceleration

### Embedding Integrations

- OpenAI, Qwen (DashScope), SentenceTransformer, BM25
- Dense and sparse embedding functions
- Rerankers: RRF, Weighted, Qwen, custom

### Performance

- In-process: zero network latency
- Quantization: FP16, INT8 compression
- Background optimization and compaction
- Container-aware thread/memory auto-detection

## Example Interactions

- "Create a vector collection for storing 768-dim OpenAI embeddings with metadata"
- "Search similar documents using cosine similarity with category filters"
- "Set up HNSW index tuned for 99% recall on 1M vectors"
- "Integrate Qwen embeddings with Zvec for a Chinese-language RAG pipeline"
- "Optimize a Zvec collection running in a Docker container with 4GB RAM"
