# bd CLI Reference

Full command reference for the Beads CLI (`bd`). For thinking guidance and best practices, see the main [SKILL.md](../SKILL.md).

---

## Installation

```bash
# Install via script
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

# Or via Homebrew
brew tap steveyegge/beads && brew install beads
```

## Initialize

```bash
bd init                    # Interactive setup (creates .beads/ directory)
bd init --quiet            # Non-interactive (for agents)
bd init --stealth          # Local-only, no repo pollution
bd init --contributor      # OSS fork workflow
bd init --team             # Team member with commit access
```

---

## Issue Lifecycle

### Creating Issues

```bash
bd create "Fix auth bug" -t bug -p 1 --json
bd create "Add dark mode" -t feature -p 2 -d "Toggle in settings" --json
bd create "Fix CSS" -t bug -p 2 -l frontend,urgent --json
bd create "Complex feature" --body-file=description.md -p 1 --json
bd create -f feature-plan.md --json               # Batch from markdown plan
```

### Viewing & Claiming

```bash
bd ready --json                    # Unblocked work only
bd show <id> --json                # Full issue details
bd update <id> --claim --json      # Atomically claim (fails if taken)
```

### Closing

```bash
bd close <id> --reason "Done" --json
```

### Updating

```bash
bd update <id> --description "..." --json
bd update <id> --priority 1 --json
bd update <id> --status in_progress --json
```

> **DO NOT use `bd edit`** — it opens `$EDITOR` interactively.

---

## Issue Types and Priorities

| Type      | Use Case                    | Priority | Meaning                        |
| --------- | --------------------------- | -------- | ------------------------------ |
| `bug`     | Something broken            | P0       | Critical (security, data loss) |
| `feature` | New functionality           | P1       | High (major features)          |
| `task`    | Tests, docs, refactoring    | P2       | Medium (nice-to-have)          |
| `epic`    | Large feature with children | P3       | Low (polish)                   |
| `chore`   | Maintenance, tooling        | P4       | Backlog (future ideas)         |

---

## Epics and Hierarchical Issues

```bash
# Create the epic
bd create "Auth System" -t epic -p 1 --json              # → bd-a3f8e9

# Create child tasks (auto-numbered)
bd create "Design login UI" -p 1 --parent bd-a3f8e9 --json      # → bd-a3f8e9.1
bd create "Backend validation" -p 1 --parent bd-a3f8e9 --json   # → bd-a3f8e9.2
bd create "Integration tests" -p 1 --parent bd-a3f8e9 --json    # → bd-a3f8e9.3

# View hierarchy
bd dep tree bd-a3f8e9
```

Supports up to 3 levels of nesting.

---

## Dependencies

```bash
bd dep add <child> <parent>            # Add blocking dependency
bd dep tree <id>                       # View dependency tree
bd dep cycles                          # Detect circular dependencies
```

| Type              | Affects Ready? | Purpose                                            |
| ----------------- | -------------- | -------------------------------------------------- |
| `blocks`          | **Yes**        | Hard dependency — X cannot start until Y completes |
| `parent-child`    | **Yes**        | Epic/subtask relationship                          |
| `related`         | No             | Connected but don't block each other               |
| `discovered-from` | No             | Audit trail of where work was found                |

### Tracking Discovered Work

```bash
bd create "Memory leak in image loader" -t bug -p 1 \
  --deps discovered-from:bd-100 --json
```

---

## Filtering and Search

> **Note:** Use `--label` for filtering by labels (NOT `--tag` — that flag does not exist).

```bash
bd list --status open --json                    # By status
bd list --priority 1 --json                     # By priority
bd list --type bug --json                       # By type
bd list --label bug,critical --json             # Labels (AND)
bd list --label-any frontend,backend --json     # Labels (OR)
bd list --title-contains "auth" --json          # Text search
bd list --no-assignee --json                    # Unassigned work
bd stale --days 30 --json                       # Stale issues
```

---

## Sync and Maintenance

```bash
bd sync                                        # Export → commit → pull → import → push
git pull --rebase && git push                   # MANDATORY after sync

bd admin cleanup --older-than 7 --force --json  # Delete old closed issues
bd admin compact --analyze --json               # Find compaction candidates
bd doctor --fix                                 # Diagnose and auto-fix
bd restore <id>                                 # Recover deleted issue from git
```

Cleanup never loses data — git history preserves everything. Start cleaning at ~200 issues, never exceed ~500.

---

## Claude Code Integration

```bash
bd setup claude              # Install hooks globally
bd setup claude --project    # Install for this project only
```

Adds hooks that run `bd prime` on session start and pre-compact events.
