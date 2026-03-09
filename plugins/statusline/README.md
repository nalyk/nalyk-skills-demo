# statusline

Powerline-style statusline for Claude Code. Displays git status, context window usage, model info, and vim mode in the terminal status bar.

## Installation

```bash
/plugin install statusline@nalyk-skills-demo
```

The plugin auto-configures on first session start via a `SessionStart` hook. No manual setup required.

## Requirements

- `jq` (for JSON parsing)
- Terminal with Unicode support
- Powerline-compatible font (recommended, not required)

## What It Shows

- Model badge (Opus/Sonnet/Haiku)
- Current directory
- Git branch with ahead/behind counts
- Staged/modified/untracked file counts
- Context window usage meter
- Vim mode indicator
- Timestamp

## Manual Configuration

If auto-configuration fails, add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash <plugin-path>/scripts/statusline-command.sh"
  }
}
```

Where `<plugin-path>` is the installed plugin directory (typically `~/.claude/plugins/cache/nalyk-skills-demo/statusline/2.0.0`).

Restart Claude Code after configuration changes.

## Structure

```
statusline/
├── .claude-plugin/plugin.json
├── hooks/
│   └── hooks.json              # SessionStart auto-configure trigger
├── scripts/
│   ├── auto-configure.sh       # Automatic setup
│   └── statusline-command.sh   # Status bar renderer
├── agents/
│   └── statusline-setup.md
└── skills/
    └── enable-statusline/
        └── enable-statusline.md
```

## License

MIT
