# Output Styles

> Source: https://code.claude.com/docs/en/output-styles

Adapt Claude Code output for uses beyond software engineering.

## Built-in Output Styles

- **Explanatory**: Provides educational "Insights" between helping you with tasks. Helps understand implementation choices and codebase patterns.
- **Learning**: Collaborative learn-by-doing mode. Claude shares "Insights" while coding and asks you to contribute small pieces of code yourself via `TODO(human)` markers.

## How Output Styles Work

- All output styles exclude instructions for efficient output (such as responding concisely)
- Custom output styles exclude coding instructions unless `keep-coding-instructions` is true
- All output styles add custom instructions to the end of the system prompt
- Reminders to adhere to the style are triggered during the conversation

## Change Your Output Style

Via `/config` or in `.claude/settings.local.json`:

```json
{
  "outputStyle": "Explanatory"
}
```

## Create a Custom Output Style

Place in `~/.claude/output-styles/` (user) or `.claude/output-styles/` (project):

```markdown
---
name: My Custom Style
description: A brief description of what this style does
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering tasks.

[Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

### Frontmatter

| Field | Description |
|-------|-------------|
| `name` | Display name |
| `description` | Shown in `/config` |
| `keep-coding-instructions` | If true, retains default coding instructions |

## Comparisons to Related Features

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Output styles change how Claude communicates. CLAUDE.md provides project context. `--append-system-prompt` adds custom system instructions.

### Output Styles vs. Agents

Agents are separate execution contexts with their own tools and permissions. Output styles only change communication style.

### Output Styles vs. Skills

Skills are invoked with `/skill-name` and provide specific workflows. Output styles apply globally to all interactions.
