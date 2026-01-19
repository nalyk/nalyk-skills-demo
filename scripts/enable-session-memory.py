#!/usr/bin/env python3
"""
Enable Claude Code Session Memory feature.

Session Memory automatically captures key information from conversations
and persists it to disk as markdown files. This is an unreleased feature
that can be enabled by modifying local feature flags.

Re-run this script if the server resets your flags after sync.

Feature details (reverse-engineered from Claude Code CLI):
- First trigger: ~10,000 tokens (~7,500 words)
- Subsequent triggers: every ~5,000 tokens OR every 3 tool calls
- Storage: ~/.claude/projects/{project}/{session-id}/session-memory/summary.md

Source: https://decodeclaude.com/session-memory/
"""
import json
import os

config_path = os.path.expanduser('~/.claude.json')

with open(config_path, 'r') as f:
    config = json.load(f)

# Enable feature flags in both caches
for cache in ['cachedStatsigGates', 'cachedGrowthBookFeatures']:
    if cache not in config:
        config[cache] = {}
    config[cache]['tengu_session_memory'] = True
    config[cache]['tengu_sm_compact'] = True

# Set thresholds (code defaults from CLI source)
config['cachedGrowthBookFeatures']['tengu_sm_config'] = {
    "minimumMessageTokensToInit": 10000,      # ~10k tokens to first trigger
    "minimumTokensBetweenUpdate": 5000,       # ~5k tokens between updates
    "toolCallsBetweenUpdates": 3              # every 3 tool calls
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("Session memory enabled.")
print("Restart Claude Code for changes to take effect.")
print()
print("Memory files will be stored at:")
print("  ~/.claude/projects/{project}/{session-id}/session-memory/summary.md")
