# Installation Guide

Setup instructions for the Beads ecosystem (`bd` + `bv`).

---

## Beads CLI (`bd`)

### Homebrew (macOS/Linux)

```bash
brew tap steveyegge/beads && brew install beads
```

### Install Script

```bash
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
```

### Initialize in a Project

```bash
cd your-project
bd init                    # Interactive setup (creates .beads/ directory)
bd init --quiet            # Non-interactive (for agents — recommended)
bd init --stealth          # Local-only, no repo pollution
bd init --contributor      # OSS fork workflow
bd init --team             # Team member with commit access
```

The wizard creates `.beads/`, imports existing issues, installs git hooks, and starts the background daemon.

### Claude Code Integration

```bash
bd setup claude              # Install hooks globally
bd setup claude --project    # Install for this project only
```

Adds hooks that run `bd prime` on session start and pre-compact events.

---

## Beads Viewer (`bv`)

### Homebrew (macOS/Linux) — Recommended

```bash
brew install dicklesworthstone/tap/bv
```

Provides automatic updates via `brew upgrade`.

### Windows: Scoop

```powershell
scoop bucket add dicklesworthstone https://github.com/Dicklesworthstone/scoop-bucket
scoop install dicklesworthstone/bv
```

### Direct Download

Download the latest release for your platform:
- [Linux x86_64](https://github.com/Dicklesworthstone/beads_viewer/releases/latest)
- [Linux ARM64](https://github.com/Dicklesworthstone/beads_viewer/releases/latest)
- [macOS Intel](https://github.com/Dicklesworthstone/beads_viewer/releases/latest)
- [macOS ARM](https://github.com/Dicklesworthstone/beads_viewer/releases/latest)
- [Windows](https://github.com/Dicklesworthstone/beads_viewer/releases/latest)

### Install Script

**Linux/macOS:**
```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.sh?$(date +%s)" | bash
```

**Windows (PowerShell):**
```powershell
irm "https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.ps1" | iex
```

> **Note:** Windows requires Go 1.21+ ([download](https://go.dev/dl/)). For best display, use Windows Terminal with a [Nerd Font](https://www.nerdfonts.com/).

---

## Generating the JSONL File

`bv` reads from `.beads/beads.jsonl`. Both tools can generate it:

**Rust (`br`) users** — writes `.beads/beads.jsonl` by default. No extra steps.

**Go (`bd`) users** — run:
```bash
bd export --no-memories -o .beads/beads.jsonl
```

Once the file exists, `bv` works identically regardless of which tool produced it.

---

## Verification

```bash
# Verify bd
bd --version
bd ready --json

# Verify bv
bv --version
bv --robot-next

# Verify data pipeline
ls .beads/beads.jsonl
```
