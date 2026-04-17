# bv Robot Reference

Full command reference for Beads Viewer (`bv`) robot mode. For thinking guidance and best practices, see the main [SKILL.md](../SKILL.md).

> ⚠️ **CRITICAL: Never run bare `bv`** — it launches an interactive TUI that blocks your session. Always use `--robot-*` flags.

---

## The 9 Graph Metrics

`bv` computes these metrics to surface hidden project dynamics:

| Metric | What It Measures | Key Insight |
|--------|------------------|-------------|
| **PageRank** | Recursive dependency importance | Foundational blockers |
| **Betweenness** | Shortest-path traffic | Bottlenecks & bridges |
| **HITS** | Hub/Authority duality | Epics vs. utilities |
| **Critical Path** | Longest dependency chain | Keystones with zero slack |
| **Eigenvector** | Influence via neighbors | Strategic dependencies |
| **Degree** | Direct connection counts | Immediate blockers/blocked |
| **Density** | Edge-to-node ratio | Project coupling health |
| **Cycles** | Circular dependencies | Structural errors (must fix!) |
| **Topo Sort** | Valid execution order | Work queue foundation |

---

## Two-Phase Analysis

- **Phase 1 (instant):** degree, topo sort, density — always available
- **Phase 2 (async, 500ms timeout):** PageRank, betweenness, HITS, eigenvector, cycles

Always check the `status` field in output. For large graphs (>500 nodes), some metrics may be `approx` or `skipped`.

---

## Robot Commands

### Triage & Planning

```bash
bv --robot-triage              # Full triage: recommendations, quick_wins, blockers_to_clear
bv --robot-next                # Single top pick with claim command
bv --robot-plan                # Parallel execution tracks with unblocks lists
bv --robot-priority            # Priority misalignment detection
```

### Graph Analysis

```bash
bv --robot-insights            # Full metrics: PageRank, betweenness, HITS, cycles, etc.
bv --robot-label-health        # Per-label health: healthy|warning|critical
bv --robot-label-flow          # Cross-label dependency flow matrix
bv --robot-label-attention     # Attention-ranked labels
```

### History & Changes

```bash
bv --robot-history             # Bead-to-commit correlations
bv --robot-diff --diff-since <ref>  # Changes since ref
```

### Sprint & Forecasting

```bash
bv --robot-burndown <sprint>   # Sprint burndown, scope changes
bv --robot-forecast <id|all>   # ETA predictions
bv --robot-capacity            # Capacity projection
```

### Hygiene & Alerts

```bash
bv --robot-alerts              # Stale issues, blocking cascades, priority mismatches
bv --robot-suggest             # Duplicates, missing deps, label suggestions, cycle breaks
```

### Graph Export

```bash
bv --robot-graph                              # JSON (default)
bv --robot-graph --graph-format=dot           # Graphviz DOT
bv --robot-graph --graph-format=mermaid       # Mermaid diagram
bv --robot-graph --graph-root=bd-123 --graph-depth=3  # Focused subgraph
bv --export-graph report.html                 # Interactive HTML visualization
```

### Search

```bash
bv --search "login oauth" --search-mode hybrid --robot-search
```

---

## Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank
bv --robot-triage --robot-triage-by-track    # Group by parallel work streams
bv --robot-triage --robot-triage-by-label    # Group by domain
```

### Built-in Recipes

| Recipe | Purpose |
|--------|---------|
| `default` | All open issues sorted by priority |
| `actionable` | Ready to work (no blockers) |
| `high-impact` | Top PageRank scores |
| `blocked` | Waiting on dependencies |
| `stale` | Open but untouched for 30+ days |
| `triage` | Sorted by computed triage score |
| `quick-wins` | Easy P2/P3 items with no blockers |
| `bottlenecks` | High betweenness nodes |

---

## Output Structure

All robot JSON includes:
- `data_hash` — Fingerprint of beads.jsonl (verify consistency across calls)
- `status` — Per-metric state: `computed|approx|timeout|skipped` + elapsed ms
- `as_of` / `as_of_commit` — Present when using `--as-of`

### `--robot-triage` Output

```json
{
  "quick_ref": { "open_count": 95, "actionable_count": 49, "blocked_count": 47, "top_picks": [...] },
  "recommendations": [
    { "id": "bd-123", "score": 0.85, "reason": "Unblocks 5 tasks", "unblock_info": {...} }
  ],
  "quick_wins": [...],
  "blockers_to_clear": [...],
  "project_health": { "distributions": {...}, "graph_metrics": {...} },
  "commands": { "claim": "bd claim bd-123", "view": "bv --bead bd-123" }
}
```

### `--robot-insights` Output

```json
{
  "bottlenecks": [{ "id": "bd-123", "value": 0.45 }],
  "keystones": [{ "id": "bd-456", "value": 12.0 }],
  "influencers": [...],
  "hubs": [...],
  "authorities": [...],
  "cycles": [["bd-A", "bd-B", "bd-A"]],
  "clusterDensity": 0.045,
  "status": { "pagerank": "computed", "betweenness": "computed" }
}
```

---

## TOON Format (Token Optimization)

TOON reduces robot output tokens by ~50%:

```bash
bv --robot-triage --format toon
bv --robot-insights --format toon

# Set globally
export BV_OUTPUT_FORMAT=toon
```

---

## jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.status'                         # Check metric readiness
bv --robot-insights | jq '.cycles'                         # Circular deps (must fix!)
bv --robot-label-health | jq '.results.labels[] | select(.health_level == "critical")'
```

---

## Agent Workflow Pattern

```bash
# 1. Start with triage
TRIAGE=$(bv --robot-triage)
NEXT_TASK=$(echo "$TRIAGE" | jq -r '.recommendations[0].id')

# 2. Check for cycles first (structural errors)
CYCLES=$(bv --robot-insights | jq '.cycles')
if [ "$CYCLES" != "[]" ]; then
  echo "Fix cycles first: $CYCLES"
fi

# 3. Claim the task
bd update "$NEXT_TASK" --claim --json

# 4. Work on it...

# 5. Close when done
bd close "$NEXT_TASK" --reason "Completed" --json
bd sync
```

---

## Time Travel

Compare against historical states:

```bash
bv --as-of HEAD~10                    # 10 commits ago
bv --as-of v1.0.0                     # At tag
bv --as-of "2024-01-15"               # At date
bv --robot-diff --diff-since HEAD~30  # Changes in last 30 commits
```
