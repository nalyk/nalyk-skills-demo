# nalyk-skills

Personal Claude Code plugin marketplace.

## Installation

```bash
/plugin marketplace add nalyk/nalyk-skills
```

## Available Plugins

### auto-ralph

Proactively detects tasks suitable for Ralph Loop iteration. Auto-scores tasks (0-4),
generates optimized prompts, and executes with configurable iterations.

**Install:**
```bash
/plugin install auto-ralph@nalyk-skills
```

**Configure (optional):** Create `~/.claude/auto-ralph.local.md`:
```yaml
---
max_iterations: 25
score_threshold: 3
skip_explore_for_score: 4
default_language: ro
auto_execute: false
docker_analysis: true
---
```

**Triggers:**
- Explicit: "ralph this", "auto ralph", "loop it"
- Auto-detect: Bug fixes, feature requests, refactoring (score >= 3/4)

**Output:** Romanian (accepts input in ro/en/ru/mixed)

## Scripts

### enable-session-memory.py

Enables the unreleased Claude Code Session Memory feature by modifying local feature flags.

**What it does:**
- Enables `tengu_session_memory` and `tengu_sm_compact` flags in `~/.claude.json`
- Sets thresholds to code defaults (not server defaults which are much higher)

**Thresholds:**
| Setting | Server Default | Script Sets |
|---------|---------------|-------------|
| First trigger | 140,000 tokens | **10,000 tokens** |
| Update interval | 10,000 tokens | **5,000 tokens** |
| Tool call trigger | 5 calls | **3 calls** |

**Usage:**
```bash
python3 scripts/enable-session-memory.py
# Then restart Claude Code
```

**Storage location:**
```
~/.claude/projects/{project}/{session-id}/session-memory/summary.md
```

**Note:** The server may reset these flags on sync. Re-run the script if session memory stops working.

Source: [decodeclaude.com/session-memory](https://decodeclaude.com/session-memory/)

## Adding Plugins

See individual plugin READMEs in `plugins/` for detailed documentation.
