# Run Claude Code Programmatically

> Source: https://code.claude.com/docs/en/headless

Use the Agent SDK to run Claude Code programmatically from the CLI, Python, or TypeScript.

## Basic Usage

Use `-p` or `--print` flag for non-interactive mode:

```bash
claude -p "What does the auth module do?"
```

Key flags:
- `--continue` — continue previous conversation
- `--allowedTools` — auto-approve specific tools
- `--output-format` — control output format

## Examples

### Get Structured Output

```bash
# Plain text (default)
claude -p "Summarize this project"

# JSON output
claude -p "Summarize this project" --output-format json

# JSON with structured schema
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Output formats:
- `text` — plain text (default)
- `json` — structured JSON with result, session ID, and metadata
- `stream-json` — newline-delimited JSON for real-time streaming

Parse with `jq`:

```bash
claude -p "Summarize" --output-format json | jq -r '.result'
```

### Stream Responses

```bash
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

Real-time text streaming:

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

### Auto-Approve Tools

```bash
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

### Create a Commit

```bash
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Note: `Bash(git diff *)` allows `git diff` followed by anything. Without trailing `*`, it only allows exact match.

### Customize the System Prompt

```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Also available: `--system-prompt` for full replacement.

### Continue Conversations

```bash
# First request
claude -p "Review this codebase for performance issues"

# Continue most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Resume specific session by ID:

```bash
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Next Steps

- [Agent SDK quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)
