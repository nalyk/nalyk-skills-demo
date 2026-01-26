---
name: enable-statusline
description: Enable the premium powerline statusline in Claude Code settings
---

# Enable Premium Statusline

This skill configures the premium powerline-style statusline.

## What to do

1. Determine the plugin's script location by finding the statusline-command.sh in the statusline plugin directory

2. Update the user's `~/.claude/settings.json` to add/update the statusLine configuration:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash <path-to-plugin>/scripts/statusline-command.sh"
  }
}
```

3. The path should be resolved relative to where the plugin is installed. Check the plugin directory path.

4. Confirm to the user that the statusline has been enabled and they need to restart Claude Code to see it.

## Notes

- The script requires `jq` to be installed for JSON parsing
- Works best with a terminal that supports Unicode and powerline fonts
- Shows: model badge, directory, git status (branch, ahead/behind, staged/modified/untracked), context window meter, vim mode, time
