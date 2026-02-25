---
title: Thread and Memory Configuration for Containers
impact: LOW
impactDescription: "misconfigured threads/memory in containers causes OOM or underutilization"
tags: [performance, threading, memory, container, docker, kubernetes]
---

## Thread and Memory Configuration for Containers

Zvec auto-detects CPU cores and memory limits from cgroup (Docker/Kubernetes).
Override only when you need explicit control.

**Default behavior (recommended for most cases):**

```python
zvec.init()
# query_threads: auto-detected from cgroup CPU limits
# optimize_threads: same as query_threads
# memory_limit_mb: 80% of cgroup memory limit
```

**Explicit configuration (shared machines or multi-process):**

```python
zvec.init(
    query_threads=4,       # Dedicate 4 cores to queries
    optimize_threads=1,    # 1 background thread for compaction
    memory_limit_mb=2048,  # 2GB hard limit (leave room for app)
)
```

**Incorrect (over-provisioned in 4-core container):**

```python
zvec.init(
    query_threads=16,      # Only 4 cores available — thread contention
    optimize_threads=8,    # Starves query threads
    memory_limit_mb=16384, # Container only has 4GB — OOM kill
)
```

**Correct (match container resources):**

```python
zvec.init(
    query_threads=3,       # 3 of 4 cores for queries
    optimize_threads=1,    # 1 core for background tasks
    memory_limit_mb=3072,  # 3GB of 4GB — leave 1GB for app + OS
)
```

**Guideline:**

- `query_threads`: N-1 cores (leave 1 for optimize + app)
- `optimize_threads`: 1-2 threads
- `memory_limit_mb`: 60-80% of container memory
- When in doubt, omit all and let Zvec auto-detect

Reference: [Zvec Configuration](https://zvec.org/en/docs/)
