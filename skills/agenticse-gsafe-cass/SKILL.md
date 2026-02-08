---
name: agentic-gsafe-cass
description: >-
  Use CASS (Coding Agent Session Search) to index and search across all local
  coding agent history. Aggregates sessions from Claude Code, Codex, Cursor,
  Gemini CLI, Aider, and more into a single searchable timeline.
  Triggers: cass, session search, agent history, cross-agent search.
license: MIT
risk: safe
source: self
metadata:
  author: agenticse
  version: "1.0.0"
---

# CASS: Coding Agent Session Search

CASS (`cass`) is a unified, high-performance search engine for your local coding agent history. It aggregates sessions from **Codex, Claude Code, Gemini CLI, Cline, OpenCode, Amp, Cursor, ChatGPT, Aider, Pi-Agent, and Factory** into a single searchable timeline.

**Mental model:** `cass index` normalizes all agent session formats into a common schema with full-text + optional semantic search. `cass search --robot` returns structured JSON results. Everything stays local — nothing phones home.

## When to Apply

- Searching for solutions you've encountered in previous agent sessions
- Finding debugging strategies across any AI coding agent you've used
- Building cross-agent institutional memory
- Investigating patterns across your coding history
- Feeding context to CM (CASS Memory) for playbook building

---

## Quickstart

### Installation

```bash
# Homebrew (recommended)
brew install dicklesworthstone/tap/cass

# Or via install script
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/coding_agent_session_search/main/install.sh?$(date +%s)" \
  | bash -s -- --easy-mode --verify
```

### First Search

```bash
# Build the index (one-time, ~30s)
cass index --full

# Search across all agent history
cass search "authentication error" --robot --limit 5

# View a specific hit
cass view /path/to/session.jsonl -n 42 --json

# Expand context around a hit
cass expand /path/to/session.jsonl -n 42 -C 3 --json
```

---

## Critical Rules

⚠️ **Never run bare `cass` in an agent context** — it launches the interactive TUI. Always use `--robot` or `--json`.

**Always use `--robot`** for machine-readable output. `stdout` = data only, `stderr` = diagnostics, exit `0` = success.

**DO NOT parse human-readable output.** Use `--robot` or `--robot-format jsonl` for structured data.

---

## Core Commands

### Health Check

```bash
cass health --json || cass index --full
```

Run before searching. If health fails, rebuild the index.

### Search

```bash
# Basic search
cass search "error handling" --robot --limit 10

# Filter by agent
cass search "auth" --agent claude --robot

# Filter by recency
cass search "bug fix" --today --robot
cass search "refactor" --since 7d --robot

# Minimal fields (saves tokens)
cass search "deploy" --robot --fields minimal --limit 5

# Token budget control
cass search "error" --robot --max-tokens 2000 --limit 5
```

### Search Modes

| Mode                  | Flag              | Best For                            |
| --------------------- | ----------------- | ----------------------------------- |
| **Lexical** (default) | `--mode lexical`  | Exact term matching, code searches  |
| **Semantic**          | `--mode semantic` | Conceptual queries ("find similar") |
| **Hybrid**            | `--mode hybrid`   | Balanced precision and recall       |

### View & Expand

```bash
# View a specific hit (use source_path/line_number from search)
cass view /path/to/session.jsonl -n 42 --json

# Expand context (5 messages before/after)
cass expand /path/to/session.jsonl -n 42 -C 5 --json
```

### Chained Search

```bash
# Find sessions about "auth", then drill into "token refresh"
cass search "authentication" --robot-format sessions | \
  cass search "refresh token" --sessions-from - --robot
```

---

## Token Budget Management

| Flag                       | Effect                                     |
| -------------------------- | ------------------------------------------ |
| `--fields minimal`         | Only `source_path`, `line_number`, `agent` |
| `--fields summary`         | Adds `title`, `score`                      |
| `--max-content-length 500` | Truncate long fields (UTF-8 safe)          |
| `--max-tokens 2000`        | Soft budget (~4 chars/token)               |
| `--limit N`                | Cap number of results                      |

---

## Error Handling

Errors are structured JSON with recovery hints:

```json
{
  "error": {
    "code": 3,
    "kind": "index_missing",
    "message": "Search index not found",
    "hint": "Run 'cass index --full' to build the index",
    "retryable": false
  }
}
```

| Exit Code | Meaning             | Action                     |
| --------- | ------------------- | -------------------------- |
| 0         | Success             | Parse stdout               |
| 1         | Health check failed | `cass index --full`        |
| 2         | Usage error         | Fix syntax (hint provided) |
| 3         | Index/DB missing    | `cass index --full`        |
| 7         | Lock/busy           | Retry later                |

---

## Self-Documenting API

```bash
cass robot-docs guide      # Quick-start for agents
cass robot-docs commands   # All commands and flags
cass robot-docs schemas    # Response JSON schemas
cass capabilities --json   # Feature detection
```

---

## Multi-Machine Search

```bash
# Interactive setup wizard
cass sources setup

# Or manual
cass sources add user@laptop.local --preset macos-defaults
cass sources sync
cass sources doctor
```

Sessions from remotes are indexed alongside local sessions with provenance tracking (`source_id`, `source_kind`).

---

## Forgiving Syntax

CASS auto-corrects common agent mistakes:

| Input                  | Interpreted As           |
| ---------------------- | ------------------------ |
| `cass serach "error"`  | `cass search "error"`    |
| `cass -robot -limit=5` | `cass --robot --limit=5` |
| `cass find "auth"`     | `cass search "auth"`     |

Corrections go to stderr as teaching notes.

---

## Honest Gaps

- Semantic search requires manual model file install (~90MB); hash fallback provides lexical overlap only
- Index rebuild needed after first install (`cass index --full`)
- TUI mode is powerful but **never safe in agent contexts** — always use `--robot`
