# Extend Claude with Skills

> Source: https://code.claude.com/docs/en/skills

Create, manage, and share skills to extend Claude's capabilities in Claude Code.

## Bundled Skills

| Command | Description |
|---------|-------------|
| `/batch <instruction>` | Process files in parallel using git worktrees |
| `/claude-api` | Work with Anthropic API SDKs |
| `/debug [description]` | Debug issues |
| `/loop [interval] <prompt>` | Run prompts on a schedule |
| `/simplify [focus]` | Simplify code |

## Getting Started

### Create Your First Skill

```bash
mkdir -p ~/.claude/skills/explain-code
```

Create `~/.claude/skills/explain-code/SKILL.md`:

```markdown
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works.
---

When explaining code, always include:
1. **Start with an analogy**
2. **Draw a diagram** using ASCII art
3. **Walk through the code** step-by-step
4. **Highlight a gotcha**
```

Test with: `/explain-code src/auth/login.ts`

### Where Skills Live

| Location | Scope |
|----------|-------|
| `~/.claude/skills/<name>/SKILL.md` | User-level (personal) |
| `.claude/skills/<name>/SKILL.md` | Project-level (shared) |
| `<plugin>/skills/<name>/SKILL.md` | Plugin-level (namespaced) |

Skills in `.claude/commands/` also work (legacy location).

**Automatic discovery**: Claude Code discovers skills from nested directories like `packages/frontend/.claude/skills/`.

Skill directory structure:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output
└── scripts/
    └── validate.sh    # Script Claude can execute
```

## Configure Skills

### Types of Skill Content

- **Guidelines**: Always-active instructions (e.g., API conventions)
- **Workflows**: User-triggered commands with `disable-model-invocation: true`
- **Templates**: SKILL.md references supporting files

### Frontmatter Reference

```yaml
---
name: my-skill               # Display name
description: What this does   # Used for auto-triggering
argument-hint: [filename]     # Placeholder hint for arguments
disable-model-invocation: true  # Only user can invoke
user-invocable: false         # Only Claude can invoke
allowed-tools: Read, Grep     # Restrict available tools
model: sonnet                 # Use specific model
context: fork                 # Run in subagent context
agent: Explore                # Which agent runs it
hooks:                        # Lifecycle hooks
---
```

**String substitutions:**
- `$ARGUMENTS` — all user-provided arguments
- `$ARGUMENTS[N]` or `$N` — individual positional arguments
- `${CLAUDE_SESSION_ID}` — current session ID
- `${CLAUDE_SKILL_DIR}` — path to the SKILL.md directory

### Add Supporting Files

Reference additional files from SKILL.md:

```markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

### Control Who Invokes a Skill

- `disable-model-invocation: true` — Only the user can invoke (e.g., `/deploy`)
- `user-invocable: false` — Only Claude can invoke (background knowledge)

### Restrict Tool Access

```yaml
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### Pass Arguments to Skills

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
```

Usage: `/fix-issue 123`

Positional arguments:

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
```

Usage: `/migrate-component SearchBar React Vue`

## Advanced Patterns

### Inject Dynamic Context

Use `!` prefix to execute commands at skill load time:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`
```

### Run Skills in a Subagent

Use `context: fork` to run in an isolated subagent:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

### Restrict Claude's Skill Access

Use permission rules:

```
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

## Share Skills

- **Project**: Commit `.claude/skills/` to version control
- **Plugins**: Create `skills/` directory in your plugin
- **Managed**: Deploy organization-wide through managed settings

## Troubleshooting

- **Skill not triggering**: Check description keywords, verify with "What skills are available?"
- **Skill triggers too often**: Make description more specific, add `disable-model-invocation: true`
- **Claude doesn't see all skills**: Check `/context`, review `SLASH_COMMAND_TOOL_CHAR_BUDGET`
