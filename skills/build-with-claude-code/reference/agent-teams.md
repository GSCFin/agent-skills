# Orchestrate Teams of Claude Code Sessions

> Source: https://code.claude.com/docs/en/agent-teams

Coordinate multiple Claude Code instances working together as a team, with shared tasks, inter-agent messaging, and centralized management.

> **Experimental Feature**: Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable. Check `claude --version` for compatibility.

## When to Use Agent Teams

Best use cases:
- **Research and review**: multiple teammates investigate different aspects simultaneously
- **New modules or features**: teammates each own a separate piece
- **Debugging with competing hypotheses**: test different theories in parallel
- **Cross-layer coordination**: frontend, backend, and tests each owned by different teammate

### Compare with Subagents

Agent teams are separate Claude Code processes that communicate via messaging. Subagents run within a single process. Use teams for parallel independent work; use subagents for delegated subtasks.

## Enable Agent Teams

Set the environment variable:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Start Your First Agent Team

```
I'm designing a CLI tool that helps developers track TODO comments across their
codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

## Control Your Agent Team

### Choose a Display Mode

- **In-process**: all teammates run inside your main terminal. Use `Shift+Down` to cycle through teammates.
- **Split panes**: each teammate gets its own pane. Requires `tmux` or iTerm2.

```json
{ "teammateMode": "in-process" }
```

Or via CLI: `claude --teammate-mode in-process`

Requirements for split panes:
- **tmux**: install through package manager
- **iTerm2**: install the `it2` CLI, enable Python API in settings

### Specify Teammates and Models

```
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### Require Plan Approval for Teammates

```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

### Talk to Teammates Directly

- **In-process mode**: `Shift+Down` to cycle, type to message. `Enter` to view session, `Escape` to interrupt. `Ctrl+T` for task list.
- **Split-pane mode**: click into a pane to interact directly.

### Assign and Claim Tasks

- **Lead assigns**: tell the lead which task to give to which teammate
- **Self-claim**: after finishing a task, a teammate picks up the next unassigned, unblocked task

### Shut Down Teammates

```
Ask the researcher teammate to shut down
```

### Clean Up the Team

```
Clean up the team
```

### Enforce Quality Gates with Hooks

- **TeammateIdle**: runs when a teammate is about to go idle. Exit code 2 sends feedback.
- **TaskCompleted**: runs when a task is being marked complete. Exit code 2 prevents completion.

## How Agent Teams Work

### How Claude Starts Agent Teams

1. **You request a team**: explicitly ask for a team
2. **Claude proposes a team**: Claude suggests if beneficial, you confirm

### Architecture

- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

### Permissions

All teammates inherit the lead's permission mode (`--dangerously-skip-permissions`).

### Context and Communication

- **Automatic message delivery**: messages delivered automatically
- **Idle notifications**: teammates notify lead when finished
- **Shared task list**: all agents can see task status
- **message**: send to one specific teammate
- **broadcast**: send to all (use sparingly — costs scale)

### Token Usage

Each teammate has its own context window and consumes tokens independently.

## Use Case Examples

### Run a Parallel Code Review

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
```

### Investigate with Competing Hypotheses

```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses.
Have them talk to each other to try to disprove each other's theories.
```

## Best Practices

### Give Teammates Enough Context

```
Spawn a security reviewer teammate with the prompt: "Review the authentication
module at src/auth/ for security vulnerabilities. Focus on token handling,
session management, and input validation."
```

### Choose an Appropriate Team Size

- Token costs scale linearly with team size
- Coordination overhead increases with more teammates
- Diminishing returns beyond a certain point

### Size Tasks Appropriately

- Too small → coordination overhead exceeds benefit
- Too large → teammates work too long without check-ins
- Just right → self-contained units with clear deliverables

### Wait for Teammates to Finish

```
Wait for your teammates to complete their tasks before proceeding
```

### Additional Tips

- Start with research and review before implementation
- Avoid file conflicts by assigning different files to different teammates
- Monitor and steer the team as needed

## Troubleshooting

### Teammates Not Appearing

- In in-process mode, press `Shift+Down` to find them
- Check task complexity — Claude may decide a team isn't needed
- Verify `tmux` is installed for split-pane mode

### Too Many Permission Prompts

Configure permission settings to reduce prompts.

### Teammates Stopping on Errors

- Give additional instructions directly
- Spawn a replacement teammate

### Lead Shuts Down Before Work is Done

Be aware that stopping the lead stops the team.

### Orphaned tmux Sessions

```bash
tmux ls
tmux kill-session -t <session-name>
```

## Limitations

- No session resumption with in-process teammates (`/resume` and `/rewind` don't restore them)
- Task status can lag
- Shutdown can be slow
- One team per session
- No nested teams (teammates can't spawn their own teams)
- Lead is fixed (can't transfer leadership)
- Permissions set at spawn
- Split panes require tmux or iTerm2

## Next Steps

- Lightweight delegation: [subagents](https://code.claude.com/docs/en/sub-agents)
- Manual parallel sessions: [Git worktrees](https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)
