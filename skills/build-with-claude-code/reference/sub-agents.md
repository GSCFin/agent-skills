# Create Custom Subagents

> Source: https://code.claude.com/docs/en/sub-agents

Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

**Key benefits:**
- Preserve context by keeping exploration and implementation out of your main conversation
- Enforce constraints by limiting which tools a subagent can use
- Reuse configurations across projects with user-level subagents
- Specialize behavior with focused system prompts for specific domains
- Control costs by routing tasks to faster, cheaper models like Haiku

## Built-in Subagents

| Subagent | Model | Tools | Purpose |
|----------|-------|-------|---------|
| **Explore** | Haiku (fast, low-latency) | Read-only tools | File discovery, code search, codebase exploration |
| **Plan** | Inherits from main | Read-only tools | Codebase research for planning |
| **General-purpose** | Inherits from main | All tools | Complex research, multi-step operations, code modifications |

Use `/statusline` to see active subagents.

## Quickstart: Create Your First Subagent

1. Open the subagents interface with `/agents`
2. Create a new user-level agent at `~/.claude/agents/`
3. Generate with Claude by describing what you want
4. Select tools, model, and color
5. Save and try it out

You can also [create them manually](#write-subagent-files).

## Configure Subagents

### Use the /agents Command

The `/agents` command lets you:
- View all available subagents (built-in, user, project, and plugin)
- Create new subagents with guided setup or Claude generation
- Edit existing subagent configuration and tool access
- Delete custom subagents
- See which subagents are active when duplicates exist

CLI equivalent: `claude agents`

### Choose the Subagent Scope

Subagents can be defined at three levels:
- **Project-level**: `.claude/agents/` — shared with team via version control
- **User-level**: `~/.claude/agents/` — personal, available across all projects
- **Plugin-level**: `agents/` inside a plugin
- **CLI flag**: `--agents` for inline JSON definitions

```bash
claude --agents '{ "code-reviewer": { "description": "Expert code reviewer...", "prompt": "You are a senior code reviewer...", "tools": ["Read", "Grep", "Glob", "Bash"], "model": "sonnet" } }'
```

### Write Subagent Files

Subagent files use YAML frontmatter + markdown body:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

#### Supported Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Display name (falls back to filename) |
| `description` | Used by Claude to decide when to delegate |
| `tools` | Comma-separated list of allowed tools |
| `disallowedTools` | Tools to explicitly deny |
| `model` | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` (default) |
| `permissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Maximum conversation turns |
| `skills` | Skills to preload |
| `mcpServers` | MCP servers to scope to this subagent |
| `hooks` | Lifecycle hooks |
| `memory` | Persistent memory scope: `user`, `project`, or `local` |
| `background` | `true` to run as background task |
| `isolation` | `worktree` for git worktree isolation |

### Choose a Model

Options for the `model` field:
- **Model alias**: `sonnet`, `opus`, or `haiku`
- **Full model ID**: e.g., `claude-opus-4-6` or `claude-sonnet-4-6`
- **`inherit`**: Use the same model as the main conversation (default)

### Control Subagent Capabilities

#### Available Tools

Use `tools` to whitelist and `disallowedTools` to blacklist:

```yaml
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---
```

#### Restrict Which Subagents Can Be Spawned

Use `Agent(agent_type)` in the tools list:

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

#### Scope MCP Servers to a Subagent

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github
---
```

#### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Normal permission prompting |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Skip all permission prompts |
| `bypassPermissions` | Full bypass (use with caution) |
| `plan` | Read-only mode |

#### Preload Skills into Subagents

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
```

#### Enable Persistent Memory

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---
```

Memory scopes:
- `user`: `~/.claude/agent-memory/<name-of-agent>/`
- `project`: `.claude/agent-memory/<name-of-agent>/`
- `local`: `.claude/agent-memory-local/<name-of-agent>/`

The subagent's system prompt includes instructions for managing `MEMORY.md`.

#### Conditional Rules with Hooks

```yaml
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

#### Disable Specific Subagents

Use `permissions.deny` in settings:

```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Or via CLI: `claude --disallowedTools "Agent(Explore)"`

### Define Hooks for Subagents

Two places to define hooks:
1. **In subagent frontmatter**: runs only while that subagent is active
2. **In settings.json**: runs in the main session for `SubagentStart`/`SubagentStop` events

#### Hooks in Subagent Frontmatter

Supported events: `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`

```yaml
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

#### Project-Level Hooks for Subagent Events

```json
{
  "hooks": {
    "SubagentStart": [{
      "matcher": "db-agent",
      "hooks": [{
        "type": "command",
        "command": "./scripts/setup-db-connection.sh"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "./scripts/cleanup-db-connection.sh"
      }]
    }]
  }
}
```

## Work with Subagents

### Understand Automatic Delegation

Claude uses the `description` field to decide when to delegate. You can also explicitly request:

```
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

### Run Subagents in Foreground or Background

- **Foreground**: blocks main conversation; permission prompts pass through to you
- **Background**: runs concurrently; pre-approves permissions at launch; clarifying questions fail silently

To run in background:
- Ask Claude to "run this in the background"
- Press `Ctrl+B` to background a running task
- Disable with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`

### Common Patterns

- **Isolate high-volume operations**: "Use a subagent to run the test suite and report only failing tests"
- **Run parallel research**: "Research the auth, database, and API modules in parallel using separate subagents"
- **Chain subagents**: "Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them"

### Choose Between Subagents and Main Conversation

**Keep in main conversation when:**
- Task needs frequent back-and-forth or iterative refinement
- Multiple phases share significant context
- Making a quick, targeted change
- Latency matters

**Use subagents when:**
- Task produces verbose output you don't need in main context
- You want to enforce specific tool restrictions
- The work is self-contained and can return a summary

### Manage Subagent Context

#### Resume Subagents

After a subagent completes, you can resume it with full context:

```
Continue that code review and now analyze the authorization logic
```

Transcripts are stored at: `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`

#### Auto-Compaction

Subagents auto-compact when context grows too large. Configure with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (default: 50%).

## Example Subagents

### Code Reviewer

```yaml
---
name: code-reviewer
description: Expert code review specialist. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)
```

### Debugger

```yaml
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works
```

### Data Scientist

```yaml
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.
```

### Database Query Validator

```yaml
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access.
```

## Next Steps

- [Distribute subagents with plugins](https://code.claude.com/docs/en/plugins)
- [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) with the Agent SDK
- [Use MCP servers](https://code.claude.com/docs/en/mcp) to give subagents access to external tools
