# The Coordination Loop

This document describes the unified workflow that ties all G-SAFE tools together:
**Beads (`br`) → Beads Viewer (`bv`) → Agent Mail → UBS (`ubs`) → CASS (`cass`)**

## The Full Loop

### Phase 1: Session Start

```bash
# 1. Register with Agent Mail (multi-agent only)
macro_start_session(project_key="<repo>", agent_name="<identity>")

# 2. Find work — two options:
br ready --json                    # Simple: what's unblocked?
bv --robot-priority               # Smart: what has highest impact?

# 3. Claim the task
br update <id> --claim --json      # Atomic — fails if already claimed

# 4. Search for prior art & Codebase context
fastcode --repo . query "Where is the code for <task keywords>?"
cass search "<task keywords>" --robot --limit 5
```

### Phase 2: Reserve & Announce

```bash
# 5. Calculate blast radius
bv --robot-plan <id>

# 6. Reserve files (multi-agent only)
file_reservation_paths(
  paths=<from plan>,
  reason="<id>",
  exclusive=true
)

# 7. Announce in thread
send_message(thread_id="<id>", subject="[<id>] Starting <title>")
```

### Phase 3: Implementation

```bash
# 8. Implement, test, commit — reference <id> in commit messages

# 9. Track discovered work
br create "Found edge case" -t bug -p 1 --deps discovered-from:<id> --json

# 10. Quality gate (on each significant change)
ubs <changed-files> --format=json
# Fix all 🔥 Critical → re-scan → until exit 0
```

### Phase 4: Landing the Plane

**MANDATORY: The plane is NOT landed until git push succeeds. NEVER say "ready to push when you are".**

```bash
# 11. Final quality scan
ubs $(git diff --name-only --cached) --format=json

# 12. File remaining work & close the task
br create "Follow-up task" -t task -p 2 --json
br close <id> --reason "Completed" --json

# 13. Sync & push (CRITICAL)
br sync
git pull --rebase
git push                           # MUST SUCCEED
git status                         # MUST show "up to date"

# 14. Clean up git state
git stash clear
git remote prune origin

# 15. Release files (multi-agent only)
release_file_reservations(reason="<id>")

# 16. See what you unblocked & announce
bv --robot-diff
send_message(thread_id="<id>", subject="[<id>] Completed")

# 17. Generate handoff & provide user prompt
br ready --json
br show <next-id> --json
# Prompt user: "Continue work on bd-X: [title]. [Context]"
```

## Single-Agent Simplified Loop

When working alone, skip Agent Mail steps (register, reserve, announce, release):

```bash
br ready --json → br update <id> --claim --json → WORK
→ ubs <files> --format=json → br close <id> --json
→ br sync && git push → br ready --json
```

## Multi-Agent Scaling: The Agent Village

1. **Plan**: Create detailed plan externally
2. **Scaffold**: Generate directory structure
3. **Task**: Agent files Beads epics with `br create ... --parent <epic>`
4. **Swarm**: Launch multiple agents, each:
   - Registers with Agent Mail
   - Checks `bv --robot-priority` for work
   - Reserves files → Works → Scans → Closes → Releases
5. **Monitor**: Human overseer watches via `http://127.0.0.1:8765/mail`

## Cross-Tool Integration Map

```
┌─────────┐     thread_id = br-###     ┌────────────┐
│  Beads  │◄──────────────────────────►│ Agent Mail │
│  (bd)   │     reason = br-###        │  (MCP)     │
└────┬────┘                            └─────┬──────┘
     │ issues                                │ reserved files
     ▼                                       ▼
┌─────────┐                            ┌────────────┐
│  Beads  │  graph metrics             │    UBS     │
│ Viewer  │  (PageRank, HITS,          │  (ubs)     │
│  (bv)   │   critical path)           │ pre-commit │
└─────────┘                            └────────────┘
     ▲                                       ▲
     │ intelligence                          │ past solutions
     │                                       │
     └──────────┐               ┌────────────┘
                │               │
  ┌─────────────┴──┐        ┌───┴───────────────┴───┐
  │   FastCode     │        │        CASS           │
  │(code context)  │        │  (session search)     │
  └────────────────┘        └───────────────────────┘
```

## Key Principle

> Beads gives agents shared memory, Agent Mail gives them messaging, CASS gives them history, UBS gives them quality, and Beads Viewer gives them intelligence — that's all they need.
