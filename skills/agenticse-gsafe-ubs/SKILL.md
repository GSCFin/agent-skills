---
name: agenticse-gsafe-ubs
description: >-
  Use UBS (Ultimate Bug Scanner) as a quality gate for AI-generated code.
  Multi-language static analysis catching null safety, XSS, async bugs, memory
  leaks, and 13+ more categories across JS/TS, Python, Rust, Go, Java, C++, Ruby.
  Triggers: ubs, bug scanner, quality gate, static analysis, code scan.
license: MIT
risk: safe
source: self
metadata:
  author: agenticse
  version: "1.0.0"
---

# UBS: Ultimate Bug Scanner

UBS (`ubs`) is a multi-language static bug scanner built for AI coding agents. It catches 1000+ bug patterns across **JavaScript/TypeScript, Python, C/C++, Rust, Go, Java, Ruby, and Swift** in under 5 seconds.

**Mental model:** `ubs .` scans your project, reports findings by severity (🔥 Critical / ⚠️ Warning / ℹ️ Info), and exits non-zero on issues. Use it as a quality gate before every commit. The agent's job is: **scan → fix criticals → re-scan → commit**.

## When to Apply

- After implementing any feature or fix (pre-commit scan)
- In CI/CD pipelines as a quality gate
- When reviewing AI-generated code for common pitfalls
- After large refactors to catch regressions
- As a git pre-commit hook

---

## Quickstart

### Installation

```bash
# Homebrew (recommended)
brew install dicklesworthstone/tap/ubs

# Or via install script
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/master/install.sh?$(date +%s)" \
  | bash -s -- --easy-mode
```

### First Scan

```bash
# Scan current project
ubs .

# Machine-readable output
ubs . --format=json

# Token-optimized output for agents
ubs . --format=toon
```

---

## Critical Rules

**Always scope to changed files** — `ubs src/file.ts` (<1s) is vastly faster than `ubs .` (30s). Never full-scan for small edits.

**Use `--format=json` or `--format=toon`** in agent contexts. `stdout` = data, `stderr` = diagnostics, exit `0` = success.

**Fix all 🔥 Critical issues before commit.** Review ⚠️ Warnings and fix if trivial.

---

## Core Commands

### Basic Scanning

```bash
# Scan specific files (fastest)
ubs file.ts file2.py

# Scan staged changes only
ubs --staged

# Scan working tree changes vs HEAD
ubs --diff

# Language filter (3-5x faster)
ubs --only=js,python src/

# Scan whole project
ubs .
```

### Output Formats

```bash
ubs . --format=json     # Pure JSON (for parsing)
ubs . --format=jsonl    # Line-delimited (streaming)
ubs . --format=toon     # ~50% smaller than JSON (LLM-optimized)
ubs . --format=sarif    # SARIF (GitHub integration)
```

### Strictness Profiles

```bash
ubs --profile=strict    # Fail on warnings, enforce high standards
ubs --profile=loose     # Skip TODO/debug nits (prototyping mode)
```

### CI Mode

```bash
ubs . --fail-on-warning --ci    # Exit 1 on any warning
```

---

## The Fix-Verify Loop

This is the golden pattern for AI coding workflows:

```
1. Implement feature
2. Run: ubs <changed-files> --format=json
3. Critical issues? → Fix them
4. Re-run scan
5. Exit 0? → Commit
6. Exit >0? → Go to step 3
```

```bash
# Agent decision: scope to changed files
ubs $(git diff --name-only --cached) --format=json
```

---

## 18 Detection Categories

| Category               | Prevents                                 | Time Saved |
| ---------------------- | ---------------------------------------- | ---------- |
| **Null Safety**        | "Cannot read property of undefined"      | 2-4h       |
| **Security Holes**     | XSS, code injection, prototype pollution | 8-20h      |
| **Async/Await Bugs**   | Race conditions, unhandled rejections    | 4-8h       |
| **Memory Leaks**       | Event listeners, timers, detached DOM    | 6-12h      |
| **Type Coercion**      | `===` vs `==` issues                     | 1-3h       |
| **Resource Lifecycle** | Unclosed files, connections, contexts    | 3-6h       |
| + 12 more              | Division-by-zero, dead code, etc.        |            |

### Category Packs

```bash
# Focus on resource hygiene (Python/Go/Java)
ubs --category=resource-lifecycle .
```

---

## Suppression

When a finding is intentional:

```python
eval("print('safe')")  # ubs:ignore
```

### Skip Categories

```bash
# Skip TODO markers and debug statements
ubs . --skip=11,14
```

---

## Agent Integration Patterns

### Git Pre-Commit Hook

```bash
#!/bin/bash
if ! ubs . --fail-on-warning 2>&1 | tail -30; then
  echo "❌ Critical issues found. Fix or: git commit --no-verify"
  exit 1
fi
```

### Comparison & Regression Detection

```bash
# Capture baseline
ubs --ci --report-json .ubs/baseline.json .

# Compare against baseline
ubs --ci --comparison .ubs/baseline.json --report-json .ubs/latest.json .
```

### AGENTS.md Blurb

```markdown
## Quality Gate

Before marking any task complete:

1. Run `ubs <changed-files>` (scope to files, not full project)
2. Fix ALL 🔥 Critical issues
3. Review ⚠️ Warnings, fix if trivial
4. Re-run until exit 0
5. Only then commit
```

---

## Bug Severity Guide

| Level           | Always Fix      | Examples                                                |
| --------------- | --------------- | ------------------------------------------------------- |
| **Critical** 🔥 | Yes             | Null safety, XSS/injection, missing await, memory leaks |
| **Warning** ⚠️  | Production code | Type narrowing, division-by-zero, resource leaks        |
| **Info** ℹ️     | Judgment call   | TODO/FIXME, console.log, code quality                   |

**Anti-patterns:**

- ❌ Ignore findings → ✅ Investigate each one
- ❌ Full scan per edit → ✅ Scope to changed files
- ❌ Fix symptom (`if (x) { x.y }`) → ✅ Root cause (`x?.y`)

---

## Performance

```
Small project (5K lines):     0.8s  ⚡
Medium project (50K lines):   3.2s  🚀
Large project (200K lines):  12s    💨
Huge project (1M lines):     58s    🏃
```

UBS auto-ignores `node_modules`, virtualenvs, `dist/build/target/vendor`, and editor caches.

---

## Honest Gaps

- Pattern-based scanner, not a type checker — some findings are heuristic
- `# ubs:ignore` suppression is per-line only
- Taint analysis is lightweight (traces source → sink, not full dataflow)
- React Hooks analysis requires the JS/TS scanner module
- Swift scanning requires Python3 for the guard helper
