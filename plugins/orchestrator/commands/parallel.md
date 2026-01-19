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

## Error Handling

When one or more parallel tasks fail:

1. **Partial results are returned** - Successful tasks still provide their output
2. **Failed tasks are clearly marked** with error description
3. **No automatic retry** - User decides whether to retry failed tasks

### Failure Output Format

```
PARALLEL EXECUTION RESULTS
──────────────────────────
[1] explore:find API routes     ✓ Complete
[2] explore:check coverage      ✗ FAILED: Timeout after 120s
[3] review auth flow            ✓ Complete

Successful: 2/3
Failed: 1/3

Failed task details:
- [2] Timeout - consider breaking into smaller scope or using /orchestrate for complex tasks
```

### When to Use /orchestrate Instead

If your parallel tasks:
- Have dependencies between them
- Require error recovery with context
- Need sophisticated retry logic

Consider using `/orchestrate` which provides full error handling with retry, skip, and cancel options.
