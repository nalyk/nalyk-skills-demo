---
description: Decompose complex task and execute parallel agents
allowed-tools: Skill, Task, Read, Glob, Grep, Bash, Edit, Write, TodoWrite
---

# /orchestrate Command

Full orchestration workflow for complex multi-part tasks.

## Workflow

1. **Analyze request using orchestrator skill** (`skills/orchestrator/SKILL.md`)
   - The skill is automatically loaded and provides the orchestration protocol
   - It assesses complexity, decomposes tasks, and routes to appropriate agents
2. **Review execution plan** returned by the skill
3. **Confirm with user** if `confirm_before_execute: true`
4. **Execute phases:**
   - Launch parallel agents simultaneously for Phase 1
   - Wait for all Phase 1 agents to complete
   - Execute Sequential phases in order
   - Pass context between phases
5. **Synthesize results** into unified output

## Request

$ARGUMENTS

## Execution Rules

- Use `Task(subagent_type="Explore", ...)` for read-only exploration
- Use `Task(subagent_type="Plan", ...)` for deep analysis
- Use `Task(subagent_type="general-purpose", ...)` for implementation
- Launch parallel workstreams in single message with multiple Task calls
- Wait for phase completion before starting dependent phases
- Track progress with TodoWrite tool

## Error Handling

If a workstream fails:
1. Report failure clearly
2. Offer retry, skip, or cancel options
3. Do not proceed with dependent workstreams until resolved

## Output Format

Orchestration results follow a structured format for consistency and parseability.

### Completion Output

```
ORCHESTRATION COMPLETE
══════════════════════════════════════════════

**Summary:**
- Workstreams: [N]/[M] complete
- Total time: [duration]
- Phases: [count]

**Deliverables:**
1. [Type] [Description] - [location]
2. [Type] [Description] - [location]

**Files Modified:**
- [file path] (created|updated)

**Notes:**
- [observations and recommendations]

══════════════════════════════════════════════
```

### Partial Failure Output

```
PARTIAL COMPLETION
══════════════════════════════════════════════

**Completed:** [N-1]/[N] workstreams

**Successful:**
- [Workstream] - ✓

**Failed:**
- [Workstream] - ✗
  Error: [description]
  Impact: [affected downstream work]

**Options:**
1. Retry failed workstream
2. Accept partial results
3. Cancel orchestration

══════════════════════════════════════════════
```

For full output format specification, see: `skills/orchestrator/references/synthesis-rules.md`
