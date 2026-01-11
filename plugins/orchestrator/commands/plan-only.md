---
description: Get orchestration plan without executing it
allowed-tools: Skill, Read, Glob, Grep
---

# /plan-only Command

Generate and display execution plan without running any workstreams.

## Purpose

- **Preview** what orchestrator would do
- **Review** decomposition before committing
- **Adjust** workstreams manually if needed
- **Learn** how orchestrator analyzes tasks

## Request

$ARGUMENTS

## Workflow

1. **Invoke orchestrator skill** to analyze the request
2. **Display full execution plan:**
   - Complexity assessment
   - Workstream decomposition
   - Agent routing decisions
   - Phase ordering
   - Dependency graph
3. **DO NOT execute** any workstreams
4. **Return plan** for user review

## Output Format

```
EXECUTION PLAN (NOT EXECUTED)
══════════════════════════════════════════════

**Complexity:** [SIMPLE | MODERATE | COMPLEX | EPIC]

**Phase 1 (Parallel):**
  [1] [Agent: Explore] Task description
  [2] [Agent: Explore] Task description

**Phase 2 (Sequential):**
  [3] [Agent: general-purpose] Task description
      Depends: [1], [2]

**Estimated total:** [X] workstreams across [Y] phases

══════════════════════════════════════════════

To execute this plan, run:
/orchestrate [same task description]
```

## Next Steps

After reviewing the plan, user can:
1. Run `/orchestrate` with same task to execute
2. Modify the request and re-run `/plan-only`
3. Execute workstreams manually with custom routing
