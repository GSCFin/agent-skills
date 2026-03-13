---
description: Ralph Loop Stage 2 — Hi-Fi Implementation through Gate B. Orchestrates BUILD↔AUDIT loop, Agile Refine, and Final Human Approval.
---

# Ralph Loop Stage 2: Contract → Hi-Fi Implementation → Gate B

<!-- beads-id: br-workflow-ralph-loop-stage2 -->

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 3-LAYER AGENT COMPREHENSION PYRAMID                        │
│                                                                             │
│                    /\        LAYER 1: ROOT METHODOLOGY                     │
│                   /  \       spike-design-system-ralph-loop-agent.md        │
│                  /    \      "WHY & WHAT" — Theory, DoD, RFT, 3-Tier Eval  │
│                 /──────\                                                    │
│                /        \    LAYER 2: ORCHESTRATION                         │
│               /          \   gsafe-uiux-ralph-loop-antigravity.md (main)    │
│              /            \                                                 │
│             /   Sub-wf:    \  ├── gsafe-uiux-ralph-loop-stage1.md          │
│            /   YOU ARE HERE \ └── gsafe-uiux-ralph-loop-stage2.md ◄── HERE │
│           /──────────────────\                                              │
│          /                    \  LAYER 3: EXECUTOR SKILLS                  │
│         / Gatecheck (Evaluator) \ design-system-gatecheck/                 │
│        / Implementor (Builder)   \ agenticse-design-system/                │
│       /──────────────────────────\ "HOW" — Rules, Steps, Standards         │
│                                                                             │
│  >> AGENT DIRECTIVE:                                                       │
│  >> You are at LAYER 2 (sub-workflow). This file orchestrates Stage 2.     │
│  >> For BUILD steps: read agenticse-design-system skill rules.             │
│  >> For AUDIT steps: read design-system-gatecheck skill rules.             │
│  >> Each step below tells you EXACTLY which rule file to read.             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **SAFe 6.0 Phase:** Continuous Integration — Iterate & Learn
> **Skills Used:** `agenticse-design-system` (Implementor) + `design-system-gatecheck` (Evaluator)
> **Outcome:** Human-approved Hi-Fi UI, merge-ready

## Preconditions

- [ ] Gate A approved (Stage 1 complete)
- [ ] The following immutable contract artifacts exist:
  - `docs/design/contracts/feature-x.contract.yaml`
  - `docs/design/contracts/feature-x.ascii.md`
  - `docs/design/contracts/feature-x.storyboards.json`
  - `docs/design/contracts/feature-x.layout-rules.json`
  - `docs/design/contracts/feature-x.component-map.json`
  - `docs/design/test-plans/feature-x.assertion-checklist.md`
  - `docs/design/test-plans/feature-x.coverage-matrix.csv`

## Architecture Overview

```text
┌═══════════════════════════════════════════════════════════════════════════════┐
║                        RALPH LOOP STAGE 2 (Hi-Fi)                           ║
║                                                                              ║
║  ┌─ W0 PLAN DECLARATION GATE ──────────────────────────────────────────┐    ║
║  │ Implementor emits plan-declaration.json                             │    ║
║  │ Evaluator validates: all data-ds-id in build_sequence?              │    ║
║  │ PLAN_REJECTED → revise plan BEFORE any code                        │    ║
║  └──────────────────────────────────────┬──────────────────────────────┘    ║
║                                         │ PLAN_APPROVED                      ║
║                                         v                                    ║
║  ┌─ Sub-Task 2A: BUILD ─────────────────────────────────────────────┐      ║
║  │ Implementor (agenticse-design-system): W1→W2                     │      ║
║  │ Read layout-rules.json → Write HTML/CSS/Tokens                   │      ║
║  │ Self-Verification: CSS lint → Playwright preview → log           │      ║
║  └──────────────────────────────────────┬───────────────────────────┘      ║
║                                         v                                    ║
║  ┌─ Sub-Task 2B: AUDIT ─────────────────────────────────────────────┐      ║
║  │ Evaluator (design-system-gatecheck): g3→g8                       │      ║
║  │ g3: Env setup → g4: DOM Conformance → g5: Visual Diff            │      ║
║  │ g6: Flow Nav → g7: A11y → g8: Scoring (100-pt DoD)               │      ║
║  └──────────────────────────────────────┬───────────────────────────┘      ║
║                                         v                                    ║
║  ┌─ ADAPTIVE CONVERGENCE DECISION ──────────────────────────────────┐      ║
║  │ Score ≥ 95 AND P0 == 0  → GATE_B_READY                           │      ║
║  │ Score improves ≥ 5 pts  → +1 retry (max 6)                       │      ║
║  │ Plateau ≤ 1 pt for 2×   → LOOP_STALLED → escalate               │      ║
║  │ score[N] < score[N-1]   → REGRESSION → restore N-1 snapshot      │      ║
║  │ wall_clock > 30min      → LOOP_TIMEOUT → escalate                │      ║
║  └─────────────┬────────────────────────────────────┬───────────────┘      ║
║     CONTINUE   │                                    │ GATE_B_READY          ║
║     (Fix Queue)│                                    v                        ║
║         ▲      │                          ┌──────────────────┐              ║
║         └──────┘                          │ Task 3: Agile    │              ║
║                                           │ Refine (PRD Sync)│              ║
║                                           └────────┬─────────┘              ║
║                                                    v                         ║
║                                           ┌──────────────────┐              ║
║                                           │ 🚧 GATE B        │              ║
║                                           │ Human Scorecard   │              ║
║                                           └────────┬─────────┘              ║
╚════════════════════════════════════════════════════╪══════════════════════════╝
                                                     │ APPROVE
                                                     v
                                               ✅ MERGE & DEPLOY
```

---

## Step-by-Step Execution

### W0: Plan Declaration Gate

**Skill rule:** Read `skills/agenticse-design-system/rules/w1-discover-plan.md` (Section W0)

**`task_boundary` call:**
```
TaskName: "Stage 2 — W0 Plan Declaration"
Mode: EXECUTION
```

**Actions:**

1. Implementor emits `docs/design/plan-declaration.json`:
   ```json
   {
     "rollout_id": "rl-YYYY-MM-DD-NNN",
     "prd_beads_id": "br-xxx",
     "contract_version": "feature-x.contract.yaml",
     "build_sequence": [
       { "step": 1, "component": "ds:comp:top-nav-001", "type": "structural" },
       { "step": 2, "component": "ds:comp:kpi-cards-001", "type": "data-display" }
     ],
     "states_to_implement": ["default", "loading", "empty", "error"],
     "risks": ["..."],
     "tool_budget_estimate": 6
   }
   ```

2. Evaluator validates: every `data-ds-id` in the contract's `components.required[]` MUST appear in `build_sequence`

3. **If `PLAN_REJECTED`** → Implementor revises plan. No HTML/CSS is written until plan is approved.

**Exit condition:** Plan validated. Proceed to BUILD.

---

### Sub-Task 2A: BUILD (Implementor)

**Skill rules:**
- Read `skills/agenticse-design-system/rules/w1-discover-plan.md`
- Read `skills/agenticse-design-system/rules/w2-create-build.md`

**`task_boundary` call:**
```
TaskName: "Stage 2 — BUILD: Implementing UI"
Mode: EXECUTION
```

**Actions:**

1. **W1 (Discover & Plan):** Read `layout-rules.json` as immutable contract input. Read `PRD_DS_CONFLICT` resolution log. Plan build sequence per `plan-declaration.json`.

2. **W2 (Create & Build):** Write HTML/CSS/Tokens strictly following the DS token system. Every component gets a `data-ds-id` attribute. Code against exact component map from contract.

3. **Self-Verification** (earns +5 bonus pts in DoD):
   - CSS lint run
   - Rendered page opened in Playwright preview
   - Pre-submission checklist logged

**Exit condition:** UI built and self-verified. Proceed to AUDIT.

---

### Sub-Task 2B: AUDIT (Evaluator)

**Skill rules:** Read the following gatecheck rules:
- `skills/design-system-gatecheck/rules/g3-env-deterministic.md`
- `skills/design-system-gatecheck/rules/g4-conformance-test.md`
- `skills/design-system-gatecheck/rules/g5-visual-diff.md`
- `skills/design-system-gatecheck/rules/g6-flow-navigation.md`
- `skills/design-system-gatecheck/rules/g7-a11y-contrast.md`
- `skills/design-system-gatecheck/rules/g8-scoring-policy.md`

**`task_boundary` call:**
```
TaskName: "Stage 2 — AUDIT: Evaluating UI"
Mode: VERIFICATION
```

**Actions:**

| Step | Rule | Description | Gate Enforcement |
|------|------|-------------|------------------|
| g3 | `g3-env-deterministic` | Lock browser, fonts, mock data, disable animations | — |
| g4 | `g4-conformance-test` | Tier 1: DOM Conformance — component existence, hierarchy, overlap | FAIL_P0 → SKIP g5-g7 |
| g5 | `g5-visual-diff` | Tier 2: Screenshot comparison across viewport×theme×state matrix | FAIL_P0 → SKIP g6 |
| g6 | `g6-flow-navigation` | Tier 2: Storyboard trajectory execution, dead-end detection | — |
| g7 | `g7-a11y-contrast` | Tier 1: axe-core/pa11y WCAG AA audit | SKIPPED_TOOL_ERROR if axe fails |
| g8 | `g8-scoring-policy` | 100-pt DoD scoring engine — 6 pillars + anti-hacking + safety | Emits scorecard v1.1 |

**Scorecard output includes:**
- `total_score` (0-100), `p0_violations`, gradient penalty
- Prioritized `p0_fixes → p1_fixes → p2_fixes` queue
- `pillar_deltas` per iteration, `rollout_id`, `reasoning_trace_score`
- `component_attribution` (implementor | evaluator_env | unknown)
- `autonomy_score`, `wall_clock_ms`, `total_tokens`
- Graceful degradation: `TOOL_FAILURE` events logged (not crashed)

**Exit condition:** Scorecard emitted. Proceed to Convergence Decision.

---

### Adaptive Convergence Decision

| Condition | Action |
|-----------|--------|
| Score ≥ 95 AND P0 == 0 | → `GATE_B_READY` — proceed to Task 3 |
| Score improves ≥ 5 pts | → +1 retry allowed (max cap: 6) |
| Score plateau ≤ 1 pt for 2 consecutive | → `LOOP_STALLED` → escalate to Gate B |
| score[N] < score[N-1] | → `REGRESSION_DETECTED` → restore N-1 snapshot, send regression delta to Implementor |
| wall_clock > 30min (std) / 60min (complex) | → `LOOP_TIMEOUT` → freeze best snapshot, escalate to Gate B |

**On CONTINUE:** Send Prioritized Fix Queue back to Sub-Task 2A (BUILD). Implementor reads `skills/agenticse-design-system/rules/w3-refine-align.md` for fix application.

**On GATE_B_READY / STALL / TIMEOUT:** Proceed to Task 3.

---

### Task 3: Agile Refine (PRD-DS Sync)

**`task_boundary` call:**
```
TaskName: "Stage 2 — Task 3: Agile Refine"
Mode: VERIFICATION
```

**Actions:**

1. Compare final UI code against original PRD
2. Generate **PRD Journey Coverage Matrix** (`prd-coverage-matrix.csv`):
   - For each user journey: storyboard exists? was executed? did it pass?
   - Any `NOT_COVERED` journey **blocks Gate B approval**
3. Generate `latest-ui-handover.md` with `text_output_match_score`
4. Generate missing states list and PRD refinement recommendations
5. Compute **Task Success Rate:** `TSR = converged_runs / total_runs`

**If missing UI states discovered** → route back to PRD Writer (Stage 1, Step 0).

**Exit condition:** Coverage matrix complete. Proceed to Gate B.

---

### 🚧 GATE B: Final Human Approval

**Skill rule:** Read `skills/design-system-gatecheck/rules/gate-b-result-approval.md`

**`task_boundary` call:**
```
TaskName: "Stage 2 — Gate B: Final Approval"
Mode: VERIFICATION
```

**Present to Human** via `notify_user` with `BlockedOnUser: true`:

**Structured Human Scorecard:**

| Criteria | Scale | Required Minimum |
|----------|-------|-------------------|
| Visual brand fit | 1–5 | ≥ 3 |
| Copy clarity | 1–5 | ≥ 3 |
| Interaction intuitiveness | 1–5 | ≥ 3.5 |
| Safety / edge case handling | 1–5 | ≥ 4 |
| Production readiness | 1–5 | ≥ 3.5 |

**Minimum average: 3.5/5 to approve.**

**Also disclosed:**
- Pillar delta convergence curves
- `TOOL_FAILURE` events
- `NOT_COVERED` PRD journeys
- Autonomy score

### Gate B Decision Routing

| Decision | Action | Route |
|----------|--------|-------|
| ✅ **APPROVE** | UI passes all criteria | → Merge & Deploy |
| 🔄 **REQUEST_FIX** | Issues found | → Return to Sub-Task 2A (BUILD) within the Ralph Loop |
| ✅ **APPROVE_WITH_BASELINE_UPDATE** | UI approved, baselines need refresh | → Merge + run baseline governance (g9) |

**Output:** `docs/design/reports/feature-x-approval-log.md`

---

## Post-Approval: Stage 2 Complete

On **APPROVE**, the full Ralph Loop pipeline is complete:
- CI pipeline (`.github/workflows/ralph-loop-ci.yml`) runs on merge
- Scorecard artifact uploaded for audit trail
- RFT training data stored at `docs/rft-dataset/{prd_id}/`
- Baseline governance executed via `g9-baseline-governance.md`
