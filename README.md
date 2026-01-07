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

## Adding Plugins

See individual plugin READMEs in `plugins/` for detailed documentation.
