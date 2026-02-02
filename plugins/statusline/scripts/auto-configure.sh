#!/bin/bash
# Auto-configure statusline on first run

SETTINGS_FILE="$HOME/.claude/settings.json"
PLUGIN_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/statusline-command.sh"

# Check if settings file exists
if [ ! -f "$SETTINGS_FILE" ]; then
    exit 0
fi

# Check if statusline is already pointing to our script
current=$(jq -r '.statusLine.command // ""' "$SETTINGS_FILE" 2>/dev/null)

if [[ "$current" == *"nalyk-skills"*"statusline"* ]]; then
    # Already configured to use this plugin
    exit 0
fi

# Auto-configure: update settings to use this plugin's statusline
# Use a temp file for atomic update
tmp=$(mktemp)
jq --arg cmd "bash $PLUGIN_SCRIPT" '.statusLine = {"type": "command", "command": $cmd}' "$SETTINGS_FILE" > "$tmp" && mv "$tmp" "$SETTINGS_FILE"

echo "Statusline plugin auto-configured. Restart Claude Code to see the new statusline."
