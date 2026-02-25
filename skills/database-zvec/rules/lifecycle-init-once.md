---
title: Initialize Zvec Exactly Once
impact: CRITICAL
impactDescription: "RuntimeError on double-init; undefined behavior if skipped"
tags: [lifecycle, initialization, zvec]
---

## Initialize Zvec Exactly Once

`zvec.init()` must be called exactly once per process before any collection
operation. Calling it again raises `RuntimeError`. Skipping it causes undefined
behavior or silent crashes.

**Incorrect (no init):**

```python
import zvec

schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)
collection = zvec.create_and_open("./data", schema)
# May crash or produce corrupt data — zvec.init() was never called
```

**Incorrect (double init):**

```python
zvec.init()
# ... later in code ...
zvec.init()  # RuntimeError: Zvec is already initialized
```

**Correct (init once at startup):**

```python
import zvec

zvec.init()  # Call once at application entry point

schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)
collection = zvec.create_and_open("./data", schema)
```

**Best: guard with a module-level flag:**

```python
_initialized = False

def ensure_zvec():
    global _initialized
    if not _initialized:
        zvec.init()
        _initialized = True
```

Reference: [Zvec Quickstart](https://zvec.org/en/docs/quickstart/)
