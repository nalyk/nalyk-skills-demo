---
name: statusline-auto-configure
description: Auto-configure statusline on session start if not already set
event: SessionStart
type: command
command: bash ${CLAUDE_PLUGIN_ROOT}/scripts/auto-configure.sh
---
