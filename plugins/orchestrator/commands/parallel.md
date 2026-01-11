---
description: Quick parallel launch without full orchestration analysis
allowed-tools: Task, Read, Glob, Grep
---

# /parallel Command

Quick parallel launch of multiple tasks without full decomposition analysis.

## Usage

```
/parallel "task1" "task2" "task3"
```

## Agent Prefixes

- `explore:task` → Explore agent (read-only)
- `plan:task` → Plan agent (research/planning)
- `task` → general-purpose agent (default)

## Examples

```
/parallel "explore:find all API routes" "explore:check test coverage" "review auth flow"
```

```
/parallel "plan:design database schema" "explore:find similar implementations"
```

## Request

$ARGUMENTS

## Execution Rules

1. Parse the request for distinct parallel workstreams
2. Extract agent type from prefix (if any)
3. Launch up to 4 agents simultaneously
4. Collect and present unified results

## Constraints

- Maximum 4 parallel tasks
- No dependency analysis (all run simultaneously)
- Best for: obvious parallelization with independent tasks
