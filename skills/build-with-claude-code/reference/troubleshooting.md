# Troubleshooting

> Source: https://code.claude.com/docs/en/troubleshooting

Solutions to common issues with Claude Code installation and usage.

## Troubleshoot Installation Issues

### Debug Installation Problems

1. **Check network connectivity**: ensure you can reach Anthropic's servers
2. **Verify your PATH**: confirm `claude` binary is in your PATH
3. **Check for conflicting installations**: look for multiple versions
4. **Check directory permissions**: ensure write access to install directory
5. **Verify the binary works**: run `claude --version`

## Common Installation Issues

### Install Script Returns HTML

Network proxy or firewall may be intercepting the download.

### `command not found: claude` After Installation

Add the installation directory to your PATH.

### `curl: (56) Failure writing output to destination`

Check disk space and permissions.

### TLS or SSL Connection Errors

Update your system's CA certificates or check proxy settings.

### Failed to Fetch Version

Check network connectivity to `storage.googleapis.com`.

### Windows: `irm` or `&&` Not Recognized

Use PowerShell (not cmd.exe).

### Install Killed on Low-Memory Linux

The binary requires adequate memory. Try increasing swap space.

### Install Hangs in Docker

Run without TTY allocation or use `--no-interactive` flag.

### Windows: Claude Desktop Overrides `claude` CLI Command

Rename or adjust PATH priority.

### Windows: "Claude Code on Windows requires git-bash"

Install Git for Windows and use Git Bash.

### Linux: Wrong Binary Variant (musl/glibc Mismatch)

Check `ldd --version` and install the correct variant.

### Illegal Instruction on Linux

CPU may not support required instruction set.

### `dyld: cannot load` on macOS

System library compatibility issue. Try reinstalling.

### Windows Installation Issues in WSL

Follow WSL-specific installation instructions.

### Permission Errors During Installation

Use appropriate permissions or install to user directory.

## Permissions and Authentication

### Repeated Permission Prompts

Configure permission settings to reduce prompts.

### Authentication Issues

Re-authenticate with `claude login`.

### OAuth Error: Invalid Code

Clear cached tokens and re-authenticate.

### 403 Forbidden After Login

Check subscription status and API access.

### OAuth Login Fails in WSL2

Use browser forwarding or manual token entry.

### "Not Logged In" or Token Expired

Tokens expire periodically. Re-authenticate.

## Configuration File Locations

Key configuration files:
- `~/.claude/settings.json` — user settings
- `.claude/settings.json` — project settings
- `.claude/settings.local.json` — local project settings
- `~/.claude/.mcp.json` — MCP server config

### Resetting Configuration

Delete or rename configuration files to reset.

## Performance and Stability

### High CPU or Memory Usage

- Check for large files in the working directory
- Use `.claudeignore` to exclude unnecessary files
- Restart Claude Code

### Command Hangs or Freezes

- Check network connectivity
- Ensure no conflicting processes
- Try `claude --debug` for diagnostics

### Search and Discovery Issues

Claude Code may miss files in very large repositories. Use specific paths.

### Slow or Incomplete Search Results on WSL

WSL filesystem access is slower than native. Use Linux-native paths.

## IDE Integration Issues

### JetBrains IDE Not Detected on WSL2

Configure the IDE to listen on the WSL2 IP address.

### Report Windows IDE Integration Issues

File issues on the Claude Code GitHub repository.

### Escape Key Not Working in JetBrains IDE Terminals

Configure terminal keybindings for the escape key.

## Markdown Formatting Issues

### Missing Language Tags in Code Blocks

Enable language-specific formatting.

### Inconsistent Spacing and Formatting

Use output styles for consistent formatting preferences.

### Reduce Markdown Formatting Issues

Configure formatting preferences in settings.

## Get More Help

- [GitHub issues](https://github.com/anthropics/claude-code/issues)
- [Support center](https://support.claude.com/)
- [Discord community](https://discord.gg/anthropic)
