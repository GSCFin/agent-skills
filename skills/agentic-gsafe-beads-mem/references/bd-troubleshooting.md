# bd Troubleshooting

Common issues and debugging guidance for the Beads CLI (`bd`).

---

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `bd edit` blocks the session | Opens `$EDITOR` interactively | Use `bd update <id> --description "..."` instead |
| Changes not visible to collaborators | `bd sync` not run, or `git push` not done | Run `bd sync` then `git pull --rebase && git push` |
| Human-readable output breaks parsing | Missing `--json` flag | **Always** use `--json` for structured agent output |
| `bd ready` returns too many items | Database too large or priorities too flat | Clean with `bd admin cleanup --older-than 7 --force --json` |
| Claiming fails | Another agent already claimed the issue | Check `bd show <id> --json` for current assignee |
| `--tag` flag doesn't work | Flag doesn't exist | Use `--label` for label filtering |

---

## Sync Failures

The `bd sync` command performs: export → commit → pull → import → push. If it fails:

```bash
# 1. Check git status
git status

# 2. Try manual sync
bd sync --flush-only          # Export-only (no git operations)
git add .beads/
git commit -m "beads sync"
git pull --rebase
git push
```

---

## Merge Conflicts

Beads is self-healing through git. Even corrupted databases can be reconstructed:

```bash
# If .beads/beads.jsonl has conflicts:
# 1. Accept the incoming version
git checkout --theirs .beads/beads.jsonl
git add .beads/beads.jsonl
git commit

# 2. Re-import
bd sync

# If the SQLite database is corrupted:
# Delete it and re-import from JSONL (the JSONL in git is the source of truth)
rm .beads/beads.db
bd sync
```

---

## Database Maintenance

```bash
bd doctor --fix                                 # Diagnose and auto-fix common issues
bd admin cleanup --older-than 7 --force --json  # Delete old closed issues
bd admin compact --analyze --json               # Find compaction candidates
bd restore <id>                                 # Recover deleted issue from git history
```

**Cleanup never loses data** — git history preserves everything. Start cleaning at ~200 issues, never exceed ~500.

---

## Dependency Cycles

If `bd dep cycles` reports circular dependencies:

1. Review each cycle to identify the misclassified dependency
2. Remove the incorrect link: `bd dep remove <child> <parent>`
3. Consider if the tasks should be merged or if an intermediate task is missing
4. Re-run `bd dep cycles` to verify resolution
