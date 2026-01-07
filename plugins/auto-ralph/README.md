# auto-ralph

Proactively detects tasks suitable for Ralph Loop iteration.

## Features

- Auto-scores tasks (0-4) based on clear criteria
- Generates optimized prompts for iteration
- Configurable via `~/.claude/auto-ralph.local.md`

## Configuration

Create `~/.claude/auto-ralph.local.md`:

```yaml
---
max_iterations: 25       # Max iterations (default: 25)
score_threshold: 3       # Min score for Ralph mode (default: 3)
skip_explore_for_score: 4 # Skip explore at this score (default: 4)
default_language: ro     # Output: ro/en/ru (default: ro)
auto_execute: false      # Skip confirmation (default: false)
docker_analysis: true    # Include Docker context (default: true)
---

# Auto-Ralph Settings

Personal configuration for the auto-ralph skill.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_iterations | 25 | Maximum Ralph Loop iterations |
| score_threshold | 3 | Minimum score for Ralph mode activation |
| skip_explore_for_score | 4 | Score at which to skip Explore phase |
| default_language | ro | Output language (ro/en/ru) |
| auto_execute | false | If true, skip confirmation prompt |
| docker_analysis | true | Include Docker in context detection |

## Learned Patterns

(Will be populated automatically in future versions)
```

## Triggers

**Explicit:** "ralph this", "auto ralph", "loop it", "iterate"

**Auto-detect (score >= 3):**
- Bug fixes ("fix", "repair", "repara")
- Features ("add", "implement", "adauga")
- Refactoring ("refactor", "clean up")

**Disable:** "just answer", "don't loop", "explain first"

## Scoring Criteria

| +1 point | Description |
|----------|-------------|
| Clear criteria | Keywords detected (fix, add, implement, etc.) |
| Iteration useful | Bug fix, feature, refactor (not questions) |
| Defined scope | Specific files/functions mentioned |
| Verifiable | Tests available or concrete error |

Score >= 3 -> Ralph mode | Score < 3 -> Normal response

## Language

- **Output:** Always Romanian
- **Input:** Accepts ro/en/ru/mixed without questions
- **Promise:** "GATA" (standard completion signal)
