---
description: Decompose complex task and execute parallel agents
allowed-tools: Skill, Task, Read, Glob, Grep, Bash, Edit, Write, TodoWrite
---

# /orchestrate Command

Full orchestration workflow for complex multi-part tasks.

## Workflow

1. **Invoke orchestrator skill** to analyze this request
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
