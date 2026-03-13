# Step 0 — PRD Intake & Normalization

<!-- beads-id: br-gatecheck-g0 -->

> **Pipeline position:** Step 0 of 12 • No prerequisites • Leads to → Step 1 (Contract Generation)

## Input

- PRD from Product Owner (markdown/doc)
- UX goals, personas, primary flows, acceptance criteria

## Processing

### 0.1 Parse PRD Sections

Extract structured data from the PRD into these categories:

1. **Universal ID** — the explicit `beads-id` from HTML comments (e.g., `<!-- beads-id: br-prd04-s2 -->`)
2. **Screens** — all routes/screens mentioned
3. **User Journeys** — step-by-step flows linked to screens
4. **State Matrix** — loading / empty / error / success / offline states per screen
5. **Breakpoints** — responsive viewport definitions (mobile, tablet, desktop)
6. **Accessibility Requirements** — WCAG level, focus order, contrast targets

### 0.2 Validate Completeness (Schema Check)

Run a checklist validation against the PRD:

| Field               | Required?   | Check                                     |
| ------------------- | ----------- | ----------------------------------------- |
| Routes/screens      | ✅          | At least 1 defined route                  |
| State matrix        | ✅          | All screens have ≥ default + error states |
| Acceptance criteria | ✅          | Measurable (not vague "should look good") |
| Personas            | ⚠️ Optional | Helpful for a11y prioritization           |
| Breakpoints         | ✅          | At least mobile + desktop                 |

### 0.3 Gap Detection & PRD Completeness Ralph Loop

If any **required** field is missing, generate a `PRD_GAP_LIST`:

```markdown
## PRD Gap List — feature-x

- [ ] Missing state matrix for `/settings` screen
- [ ] No acceptance criteria for error states
- [ ] Breakpoints not defined (defaulting to standard 3-viewport set)
```

**PRD Completeness Ralph Loop:**
If `PRD_GAP_LIST` is generated, before proceeding further, dispatch a PRD Writer Agent to iteratively resolve the gap list and amend the PRD. The loop runs (Evaluator flags missing info -> Writer amends PRD) until the Evaluator yields a completely empty `PRD_GAP_LIST`. No silent assumptions or LLM inventions are allowed; data must be resolved in the PRD artifact first.

## Output

| Artifact          | Path                                  |
| ----------------- | ------------------------------------- |
| Normalized PRD    | `docs/PRDs/feature-x.normalized.json` |
| Gap list (if any) | `docs/PRDs/feature-x.gap-list.md`     |

## Switching Rules

- **If PRD has critical gaps** → Trigger **PRD Completeness Ralph Loop**. Do not proceed to Step 1 until the loop successfully empties the gap list. If the PRD is irresolute / requires human logic: halt pipeline at `NEEDS_PRD_CLARIFICATION`.
- **If PRD is complete** → Proceed to Step 1: Contract Generation.

## Next Step

→ [g1-contract-generation.md](./g1-contract-generation.md)
