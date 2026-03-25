# Connect Claude Code to Tools via MCP

> Source: https://code.claude.com/docs/en/mcp

Learn how to connect Claude Code to your tools with the Model Context Protocol.

## What You Can Do with MCP

MCP lets Claude Code connect to external tools and data sources through standardized servers.

## Popular MCP Servers

Available through the official marketplace or custom setup.

## Installing MCP Servers

### Option 1: Add a Remote HTTP Server

Use `/mcp add` with an HTTP URL.

### Option 2: Add a Remote SSE Server

Use `/mcp add` with an SSE endpoint.

### Option 3: Add a Local stdio Server

```bash
claude mcp add my-server -e KEY=value -- npx -y @my/mcp-server
```

### Managing Your Servers

```bash
claude mcp list
claude mcp remove my-server
```

### Dynamic Tool Updates

MCP servers can dynamically add/remove tools during a session.

### Plugin-Provided MCP Servers

Plugins can ship their own MCP server configurations.

## MCP Installation Scopes

### Local Scope

For yourself in this repository only.

### Project Scope

Shared with collaborators via `.mcp.json`.

### User Scope

For yourself across all projects (`~/.claude/.mcp.json`).

### Choosing the Right Scope

| Use case | Scope |
|----------|-------|
| Personal tools | User |
| Team tools | Project |
| Repo-specific | Local |

### Environment Variable Expansion in .mcp.json

Use `$VAR_NAME` or `${VAR_NAME}` in `.mcp.json` for secrets.

## Practical Examples

### Monitor Errors with Sentry

```bash
claude mcp add sentry -- npx -y @sentry/mcp-server
```

### Connect to GitHub for Code Reviews

```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

### Query Your PostgreSQL Database

```bash
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://..."
```

## Authenticate with Remote MCP Servers

### Use a Fixed OAuth Callback Port

For predictable OAuth flows.

### Use Pre-Configured OAuth Credentials

Set credentials via environment variables.

### Override OAuth Metadata Discovery

Customize the discovery endpoint.

## Add MCP Servers from JSON Configuration

Provide server config directly in JSON format.

## Import MCP Servers from Claude Desktop

Reuse existing Claude Desktop MCP configurations.

## Use MCP Servers from Claude.ai

Share MCP servers between Claude.ai and Claude Code.

## Use Claude Code as an MCP Server

Run Claude Code itself as an MCP server for other applications.

## MCP Output Limits and Warnings

Be aware of token limits for MCP tool outputs.

## Respond to MCP Elicitation Requests

Handle interactive prompts from MCP servers.

## Use MCP Resources

### Reference MCP Resources

Access data exposed by MCP servers as resources.

## Scale with MCP Tool Search

### How It Works

For servers with many tools, MCP Tool Search finds the right tools dynamically.

### For MCP Server Authors

Implement tool search to help clients discover relevant tools.

### Configure Tool Search

Enable/disable tool search per server.

## Use MCP Prompts as Commands

### Execute MCP Prompts

Use MCP-provided prompts as slash commands.

## Managed MCP Configuration

### Option 1: Exclusive Control with managed-mcp.json

Centrally manage MCP servers for an organization.

### Option 2: Policy-Based Control with Allowlists and Denylists

Control which MCP servers can be installed via policy.
