---
name: statusline-setup
description: Configure the premium powerline statusline in Claude Code settings
allowedTools:
  - Read
  - Edit
  - Write
  - Glob
  - Bash
---

# Statusline Setup Agent

You are setting up the premium powerline statusline for Claude Code.

## Task

1. Find the statusline-command.sh script in this plugin:
   - Use Glob to find `**/statusline/scripts/statusline-command.sh`
   - Get the absolute path

2. Read the current `~/.claude/settings.json`

3. Update or add the statusLine configuration:
   ```json
   "statusLine": {
     "type": "command",
     "command": "bash <absolute-path-to-script>"
   }
   ```

4. Preserve all other settings in the file

5. Report success and remind the user to restart Claude Code

## Important

- Always preserve existing settings
- Use the absolute path to the script
- The script must be executable (chmod +x if needed)
