---
name: agile-dev-brownfield
description: "Directive for generating a Claude Code Agile Agent Team prompt for brownfield (existing codebase) software development. Produces a single ready-to-paste prompt. Team: SM, ARCH, QA1, Dev1, Dev2, Dev3, QA2."
---

# Agile Agent Team — Brownfield Development Directive

## When This Directive Applies

Use this directive when the user asks to implement a feature, fix bugs, or execute a task board on **an existing codebase** using an agent team.

---

## Step 1 — Read the Project Before Writing Anything

You MUST read these files before generating the prompt. Do not skip or assume:

1. **`GEMINI.md`** (or `CLAUDE.md` if it exists) — project rules, conventions, ground-truth hierarchy, documentation standards
2. **`README.md`** — system overview, directory layout, CLI reference
3. **`docs/`** — the primary ground truth. Read relevant subdirectories:
   - `docs/architecture/` — system design contracts
   - `docs/workflows/` — pipeline flows
   - `docs/planning/` — task boards, roadmaps
   - `docs/spikes/` — research (may lag implementation — verify against source)
4. **The task source document** the user pointed to (roadmap, issue list, spike)
5. **Key source files** relevant to the tasks (read at least the entry points)

> **Rule:** Every agent in the generated prompt must also be instructed to read `GEMINI.md` / `CLAUDE.md` and the relevant `docs/` files as their first action. No agent may touch code without first reading the ground truth.

---

## Step 2 — Extract Task Breakdown

From the task source document, extract:
- Task list with IDs (T1, T2, …)
- Dependency graph
- Definition of Done per task
- Which source files each task touches

Assign tasks to Dev1 / Dev2 / Dev3 such that:
- No two Devs own the same file at the same time
- Dependencies are respected (blocked Dev waits, does not start early)
- Each Dev has a balanced workload

---

## Step 3 — Self-Check Before Generating the Prompt

Before writing the output prompt, answer these questions internally. If any answer is NO, fix it first:

| # | Check | Must be YES |
|---|---|---|
| 1 | Does every teammate prompt start with "Read GEMINI.md and docs/ first"? | YES |
| 2 | Is the ground-truth hierarchy from GEMINI.md respected in every teammate prompt? | YES |
| 3 | Does SM auto-approve QA1's test plan without human input? | YES |
| 4 | Does SM re-spawn (not message) QA2 and the failing Dev for each bug-fix cycle? | YES |
| 5 | Are there zero file ownership conflicts between Dev1/Dev2/Dev3? | YES |
| 6 | Does every teammate have a clear "message SM when done" instruction? | YES |
| 7 | Is the entire output a single copyable prompt block (no split sections)? | YES |
| 8 | Does the prompt specify the model (`gpt-5.4` or as instructed by user)? | YES |
| 9 | Does ARCH output to a file (not just a message) that all Devs can read? | YES |
| 10 | Does QA2's re-spawn prompt include the exact list of failing test cases? | YES |

---

## Step 4 — Team Roles and Invariants

### SM — Scrum Master (orchestrator, never writes code)
- Reads GEMINI.md + task source before spawning anyone
- Spawns all 6 teammates inline in one go
- Assigns tasks to Devs per dependency graph
- When QA1 posts test plan: **immediately replies "Test plan APPROVED ✅"** and broadcasts "Devs: begin implementation"
- Runs bug-fix loop:
  ```
  LOOP until QA2 reports zero failures:
    receive QA2 report
    identify failing task owner (Dev1/Dev2/Dev3)
    re-spawn that Dev: "Fix bug: [exact failure]. Re-run your tests."
    after Dev confirms fix: re-spawn QA2: "Re-run these cases: [list]."
  mark task DONE on sprint board
  ```

### ARCH — Software Architect (reads, plans, reviews — never writes production code)
- First action: read GEMINI.md, README.md, docs/architecture/, relevant source files
- Produces `docs/planning/architecture-decisions.md` with:
  - Integration points for each task
  - File ownership map (who touches what)
  - Any risk or design constraint Devs must respect
- Reviews each Dev's work against that document before SM marks DONE
- Messages SM: "ARCH done. architecture-decisions.md ready."

### QA1 — Architecture & Planning QA (writes test plan, no implementation)
- Waits for ARCH to post `architecture-decisions.md`
- Reads GEMINI.md + ARCH output + task DoD
- Writes `docs/planning/test-plan.md` with:
  - One test case per DoD criterion
  - Exact commands / assertions (pytest, CLI, manual checks)
  - Pass/Fail criteria
- Messages SM: "QA1 done. test-plan.md ready for approval."
- Does NOT run tests — that is QA2's role

### Dev1 / Dev2 / Dev3 (implement, test their own unit, fix bugs)
- First action: read GEMINI.md + README.md + relevant docs/ + architecture-decisions.md
- Wait for SM to assign tasks AND for ARCH to post architecture-decisions.md
- Follow project conventions from GEMINI.md (PEP 8, type hints, etc.)
- Write unit tests for their own code
- Message SM: "DevN done [task IDs]. Ready for QA2."
- When re-spawned by SM for bug fix: read the exact QA2 failure, fix only that, re-run own unit tests, message SM

### QA2 — Test Execution (runs test plan, reports, re-spawned each cycle)
- Each spawn: given explicit list of test cases to run (from QA1's test-plan.md)
- Runs exact commands from test plan
- Writes `docs/planning/qa-report.md`: PASS/FAIL per case, repro steps for fails
- Never fixes code — only reports
- Messages SM: "QA2 done. [N passed / M failed]. See qa-report.md."
- On re-spawn: given only the previously failing cases; re-runs only those; reports delta

---

## Step 5 — Output Format

Your output is **one single fenced code block** containing the complete prompt.
The user copies it and pastes directly into Claude Code.

No explanation before or after the block is needed — the block is the deliverable.

```
Create an agent team with 7 teammates using model [MODEL] to implement [TASK DESCRIPTION].

Prerequisites:
- CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 must be set
- model: [MODEL] (set in .claude/settings.json or --model flag)

Read before spawning — ground truth for this project:
- GEMINI.md (or CLAUDE.md) — project rules and conventions
- README.md — system overview
- docs/ — authoritative documentation
- [task source document path] — task breakdown, DoD

Dependency order for tasks: [T1 → T2 → T3, T4 independent, etc.]

Spawn the following 7 teammates:

TEAMMATE SM — Scrum Master:
You are the Scrum Master. Read GEMINI.md and [task source] first.
Spawn these 6 teammates immediately with the prompts below.
Assign tasks per this dependency graph: [graph].
When QA1 posts test-plan.md, reply "Test plan APPROVED ✅" immediately
and broadcast to Dev1/Dev2/Dev3: "Test plan approved. Begin implementation."
Run the bug-fix loop: wait for QA2 report → re-spawn failing Dev with exact failure →
re-spawn QA2 with failing case list → repeat until zero failures → mark DONE.
Never write code yourself.

TEAMMATE ARCH — Software Architect:
Read GEMINI.md, README.md, docs/architecture/, and these source files: [list].
Produce docs/planning/architecture-decisions.md covering: [integration points, file ownership map, design constraints].
Do not write production code. Message SM when done: "ARCH done."

TEAMMATE QA1 — Planning QA:
Wait for ARCH to post architecture-decisions.md. Read GEMINI.md + ARCH output + DoD from [task source].
Write docs/planning/test-plan.md: one test case per DoD criterion with exact commands and pass/fail criteria.
Do not run tests. Message SM: "QA1 done. test-plan.md ready."

TEAMMATE Dev1:
Read GEMINI.md, README.md, docs/, architecture-decisions.md first.
Wait for SM task assignment. Own tasks: [T-list]. Files you own: [file list].
Follow all conventions in GEMINI.md. Write unit tests for your code.
Message SM when done: "Dev1 done [tasks]."
When re-spawned for a bug fix, read the exact QA2 failure, fix only that, re-run your unit tests, message SM.

TEAMMATE Dev2:
[Same structure as Dev1 with different tasks and files]

TEAMMATE Dev3:
[Same structure as Dev1 with different tasks and files]

TEAMMATE QA2 — Test Execution:
Run these test cases from docs/planning/test-plan.md: [full list on first spawn / failing cases only on re-spawn].
Write docs/planning/qa-report.md: PASS/FAIL per case, repro steps for failures.
Never fix code. Message SM: "QA2 done. [N passed / M failed]. See qa-report.md."
```
