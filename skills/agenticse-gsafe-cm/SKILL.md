---
name: agenticse-gsafe-cm
description: >-
  Use CM (CASS Memory System) for cross-agent procedural memory. Transforms
  scattered agent sessions into persistent, confidence-tracked playbook rules
  so every agent learns from every other agent's experience.
  Triggers: cm, cass memory, playbook, agent memory, cross-agent learning.
license: MIT
risk: safe
source: self
metadata:
  author: agenticse
  version: "1.0.0"
---

# CM: CASS Memory System

CM (`cm`) is procedural memory for AI coding agents. It transforms scattered agent sessions into persistent, cross-agent memory — so every agent learns from every other agent's experience.

**Mental model:** Three-layer cognitive architecture: **Episodic** (raw sessions via `cass`) → **Working** (structured diary entries) → **Procedural** (distilled playbook rules with confidence tracking). Rules decay without revalidation. Bad rules become anti-pattern warnings.

## When to Apply

- Before starting any non-trivial coding task (retrieve context)
- After completing tasks (record outcomes)
- When building institutional memory across multiple AI agents
- When onboarding a new project to capture existing patterns
- When a rule helped or hurt during implementation (leave feedback)

---

## Quickstart

### Installation

```bash
# Homebrew (recommended)
brew install dicklesworthstone/tap/cm

# Or via install script
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/cass_memory_system/main/install.sh?$(date +%s)" \
  | bash -s -- --easy-mode --verify

# Initialize
cm init
# Or with a starter playbook
cm init --starter typescript  # also: react, python, go
```

### Prerequisites

- **cass CLI** (episodic memory layer) — install via the `agentic-gsafe-cass` skill
- **LLM API Key** (optional) — for AI-powered reflection. Set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_GENERATIVE_AI_API_KEY`

---

## The One Command You Need

```bash
cm context "<your task>" --json
```

**Run this before starting any non-trivial task.** It returns:

```json
{
  "relevantBullets": [
    { "id": "b-8f3a2c", "content": "...", "effectiveScore": 8.5 }
  ],
  "antiPatterns": [
    { "id": "b-x7k9p1", "content": "Don't cache auth tokens without expiry" }
  ],
  "historySnippets": [{ "agent": "claude", "snippet": "Fixed timeout by..." }],
  "suggestedCassQueries": [
    "cass search 'authentication timeout' --robot --days 30"
  ]
}
```

**Always use `--json`** for structured output. `stdout` = data only, `stderr` = diagnostics, exit `0` = success.

---

## Session Protocol

```
1. START  → cm context "<task>" --json     # Get relevant rules & history
2. WORK   → Reference rule IDs when following them ("Following b-8f3a2c...")
3. FEEDBACK → Leave inline comments when rules help/hurt
4. END    → Just finish. Learning happens automatically.
```

### Inline Feedback

When a rule helps or hurts during work, leave inline comments in your code:

```typescript
// [cass: helpful b-8f3a2c] - this rule saved me from a rabbit hole
// [cass: harmful b-x7k9p1] - this advice was wrong for our use case
```

These are automatically parsed during reflection and update rule confidence.

### Outcome Recording

```bash
# Record success with rule IDs that helped
cm outcome success b-8f3a2c,b-xyz789 --summary "Fixed auth bug"

# Record failure
cm outcome failure b-x7k9p1 --summary "Rule led to wrong approach"

# Apply recorded outcomes to playbook
cm outcome-apply
```

---

## Playbook Management

### Confidence Decay System

Rules aren't immortal:

- **90-day half-life**: Confidence halves every 90 days without revalidation
- **4× harmful multiplier**: One mistake counts 4× as much as one success
- **Maturity progression**: `candidate` → `established` → `proven`

### Anti-Pattern Learning

Bad rules automatically become warnings:

```
"Cache auth tokens for performance"
    ↓ (3 harmful marks)
"PITFALL: Don't cache auth tokens without expiry validation"
```

### Adding Rules

```bash
# Single rule
cm playbook add "Always check token expiry before auth debugging" --category "debugging"

# Batch add from JSON
cm playbook add --file rules.json

# Track source session
cm playbook add --file rules.json --session /path/to/session.jsonl
```

---

## Agent-Native Onboarding

Build a playbook from scratch using your existing AI agent (zero additional cost):

```bash
# 1. Check progress
cm onboard status --json

# 2. Get sessions prioritized by playbook gaps
cm onboard sample --fill-gaps --json

# 3. Read session with rich context
cm onboard read /path/to/session.jsonl --template --json

# 4. Add extracted rules
cm playbook add --file rules.json --session /path/to/session.jsonl

# 5. Mark done
cm onboard mark-done /path/to/session.jsonl
```

### Gap Categories

`debugging` · `testing` · `architecture` · `workflow` · `documentation` · `integration` · `collaboration` · `git` · `security` · `performance`

| Status             | Rule Count | Priority |
| ------------------ | ---------- | -------- |
| `critical`         | 0 rules    | High     |
| `underrepresented` | 1-2 rules  | Medium   |
| `adequate`         | 3-10 rules | Low      |
| `well-covered`     | 11+ rules  | None     |

---

## Token Budget

| Flag            | Effect                                     |
| --------------- | ------------------------------------------ |
| `--limit N`     | Cap number of rules returned               |
| `--min-score N` | Only rules above score threshold           |
| `--no-history`  | Skip historical snippets (faster, smaller) |
| `--json`        | Structured output for parsing              |

---

## What NOT to Do

- **Don't** run `cm reflect` manually — automation handles this
- **Don't** run `cm mark` manually — use inline comments instead
- **Don't** manually add rules to the playbook YAML file
- **Don't** worry about the learning pipeline — it's automatic

---

## Graceful Degradation

| Condition   | Behavior                                          |
| ----------- | ------------------------------------------------- |
| No cass     | Playbook-only scoring, no history snippets        |
| No playbook | Empty playbook, commands still work               |
| No LLM      | Deterministic reflection, no semantic enhancement |
| Offline     | Cached playbook + local diary                     |

---

## Honest Gaps

- Requires `cass` for full episodic memory (works without, but degraded)
- LLM API key needed for AI-powered reflection (deterministic fallback available)
- Anti-pattern inversion is automatic but imperfect — review periodically
- Confidence decay means old rules silently lose weight — good rules need periodic revalidation
