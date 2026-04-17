# bv Troubleshooting

Common issues and debugging guidance for Beads Viewer (`bv`) robot mode.

---

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| TUI blocks agent session | Ran bare `bv` without robot flags | **Always** use `--robot-*` flags |
| Stale metrics in output | Results cached by `data_hash` | Check `data_hash` field; re-run after `.beads/beads.jsonl` changes |
| Missing cycle detection | Didn't run the right command | Use `bv --robot-insights`, check `.cycles` field |
| Wrong recommendations | Includes blocked items | Use `--recipe actionable` to filter to ready work |
| Phase 2 metrics show `timeout` | Graph too large (>500 nodes) | Metrics were approximated; check `status` field for each metric |
| Phase 2 metrics show `skipped` | Graph extremely large | Use `--robot-plan` instead of `--robot-insights` for speed |

---

## Understanding `status` Flags

Every robot JSON output includes a `status` object showing computation state:

```json
{
  "status": {
    "pagerank": "computed",     // ✅ Exact result
    "betweenness": "approx",   // ⚠️ Approximated (large graph)
    "hits": "timeout",         // ⚠️ Hit 500ms deadline
    "cycles": "skipped"        // ❌ Not computed
  }
}
```

- `computed` — Exact result, safe to rely on
- `approx` — Approximated due to graph size, directionally correct
- `timeout` — Hit the 500ms async deadline, retry or use simpler commands
- `skipped` — Not computed, use `--robot-plan` as fallback

---

## Large Graphs (>500 Nodes)

For projects with many issues:

1. **Prefer `--robot-plan` over `--robot-insights`** — plan is faster and doesn't need all 9 metrics
2. **Use scoping** — `bv --robot-insights --label backend` analyzes only a subgraph
3. **Check `status`** — always verify which metrics actually computed
4. **Results are cached** — repeat calls with the same `data_hash` return instantly

---

## TOON Format Issues

If TOON format fails or produces unexpected output:

```bash
# Fall back to JSON
bv --robot-triage --format json

# Check if tru binary is installed
which tru

# Set TOON binary path explicitly
export TOON_TRU_BIN=/path/to/tru
```

TOON requires the `tru` (toon_rust) binary. If unavailable, always fall back to JSON.

---

## Data Freshness

`bv` reads from `.beads/beads.jsonl`. If the data seems stale:

```bash
# Force bd to re-export
bd sync

# Verify the JSONL was updated
ls -la .beads/beads.jsonl

# Re-run bv (it will detect the new data_hash)
bv --robot-triage
```

---

## No `.beads/beads.jsonl` Found

If `bv` reports missing data:

```bash
# For bd (Go) users — manual export
bd export --no-memories -o .beads/beads.jsonl

# For br (Rust) users — writes by default
br sync --flush-only

# Verify
ls .beads/beads.jsonl
```
