---
name: orchestrator
description: >-
  Strategic task decomposition and parallel agent orchestration.
  INVOKE PROACTIVELY when request is complex, multi-faceted, or mentions multiple deliverables.

  Triggers: "orchestrate", "parallelize", "multi-agent", or auto-detect complex requests.

  Auto-detection patterns:
  - "research and implement", "analyze and fix", "review everything"
  - "comprehensive", "full audit", "multiple files", "across the codebase"
  - Refactoring, migrations, multi-step investigations
  - Multiple AND-connected tasks ("add X and Y and Z")

  Commands:
  - /orchestrate - Full workflow: decompose -> route -> execute -> synthesize
  - /parallel [tasks] - Quick parallel launch without decomposition
  - /plan-only - Get execution plan without running it

  Output: English. Uses Task() for subagent dispatch.
---

# Orchestrator Protocol

Multi-agent task orchestration with intelligent decomposition and parallel execution.

## Activation Banner (MANDATORY)

When skill activates, display:

```
(ORCHESTRATOR) ════════════════════════════════════════
  Mode: [/orchestrate | /parallel | /plan-only | auto]
  Complexity: [SIMPLE | MODERATE | COMPLEX | EPIC]
  Workstreams detected: [N]
════════════════════════════════════════════════════════
```

## Phase 0: Complexity Assessment

Before anything, assess task complexity:

| Indicator | Points |
|-----------|--------|
| Multiple distinct deliverables | +1 |
| Cross-cutting concerns | +1 |
| >500 lines affected estimate | +1 |
| Multiple file types/domains | +1 |
| Integration requirements | +1 |

**Complexity levels:**
- 0-1: SIMPLE - No orchestration needed
- 2-3: MODERATE - Light orchestration, 2-3 workstreams
- 4-5: COMPLEX - Full orchestration, 3-5 workstreams
- 6+: EPIC - Multi-phase orchestration, 5+ workstreams

**Decision:**
- SIMPLE: Respond normally, no orchestration
- MODERATE+: Activate orchestration protocol

## Phase 1: Task Decomposition

Break the task into atomic workstreams using the AND/OR model:

### AND Tasks (must all complete)
Tasks connected by "and", "also", "plus":
- "Add auth AND logging AND tests" -> 3 workstreams

### Sequential Dependencies
Tasks where one depends on another:
- "Create schema THEN implement API THEN add tests"

### Parallel Opportunities
Independent tasks that can run simultaneously:
- Architecture exploration (Explore agent)
- Pattern research (Explore agent)
- Dependency check (Explore agent)

### Decomposition Output Format

```
WORKSTREAM MAP
══════════════════════════════════════

Phase 1 (Parallel):
  [1] Research: Explore existing patterns
      Agent: Explore | Est: 2min
  [2] Research: Check dependencies
      Agent: Explore | Est: 1min

Phase 2 (Sequential):
  [3] Implement: Core feature
      Agent: general-purpose | Est: 10min
      Depends: [1], [2]

Phase 3 (Parallel):
  [4] Test: Write unit tests
      Agent: general-purpose | Est: 5min
      Depends: [3]
  [5] Document: Update README
      Agent: general-purpose | Est: 3min
      Depends: [3]

══════════════════════════════════════
```

## Phase 2: Agent Routing

Select agent type based on task characteristics:

| Task Type | Agent | Rationale |
|-----------|-------|-----------|
| Code exploration | Explore | Read-only, fast, cheap |
| Pattern finding | Explore | No modifications needed |
| Dependency mapping | Explore | Just reading |
| Architecture research | Plan | Needs deep thinking |
| Design decisions | Plan | Trade-off analysis |
| Implementation | general-purpose | Full tool access |
| Refactoring | general-purpose | Needs edit capabilities |
| Testing | general-purpose | Needs to run tests |
| Documentation | general-purpose | Needs to write files |

### Routing Decision Tree

```
IS READ-ONLY?
  YES → IS COMPLEX RESEARCH?
    YES → Plan agent
    NO → Explore agent (fastest)
  NO → general-purpose (full capabilities)
```

### Agent Dispatch Format

```python
# Explore agent - read-only codebase scanning
Task(subagent_type="Explore", prompt="...")

# Plan agent - research/planning mode
Task(subagent_type="Plan", prompt="...")

# general-purpose - full tool access
Task(subagent_type="general-purpose", prompt="...")
```

## Phase 3: Execution Strategy

### Parallel Execution
Launch independent workstreams simultaneously:

```
EXECUTING PHASE 1 (PARALLEL)
────────────────────────────
[1] Launching Explore: Pattern research...
[2] Launching Explore: Dependency check...

Waiting for completion...

[1] ✓ Complete (45s)
[2] ✓ Complete (32s)
────────────────────────────
```

### Sequential Execution
Wait for dependencies before proceeding:

```
EXECUTING PHASE 2 (SEQUENTIAL)
────────────────────────────
[3] Launching general-purpose: Core implementation
    Inputs from [1], [2]: [summarized context]

[3] ✓ Complete (8m 23s)
────────────────────────────
```

### Context Passing
Each subsequent phase receives synthesized context from prior phases:

```
## Context from Phase 1

### Pattern Research [1]
- Found similar feature in src/existing/
- Uses factory pattern
- Tests in tests/existing.test.ts

### Dependency Check [2]
- No breaking changes needed
- Compatible with current API version
```

## Phase 4: Result Synthesis

Aggregate all workstream outputs into coherent result:

```
ORCHESTRATION COMPLETE
══════════════════════════════════════════════
Workstreams: 5/5 complete
Total time: 15m 42s
Phases: 3

DELIVERABLES:
1. [Feature] User authentication - src/auth/
2. [Tests] Unit tests added - tests/auth.test.ts
3. [Docs] README updated - README.md

NOTES:
- Pattern from existing auth used
- All tests passing
- No breaking changes introduced
══════════════════════════════════════════════
```

## Commands

### /orchestrate [task description]

Full orchestration workflow:
1. Assess complexity
2. Decompose into workstreams
3. Route to agents
4. Execute phases
5. Synthesize results

### /parallel [task1] [task2] [task3]

Quick parallel launch without full decomposition:
- Launches all tasks simultaneously
- All use default agent type unless prefixed:
  - `explore:task` -> Explore agent
  - `plan:task` -> Plan agent
  - `task` -> general-purpose

Example:
```
/parallel "explore:find all API routes" "explore:check test coverage" "review authentication flow"
```

### /plan-only [task description]

Returns execution plan without running:
- Shows decomposition
- Shows agent routing
- Shows phase ordering
- Does NOT execute

Useful for:
- Reviewing before committing
- Adjusting workstreams manually
- Learning what orchestrator would do

## Integration with Existing Plugins

### auto-ralph Integration
If orchestrator detects a workstream suitable for Ralph Loop:
- Flag with `[RALPH-CANDIDATE]`
- Suggest: "Consider delegating workstream [N] to auto-ralph"

Handoff pattern:
```
Workstream [3] detected as iterative task:
- Clear success criteria (tests pass)
- Benefits from iteration

Options:
1. Run as standard workstream
2. Delegate to auto-ralph for iteration
```

### ultrathink Integration
For Plan agent workstreams requiring deep analysis:
- Auto-apply ULTRATHINK protocol
- Ensure multi-perspective analysis
- No shallow answers in planning phases

## Error Handling

### Workstream Failure
```
WORKSTREAM [3] FAILED
─────────────────────
Error: Tests failing after implementation
Status: Blocked

Options:
1. Retry workstream [3]
2. Retry with more context
3. Delegate to auto-ralph for iteration
4. Cancel remaining workstreams
5. Continue with partial results
```

### Dependency Failure
If a phase fails, dependent phases cannot proceed:
```
DEPENDENCY BLOCKED
─────────────────────
Workstream [3] cannot start:
- Depends on [2] (FAILED)

Options:
1. Fix [2] and retry
2. Skip [2], provide manual context
3. Cancel [3] and dependents
```

## Anti-Patterns

- DO NOT orchestrate single-task requests
- DO NOT create >7 workstreams (cognitive overload)
- DO NOT use Plan agent for implementation
- DO NOT use Explore agent when writes needed
- DO NOT skip complexity assessment
- DO NOT ignore dependencies between workstreams

## Settings Persistence

Configuration in `~/.claude/orchestrator.local.md`:

```yaml
---
max_parallel_agents: 3
default_timeout_minutes: 30
auto_ralph_handoff: true
ultrathink_for_plan: true
verbose_progress: true
confirm_before_execute: true
---
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_parallel_agents | 3 | Max simultaneous agents |
| default_timeout_minutes | 30 | Per-workstream timeout |
| auto_ralph_handoff | true | Offer Ralph for iterative tasks |
| ultrathink_for_plan | true | Apply ULTRATHINK to Plan agents |
| verbose_progress | true | Show detailed progress |
| confirm_before_execute | true | Confirm plan before running |

## Resources

- **`references/agent-routing.md`** - Agent selection decision tree
- **`references/decomposition-rules.md`** - Task breakdown patterns
- **`references/phase-patterns.md`** - Execution phase patterns
- **`references/synthesis-rules.md`** - Result aggregation rules
- **`examples/`** - Real orchestration examples
