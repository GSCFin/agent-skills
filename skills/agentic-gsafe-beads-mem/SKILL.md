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

> ⚠️ **CRITICAL (UNID Tracking):** If the document being decomposed into beads issues contains a Universal ID (UNID), the resulting beads issue description/message MUST explicitly mention that UNID to maintain traceability.
> 
> **XX-YYY-ZZZ Convention (Max 2 Hyphens):** All `beads-id` values use a strict 2-segment parent / 3-segment child format. Parent IDs have 1 hyphen (`prd-tplan`), section IDs have 2 hyphens (`prd-tplan-s1`). The `br-` prefix is NOT used. Category prefixes are: `prd` (specs), `pln` (plans), `doc` (context/records), `rev` (reviews). IDs are short human-chosen abbreviations, never auto-generated from file paths.
> 
> **Single-Line Metadata Rule:** Any HTML comment metadata containing `beads-id` and `satisfies` MUST be written strictly on a single line (e.g., `<!-- beads-id: pln-rdmap-s3 | satisfies: prd-tplan-s1 -->`). A single `beads-id` can satisfy one or multiple other `beads-id`s (comma-separated). Multi-line metadata blocks are strictly prohibited.
> 
> **Verification Gate & Proactive Checking:** ALWAYS run the bundled validation scripts (in this skill's `scripts/` directory) whenever you **change, add new, or delete** `beads-id` metadata in documents. If violations are found, you MUST fix them before proceeding.

**A healthy epic should have 2-4 tasks ready at any time.** This enables multi-agent parallelism without coordination chaos.

---

## Beads-ID Validation for `./docs/` (SSOT)

This skill ships with two Python scripts in `scripts/` to validate the consistency of `<!-- beads-id: ... -->` metadata across the project's `./docs/` directory (the Single Source of Truth for requirements, plans, and reviews).

### `scripts/extract_ids.py` — Extract & Stats

Recursively scans all `*.md` files and extracts every `<!-- beads-id: ... -->` tag.

```bash
# Full JSON extraction (all IDs with file, line, satisfies)
python3 .agents/skills/agentic-gsafe-beads-mem/scripts/extract_ids.py ./docs

# Quick stats: hyphen counts + violation check
python3 .agents/skills/agentic-gsafe-beads-mem/scripts/extract_ids.py ./docs --stats
```

**`--stats` output example:**
```text
Total Unique Beads: 483

  1 hyphens ->   26 beads  [Parents (base docs)]
  2 hyphens ->  457 beads  [Children (sections)]

✅ All IDs comply with the 2-hyphen max convention.
```

### `scripts/verify_hierarchy.py` — Parent-Child Integrity

Confirms every 2-hyphen child ID has a matching 1-hyphen parent. **Exits with code 1 if orphans are found** (CI-friendly).

```bash
python3 .agents/skills/agentic-gsafe-beads-mem/scripts/verify_hierarchy.py ./docs
```

**Output example:**
```text
## Beads-ID Hierarchy Verification

  Parents  (1 hyphen):  26
  Children (2 hyphens): 457
  Matched to parent:    457
  Orphans:              0

✅ All children have valid parents. Zero orphans.
```

### When to Run

- **After any docs edit** that adds, removes, or modifies `<!-- beads-id: ... -->` tags
- **During session bookends** — run alongside `bv --robot-triage` at session start/end
- **Before `bd sync`** — ensure metadata SSOT is clean before pushing

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

---

## Command Help References

> ⚠️ **CRITICAL INSTRUCTION FOR AGENTS:** DO NOT execute `bd help` or `bd update --help` in the terminal to learn how to use the commands. The complete help outputs are provided below to save time and tokens. Read them here directly.

### `bd help`

```text
Agent-first issue tracker (SQLite + JSONL)

Usage: bd [OPTIONS] <COMMAND>

Commands:
  agents       Manage AGENTS.md workflow instructions
  audit        Record and label agent interactions (append-only JSONL)
  blocked      List blocked issues
  changelog    Generate changelog from closed issues
  close        Close an issue
  comments     Manage comments
  completions  Generate shell completions
  config       Configuration management
  count        Count issues with optional grouping
  create       Create a new issue
  defer        Defer issues (schedule for later)
  delete       Delete an issue (creates tombstone)
  dep          Manage dependencies
  doctor       Run read-only diagnostics
  epic         Epic management commands
  graph        Visualize dependency graph
  history      Manage local history backups
  info         Show diagnostic metadata about the workspace
  init         Initialize a beads workspace
  label        Manage labels
  lint         Check issues for missing template sections
  list         List issues
  orphans      List orphan issues (referenced in commits but open)
  q            Quick capture (create issue, print ID only)
  query        Manage saved queries
  ready        List ready issues (unblocked, not deferred)
  reopen       Reopen an issue
  schema       Emit JSON Schemas for br output types (for agent/tooling integration)
  search       Search issues
  show         Show issue details
  stale        List stale issues
  stats        Show project statistics
  status       Alias for stats
  sync         Sync database with JSONL file (export or import)
  undefer      Undefer issues (make ready again)
  update       Update an issue
  upgrade      Upgrade br to the latest version
  version      Show version information
  where        Show the active .beads directory
  help         Print this message or the help of the given subcommand(s)

Options:
      --db <DB>                      Database path (auto-discover .beads/*.db if not set)
      --actor <ACTOR>                Actor name for audit trail
      --json                         Output as JSON
      --no-daemon                    Force direct mode (no daemon) - effectively no-op in br v1
      --no-auto-flush                Skip auto JSONL export
      --no-auto-import               Skip auto import check
      --allow-stale                  Allow stale DB (bypass freshness check warning)
      --lock-timeout <LOCK_TIMEOUT>  `SQLite` busy timeout in ms
      --no-db                        JSONL-only mode (no DB connection)
  -v, --verbose...                   Increase logging verbosity (-v, -vv)
  -q, --quiet                        Quiet mode (no output except errors)
      --no-color                     Disable colored output
  -h, --help                         Print help
  -V, --version                      Print version
```

### `bd update --help`

```text
Update an issue

Usage: bd update [OPTIONS] [IDS]...

Arguments:
  [IDS]...  Issue IDs to update

Options:
      --title <TITLE>
          Update title
      --description <DESCRIPTION>
          Update description [aliases: --body]
      --design <DESIGN>
          Update design notes
      --acceptance-criteria <ACCEPTANCE_CRITERIA>
          Update acceptance criteria [aliases: --acceptance]
      --notes <NOTES>
          Update additional notes
  -s, --status <STATUS>
          Change status
  -p, --priority <PRIORITY>
          Change priority (0-4 or P0-P4)
  -t, --type <TYPE>
          Change issue type
      --assignee <ASSIGNEE>
          Assign to user (empty string clears)
      --owner <OWNER>
          Set owner (empty string clears)
      --claim
          Atomic claim (assignee=actor + `status=in_progress`)
      --force
          Force update even if issue is blocked
      --due <DUE>
          Set due date (empty string clears)
      --defer <DEFER>
          Set defer until date (empty string clears)
      --estimate <ESTIMATE>
          Set time estimate
      --add-label <ADD_LABEL>
          Add label(s)
      --remove-label <REMOVE_LABEL>
          Remove label(s)
      --set-labels <SET_LABELS>
          Set label(s) (replaces all) - repeatable like bd
      --parent <PARENT>
          Reparent to new parent (empty string removes parent)
      --external-ref <EXTERNAL_REF>
          Set external reference
      --session <SESSION>
          Set `closed_by_session` when closing
      --db <DB>
          Database path (auto-discover .beads/*.db if not set)
      --actor <ACTOR>
          Actor name for audit trail
      --json
          Output as JSON
      --no-daemon
          Force direct mode (no daemon) - effectively no-op in br v1
      --no-auto-flush
          Skip auto JSONL export
      --no-auto-import
          Skip auto import check
      --allow-stale
          Allow stale DB (bypass freshness check warning)
      --lock-timeout <LOCK_TIMEOUT>
          `SQLite` busy timeout in ms
      --no-db
          JSONL-only mode (no DB connection)
  -v, --verbose...
          Increase logging verbosity (-v, -vv)
  -q, --quiet
          Quiet mode (no output except errors)
      --no-color
          Disable colored output
  -h, --help
          Print help
```
