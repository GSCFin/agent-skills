# Automate Workflows with Hooks

> Source: https://code.claude.com/docs/en/hooks-guide

Run shell commands automatically when Claude Code edits files, finishes tasks, or needs input.

## Set Up Your First Hook

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

Verify with `/hooks`, test by pressing `Esc`.

## What You Can Automate

### Get Notified When Claude Needs Input

Use `Notification` event with platform-specific notification commands (macOS: `osascript`, Linux: `notify-send`, Windows: PowerShell).

### Auto-Format Code After Edits

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}
```

### Block Edits to Protected Files

Create `.claude/hooks/protect-files.sh`:

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")
for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done
exit 0
```

Register as `PreToolUse` hook with matcher `Edit|Write`.

### Re-Inject Context After Compaction

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing.'"
      }]
    }]
  }
}
```

### Audit Configuration Changes

Use `ConfigChange` event to log all setting changes.

## How Hooks Work

### Available Events

| Event | When |
|-------|------|
| `SessionStart` | Session starts or resumes |
| `UserPromptSubmit` | User submits a prompt |
| `PreToolUse` | Before a tool executes |
| `PermissionRequest` | Permission prompt shown |
| `PostToolUse` | After a tool executes |
| `PostToolUseFailure` | After a tool fails |
| `Notification` | Claude needs attention |
| `SubagentStart` / `SubagentStop` | Subagent lifecycle |
| `Stop` | Claude finishes responding |
| `TeammateIdle` | Agent team teammate goes idle |
| `TaskCompleted` | Task marked complete |
| `InstructionsLoaded` | Rules loaded |
| `ConfigChange` | Settings changed |
| `WorktreeCreate` / `WorktreeRemove` | Git worktree lifecycle |
| `PreCompact` / `PostCompact` | Context compaction |
| `SessionEnd` | Session exits |

### Hook Types

- `"type": "command"` — shell command
- `"type": "http"` — POST to a URL
- `"type": "prompt"` — single-turn LLM evaluation
- `"type": "agent"` — multi-turn verification with tool access

### Hook Input

Hooks receive JSON via stdin with:
- `session_id`, `cwd`, `hook_event_name`
- Event-specific fields (e.g., `tool_name`, `tool_input` for PreToolUse)

### Hook Output

- **Exit 0**: action proceeds. Stdout added to Claude's context for UserPromptSubmit/SessionStart.
- **Exit 2**: action blocked. Stderr sent as feedback to Claude.
- **Other exit codes**: action proceeds, stderr logged.

### Structured JSON Output

For `PreToolUse`, return JSON with `permissionDecision`:
- `"allow"` — proceed without permission prompt
- `"deny"` — cancel and send reason to Claude
- `"ask"` — show permission prompt normally

### Filter Hooks with Matchers

```
"matcher": "Edit|Write"     # Match tool names
"matcher": "Bash"           # Match specific tool
"matcher": "mcp__.*"        # Match MCP tools (regex)
"matcher": "compact"        # Match SessionStart trigger
```

### Configure Hook Location

| File | Scope |
|------|-------|
| `~/.claude/settings.json` | Global |
| `.claude/settings.json` | Project (shared) |
| `.claude/settings.local.json` | Project (personal) |
| Plugin `hooks/hooks.json` | Plugin-scoped |
| Skill/agent frontmatter | Skill/agent-scoped |

Verify with `/hooks`. Disable all with `"disableAllHooks": true`.

## Prompt-Based Hooks

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains\"}."
      }]
    }]
  }
}
```

## Agent-Based Hooks

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "agent",
        "prompt": "Verify that all unit tests pass. Run the test suite.",
        "timeout": 120
      }]
    }]
  }
}
```

## HTTP Hooks

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "http",
        "url": "http://localhost:8080/hooks/tool-use",
        "headers": { "Authorization": "Bearer $MY_TOKEN" },
        "allowedEnvVars": ["MY_TOKEN"]
      }]
    }]
  }
}
```

## Limitations and Troubleshooting

### Limitations

- Command hooks communicate through stdout/stderr/exit codes only
- Default timeout: 10 minutes (configurable per hook)
- PostToolUse hooks cannot undo actions
- PermissionRequest hooks don't fire in non-interactive mode (`-p`)
- Stop hooks fire whenever Claude finishes, not only at task completion

### Debugging

- Run `/hooks` to verify configuration
- Check matchers are case-sensitive
- Test scripts manually with piped JSON
- Make scripts executable: `chmod +x ./my-hook.sh`
- Use `Ctrl+O` for verbose mode or `claude --debug`
