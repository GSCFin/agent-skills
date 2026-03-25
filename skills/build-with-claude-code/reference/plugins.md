# Create Plugins

> Source: https://code.claude.com/docs/en/plugins

Create custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers.

## When to Use Plugins vs Standalone Configuration

**Use standalone `.claude/` configuration when:**
- Customizing Claude Code for a single project
- Configuration is personal
- Experimenting before packaging
- Want short skill names like `/hello`

**Use plugins when:**
- Sharing functionality with team or community
- Need same skills/agents across multiple projects
- Want version control and easy updates
- Distributing through a marketplace
- Okay with namespaced skills like `/my-plugin:hello`

## Quickstart

### Prerequisites

- Claude Code installed and authenticated
- Version 1.0.33 or later (`claude --version`)

### Create Your First Plugin

**1. Create the plugin directory:**

```bash
mkdir my-first-plugin
```

**2. Create the plugin manifest:**

```bash
mkdir my-first-plugin/.claude-plugin
```

Create `my-first-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

**3. Add a skill:**

```bash
mkdir -p my-first-plugin/skills/hello
```

Create `my-first-plugin/skills/hello/SKILL.md`:

```markdown
---
description: Greet the user with a friendly message
disable-model-invocation: true
---

Greet the user warmly and ask how you can help them today.
```

**4. Test your plugin:**

```bash
claude --plugin-dir ./my-first-plugin
```

Then use `/my-first-plugin:hello` in the session.

**5. Add skill arguments:**

Use `$ARGUMENTS` in SKILL.md to capture user input:

```markdown
---
description: Greet the user with a personalized message
---

# Hello Skill

Greet the user named "$ARGUMENTS" warmly and ask how you can help them today.
```

Use with: `/my-first-plugin:hello Alex`

## Plugin Structure Overview

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── commands/                 # Custom slash commands
├── agents/                   # Subagent definitions
├── skills/                   # Skills (each with SKILL.md)
├── hooks/
│   └── hooks.json           # Hook definitions
├── .mcp.json                # MCP server configuration
├── .lsp.json                # LSP server configuration
└── settings.json            # Default settings
```

## Develop More Complex Plugins

### Add Skills to Your Plugin

Place skills in `skills/` directory, each with a `SKILL.md`:

```markdown
---
name: code-review
description: Reviews code for best practices and potential issues.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Reload with `/reload-plugins` after changes.

### Add LSP Servers to Your Plugin

Create `.lsp.json` at plugin root:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

### Ship Default Settings with Your Plugin

Create `settings.json` at plugin root:

```json
{
  "agent": "security-reviewer"
}
```

### Test Your Plugins Locally

```bash
claude --plugin-dir ./my-plugin
```

- Try skills with `/plugin-name:skill-name`
- Check agents in `/agents`
- Verify hooks work as expected
- Test multiple: `claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two`

### Debug Plugin Issues

1. Check structure: ensure directories are at plugin root, not inside `.claude-plugin/`
2. Test components individually
3. Use validation and debugging tools

### Share Your Plugins

1. Add documentation: include `README.md`
2. Version your plugin using semantic versioning
3. Create or use a marketplace
4. Test with others before distribution

### Submit to Official Marketplace

- Claude.ai: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- Console: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

## Convert Existing Configurations to Plugins

### Migration Steps

```bash
# Create plugin structure
mkdir -p my-plugin/.claude-plugin

# Copy existing files
cp -r .claude/commands my-plugin/
cp -r .claude/agents my-plugin/
cp -r .claude/skills my-plugin/

# Migrate hooks from settings.json to hooks/hooks.json
mkdir my-plugin/hooks
```

### What Changes When Migrating

| From | To |
|------|-----|
| `.claude/commands/` | `plugin-name/commands/` |
| `settings.json` hooks | `hooks/hooks.json` |
| Direct install | `/plugin install` |

## Next Steps

- **For users**: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- **For developers**: [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- Components: [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents), [Hooks](https://code.claude.com/docs/en/hooks), [MCP](https://code.claude.com/docs/en/mcp)
