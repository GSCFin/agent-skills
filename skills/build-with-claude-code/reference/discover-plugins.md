# Discover and Install Prebuilt Plugins Through Marketplaces

> Source: https://code.claude.com/docs/en/discover-plugins

Find and install plugins from marketplaces to extend Claude Code with new commands, agents, and capabilities.

## How Marketplaces Work

1. Add the marketplace
2. Install individual plugins

## Official Anthropic Marketplace

The official marketplace is `claude-plugins-official`.

```bash
/plugin install plugin-name@claude-plugins-official
```

### Code Intelligence

LSP-based plugins providing diagnostics and code navigation:

| Plugin | Language Server |
|--------|----------------|
| `clangd-lsp` | clangd (C/C++) |
| `csharp-lsp` | csharp-ls |
| `gopls-lsp` | gopls (Go) |
| `jdtls-lsp` | jdtls (Java) |
| `kotlin-lsp` | kotlin-language-server |
| `lua-lsp` | lua-language-server |
| `php-lsp` | intelephense |
| `pyright-lsp` | pyright-langserver (Python) |
| `rust-analyzer-lsp` | rust-analyzer |
| `swift-lsp` | sourcekit-lsp |
| `typescript-lsp` | typescript-language-server |

**What Claude gains:**
- Automatic diagnostics after every file edit
- Code navigation: jump to definitions, find references, get type info
- Automatic error detection and self-correction

### External Integrations

MCP server-based plugins:
- **Source control**: github, gitlab
- **Project management**: atlassian, asana, linear, notion
- **Design**: figma
- **Infrastructure**: vercel, firebase, supabase
- **Communication**: slack
- **Monitoring**: sentry

### Development Workflows

- `commit-commands`: Git commit workflows
- `pr-review-toolkit`: PR review agents
- `agent-sdk-dev`: Claude Agent SDK tools
- `plugin-dev`: Plugin creation toolkit

### Output Styles

- `explanatory-output-style`: Educational insights
- `learning-output-style`: Interactive learning mode

## Try It: Add the Demo Marketplace

```bash
/plugin marketplace add anthropics/claude-code
```

Browse with `/plugin`, install with:

```bash
/plugin install commit-commands@anthropics-claude-code
```

Use with: `/commit-commands:commit`

## Add Marketplaces

```bash
/plugin marketplace add <source>
```

### Add from GitHub

```bash
/plugin marketplace add anthropics/claude-code
```

### Add from Other Git Hosts

```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Add from Local Paths

```bash
/plugin marketplace add ./my-marketplace
/plugin marketplace add ./path/to/marketplace.json
```

### Add from Remote URLs

```bash
/plugin marketplace add https://example.com/marketplace.json
```

## Install Plugins

```bash
/plugin install plugin-name@marketplace-name
```

Installation scopes:
- **User scope** (default): across all projects
- **Project scope**: for all collaborators (adds to `.claude/settings.json`)
- **Local scope**: for yourself in this repo only

## Manage Installed Plugins

```bash
/plugin disable plugin-name@marketplace-name
/plugin enable plugin-name@marketplace-name
/plugin uninstall plugin-name@marketplace-name
```

CLI with scope:

```bash
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Apply Plugin Changes Without Restarting

```bash
/reload-plugins
```

## Manage Marketplaces

```bash
/plugin marketplace list
/plugin marketplace update marketplace-name
/plugin marketplace remove marketplace-name
```

### Configure Auto-Updates

Use `/plugin` → Marketplaces → select marketplace → Enable/Disable auto-update.

Force auto-update even when DISABLE_AUTOUPDATER is set:

```bash
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

## Configure Team Marketplaces

Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

## Troubleshooting

### /plugin Command Not Recognized

1. Check version: `claude --version` (requires 1.0.33+)
2. Update: `brew upgrade claude-code` or `npm update -g @anthropic-ai/claude-code`
3. Restart Claude Code

### Common Issues

- **Marketplace not loading**: verify URL and `marketplace.json` exists
- **Plugin installation failures**: check source URLs are accessible
- **Files not found**: plugins are copied to cache, external paths won't work
- **Skills not appearing**: `rm -rf ~/.claude/plugins/cache`, restart, reinstall

### Code Intelligence Issues

- **Server not starting**: verify binary in `$PATH`
- **High memory**: disable plugin with `/plugin disable <name>`
- **False positives in monorepos**: workspace configuration issue

## Next Steps

- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
