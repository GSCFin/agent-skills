# Run Prompts on a Schedule

> Source: https://code.claude.com/docs/en/scheduled-tasks

Use `/loop` and cron scheduling tools to run prompts repeatedly, poll for status, or set one-time reminders.

## Schedule a Recurring Prompt with /loop

```
/loop 5m check if the deployment finished and tell me what happened
```

### Interval Syntax

- Use duration suffixes: `s` (seconds), `m` (minutes), `h` (hours), `d` (days)
- Natural language: `/loop check the build every 2 hours`
- Without interval: `/loop check the build` (uses default)

### Loop Over Another Command

```
/loop 20m /review-pr 1234
```

## Set a One-Time Reminder

```
remind me at 3pm to push the release branch
in 45 minutes, check whether the integration tests passed
```

## Manage Scheduled Tasks

```
what scheduled tasks do I have?
cancel the deploy check job
```

Tools used: `CronCreate`, `CronList`, `CronDelete`

## How Scheduled Tasks Run

Tasks use cron expressions internally (e.g., `0 9 * * *`).

### Jitter

- Recurring tasks fire up to 10% of their period late, capped at 15 minutes
- One-shot tasks scheduled for top/bottom of hour fire up to 90 seconds early

### Three-Day Expiry

Tasks expire after 3 days by default.

## Cron Expression Reference

Format: `minute hour day-of-month month day-of-week`

| Pattern | Description |
|---------|-------------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour |
| `0 9 * * *` | Daily at 9 AM |
| `0 9 * * 1-5` | Weekdays at 9 AM |
| `30 14 15 3 *` | March 15 at 2:30 PM |

## Disable Scheduled Tasks

```bash
CLAUDE_CODE_DISABLE_CRON=1
```

## Limitations

- Tasks only fire while Claude Code is running and idle
- No catch-up for missed fires
- No persistence across restarts
- For persistent scheduling, use GitHub Actions with `schedule`
