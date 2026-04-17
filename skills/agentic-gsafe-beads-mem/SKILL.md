---
name: agentic-gsafe-beads-mem
description: >-
  Use Beads (bd CLI) and Beads Viewer (bv) as persistent memory and graph-aware
  triage engine for AI coding agents. Covers session workflow, issue management,
  dependency tracking, graph intelligence, cognitive offloading, and multi-agent
  coordination. Triggers: beads, bd, bv, issue tracker, task tracking, agent memory,
  triage, graph metrics, PageRank, bottleneck, critical path.
license: MIT
risk: safe
source: self
metadata:
  author: agenticse
  version: "2.0.0"
---

# Beads Agent Memory & Intelligence

Beads is a git-backed graph issue tracker for AI coding agents. It consists of two complementary tools:

- **`bd`** (Beads CLI) — The **execution layer**. Writes memory: create, claim, close, and sync issues. Solves the **"Dementia Problem"** — agents losing memory between sessions.
- **`bv`** (Beads Viewer) — The **intelligence layer**. Reads the dependency graph: computes PageRank, bottlenecks, critical paths, and cycles. Solves the **"Flat List Problem"** — agents working on the wrong task because they can't see project structure.

**Mental model:** `bd create` writes to local SQLite, auto-exports to `.beads/beads.jsonl` (git-tracked). `bv` reads that JSONL and treats it as a DAG, computing 9 graph metrics to surface what truly matters. Git IS the database. No central server needed.

**Positioning:** Beads is an **execution tool**, not a backlog. It tracks this week's work, not distant ideas. Keep `bd ready` crisp and actionable.

## When to Apply

- Starting or ending any coding agent session
- Work spanning multiple sessions or context windows
- Tracking bugs discovered during implementation
- Planning large features as epics with subtasks
- Coordinating work across multiple agents
- When you need to understand project health, bottlenecks, or what to work on next

---

## Core Thinking: Execution with `bd`

### Think → Create → Act

1. **Think** — Describe the problem, investigate with the AI
2. **Create** — Capture discovered work as structured issues
3. **Act** — Work through `bd ready`, close when done

**Issues are handoff points.** Kill a session, start fresh — the new agent runs `bd ready` and picks up exactly where you left off.

### Essential Commands

```bash
bd ready --json                        # What's unblocked right now?
bd create "Fix auth bug" -t bug -p 1 --json   # File discovered work
bd close <id> --reason "Done" --json   # Land the plane
```

For the full command reference, see [bd CLI Reference](references/bd-cli-reference.md).

### Key Principles

- **File issues liberally** — anything over ~2 minutes of work. More issues = less work forgotten between sessions.
- **Always use `--json`** — structured output for agents. Never parse human-readable output with regex.
- **DO NOT use `bd edit`** — it opens `$EDITOR` (interactive). Use `bd update <id> --description "..."` instead.
- **Right-size issues for agents** — aim for 30-minute vertical slices. One issue = one focused session that leaves the system in a working state. A task requiring changes in 5 unrelated places is too broad; a task that renames one variable is too small.

### Workflow Modes

- **Prompt-First (Reactive):** See a bug → investigate → file issues as the plan emerges → execute. Best for ad-hoc work.
- **Issue-First (Planned):** Know the work → create the issue with acceptance criteria → tell the agent "work on bd-a1b2." Best for planned features.
- **Hybrid (Specs + Beads):** Create a detailed spec externally, iterate 3-5x, then import as Beads epics. The spec provides the "why"; Beads provides the "what's next." Best for large features.

---

## Core Thinking: Intelligence with `bv`

### The Cognitive Offloading Principle

LLMs are excellent at semantic reasoning but unreliable at algorithmic graph traversal. If you feed an agent raw `beads.jsonl`, you force it to parse thousands of lines, reconstruct the dependency graph in its context window, and "hallucinate" path traversals. **Don't do this.**

`bv` acts as a deterministic graph engine sidecar. It computes 9 graph metrics (PageRank, Betweenness, HITS, Critical Path, Eigenvector, Degree, Density, Cycles, Topological Sort) and returns pre-computed answers. Use `bv` instead of parsing JSONL — it transforms raw data into strategic intelligence.

### Essential Commands

```bash
bv --robot-triage          # THE mega-command: start every session here
bv --robot-next            # Minimal: just the single top pick + claim command
bv --robot-insights        # Full graph metrics (PageRank, cycles, bottlenecks)
```

> ⚠️ **CRITICAL: Never run bare `bv`** — it launches an interactive TUI that blocks your session. Always use `--robot-*` flags.

For the full command reference, see [bv Robot Reference](references/bv-robot-reference.md).

### The 3-Phase Agent Workflow

1. **Triage & Orientation:** Run `bv --robot-triage`. Immediately know: "Task C depends on Task B, which is a bottleneck" and "The graph has a cycle that must be fixed first."
2. **Impact Analysis:** Before refactoring a module, check its PageRank and Impact Score. High scores = high-risk change with many downstream dependents. Run more comprehensive tests.
3. **Execution Planning:** Use the topological sort to generate a strictly linearized plan. Don't guess the order — let the graph tell you.

### Token Optimization with TOON

For lower context usage (~50% fewer tokens), use TOON format:

```bash
bv --robot-triage --format toon
# Or set globally:
export BV_OUTPUT_FORMAT=toon
```

---

## Session Bookends (CRITICAL)

Every agent session follows this bookend structure:

```bash
# ── START ──
bv --robot-triage                          # Graph-aware orientation
bd show <top-pick-id> --json               # Review before starting
bd update <id> --claim --json              # Atomically claim it

# ── WORK ──
# Implement, test, commit as normal
# File discovered bugs along the way:
bd create "Found edge case" -t bug -p 1 --deps discovered-from:<id> --json

# ── END ("Land the Plane") ──
bd close <id> --reason "Done" --json       # Close completed work
bd sync                                    # Export → commit → pull → import → push
git pull --rebase && git push              # MANDATORY — not done until push succeeds
bv --robot-triage                          # Generate handoff for next session
```

**The plane isn't landed until `git push` succeeds.** Without `bd sync`, changes sit in a 30-second debounce window and may never reach git.

### Why Short Sessions Win

**Restart agents after each task.** One task → land the plane → kill → start fresh.

- Context rot happens in long sessions — by hour two, the agent forgets about Beads
- Models perform better with fresh context
- Fine-grained issues (30-min tasks) make sessions cheap and throwaway
- **If context rot is happening, your session is too long.**

---

## Decomposing Plans into Beads

The hardest part isn't the CLI — it's the **software engineering judgment** to split a plan into well-structured, dependency-aware issues.

### Split by Architectural Boundary, Not File Count

**Bad:** "Update user model" / "Update user controller" / "Update user template" — these are one logical change.

**Good:** "Add email field to user profile" / "Build email verification API endpoint" / "Add email verification UI" — each is a **vertical slice** that takes the system from one working state to another.

### The 5-Step Decomposition

1. **Identify boundaries** — Split by responsibility, not by file
2. **Create epics** — One per major milestone
3. **Decompose into 30-minute tasks** — One focused agent session each
4. **Wire dependencies** — Ask: "Can an agent start B without A being done?"
5. **Review the critical path** — Trace the longest blocking chain. Look for decoupling opportunities.

**A healthy epic should have 2-4 tasks ready at any time.** This enables multi-agent parallelism without coordination chaos.

---

## Multi-Agent Coordination

```bash
bd update <id> --claim --json    # Atomic claiming — fails if already claimed
```

- **Hash-based IDs** (`bd-a3f2`) prevent merge collisions when multiple agents create issues simultaneously
- **Git Worktrees:** Each agent gets its own worktree and branch. Beads syncs via git.
- **Agent Mail:** Pair Beads (shared memory) with MCP Agent Mail (messaging) for real-time coordination. Use bead IDs as thread IDs: `send_message(..., thread_id="bd-123")`

---

## Honest Gaps

- Agents **don't proactively use Beads** — you must say "check bd ready" or "track this in beads"
- AGENTS.md instructions fade by session end — prompt "land the plane" explicitly
- Context rot still happens in long sessions — fix with shorter sessions
- Collaboration requires explicit sync branch setup for protected branches

**The tool provides the memory. You provide the discipline to use it.**

---

## Agent Execution Rules (Lessons Learned)

When scripting `bd` execution via bash or executing tools agentically, **prevent silent failures** by adhering to the following rules:

1. **Always verify `.beads/` exists** or run `bd init` before executing any `bd create` commands. If skipped, `bd` improperly writes to the global `~/.beads` directory.
2. **Use `set -ex` instead of `set -e`** for long bash scripts. `set -e` fails silently when commands error out. Using `-x` (trace) ensures all executed variables are visibly logged for agent debugging.
3. **Do not hallucinate global CLI flags**. For instance, `bd create` supports `--silent` to output strictly the ID (`epic1=$(bd create ... --silent)`), but `bd delete` will crash the script if padded with `--silent`. Always verify via `bd <cmd> --help`.

---

## References (Progressive Disclosure)

**Layer 2 — Command Details:**
- [bd CLI Reference](references/bd-cli-reference.md) — Full command tables, filtering, epics, dependencies, maintenance
- [bv Robot Reference](references/bv-robot-reference.md) — All 30+ robot commands, 9 metrics, output schemas, recipes

**Layer 3 — Deep Reference:**
- [Installation Guide](references/installation.md) — Installing bd and bv, init modes, Claude Code hooks
- [bd Troubleshooting](references/bd-troubleshooting.md) — Common pitfalls, merge conflicts, database recovery
- [bv Troubleshooting](references/bv-troubleshooting.md) — TUI blocking, stale metrics, large graph handling
