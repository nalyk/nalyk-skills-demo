# auto-ralph

Deterministic Ralph Loop activation via UserPromptSubmit hook.

## v2.0 Changes

**Problem solved:** In v1.0, skill activation was probabilistic - Claude had to recognize when to invoke the skill, which wasn't guaranteed.

**Solution:** Added a `UserPromptSubmit` hook that injects a scoring reminder into EVERY user prompt, ensuring Claude always evaluates tasks for Ralph Loop suitability.

## Architecture

```
User prompt → Hook injects scoring reminder → Claude scores (0-4) →
  Score >= 3? → Invoke auto-ralph skill → Generate prompt → Execute ralph-loop
  Score < 3?  → Normal response
```

## Features

- **Deterministic activation** via UserPromptSubmit hook (NEW in v2.0)
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
