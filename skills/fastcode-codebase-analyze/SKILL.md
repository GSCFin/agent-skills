---
name: fastcode-codebase-analyze
description: "Iteratively analyze codebases using FastCode's BM25 hybrid search. Replaces internal LLM-driven queryWithAgent() — agent coder drives the same tool_call loop with same confidence thresholds and stopping criteria. No API key needed."
allowed-tools: Bash(fastcode:*)
---

# FastCode Codebase Analyze

Spawn a SubAgent named `fastcode_codebase_analyze` to run the iterative search loop.

## How to Use

When the user asks to analyze a codebase, spawn a new agent named `fastcode_codebase_analyze` with the following task prompt. Replace `<repo-path>` and `<user-question>` with actual values:

```
You are fastcode_codebase_analyze. Your ONLY job is to search and analyze a codebase using fastcode CLI.

RULES:
- Use ONLY the `fastcode analyze` shell command. FORBIDDEN: SearchText, ReadFile, ReadDirectory, grep, cat, find.
- Do NOT run --help or fastcode index. Do NOT read reference/explain-call-flow.md.
- Do NOT delegate to any other agent or codebase_investigator.
- Ignore non-source files in results (docs/, iteration-reports/, .md files). Focus on .go, .py, .ts, .js.
- Do NOT query filenames. Query code identifiers and concepts.

TASK:
Analyze the codebase at <repo-path> to answer: <user-question>

STEP 1 — First search (must include --re-index):
  fastcode analyze --repo <repo-path> --query "<broad keywords from question>" --re-index

STEP 2 — Check results:
  If top result scores >= 0.3 and source code covers the question → go to STEP 4.
  Otherwise → STEP 3.

STEP 3 — Refine (max 2 more rounds):
  fastcode analyze --repo <repo-path> --query "<refined identifiers from step 1-2 results>"
  Stop as soon as you have enough context.

STEP 4 — Return this exact format:
  ## Codebase Analysis: <question>
  **Repo:** <name> | **Rounds:** <N> | **Confidence:** <0-100>% | **Stop:** <reason>
  ### Key Files
  1. `<path>` (score: <N>) — <description>
  ### Key Functions
  - `<Name>` in `<path>:L<start>-L<end>` — <purpose>
  ### Architecture Summary
  <answer to the question>
```

## Config

| Query Complexity                          | Max Rounds | Confidence Threshold |
| ----------------------------------------- | ---------- | -------------------- |
| Simple (< 30): "where is function X?"     | 2          | 95                   |
| Medium (30-60): "how does module Y work?" | 3          | 92                   |
| Complex (60+): "trace the full data flow" | 4          | 85                   |

## Stopping Conditions

| Condition                 | Stop Reason                    |
| ------------------------- | ------------------------------ |
| `confidence >= threshold` | `confidence_threshold_reached` |
| `round >= max_rounds`     | `max_rounds`                   |
| No more useful queries    | `no_more_actions`              |
| `gathered_elements >= 50` | `budget_exhausted`             |
