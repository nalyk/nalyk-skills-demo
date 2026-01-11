# orchestrator

Multi-agent task orchestration with intelligent decomposition and parallel execution.

## Features

- **Auto-detection** of complex multi-part tasks
- **Smart decomposition** into parallel/sequential workstreams
- **Agent routing** to Explore, Plan, or general-purpose agents
- **Phase execution** with dependency management
- **Result synthesis** into coherent output

## Commands

### /orchestrate [task]

Full orchestration workflow:
1. Assess complexity
2. Decompose into workstreams
3. Route to appropriate agents
4. Execute phases (parallel and sequential)
5. Synthesize results

```
/orchestrate add user authentication, request logging, and rate limiting
```

### /parallel [tasks...]

Quick parallel launch without decomposition:

```
/parallel "explore:find all API routes" "explore:check test coverage" "review auth flow"
```

Prefixes:
- `explore:` → Explore agent (read-only)
- `plan:` → Plan agent (research)
- No prefix → general-purpose agent

### /plan-only [task]

Preview execution plan without running:

```
/plan-only migrate user service to TypeScript
```

## Auto-Detection

Orchestrator activates automatically on patterns like:
- "research and implement"
- "analyze and fix"
- "comprehensive review"
- "audit everything"
- Multiple AND-connected tasks
- Migrations, refactoring, multi-file changes

## Complexity Levels

| Level | Points | Workstreams |
|-------|--------|-------------|
| SIMPLE | 0-1 | No orchestration |
| MODERATE | 2-3 | 2-3 workstreams |
| COMPLEX | 4-5 | 3-5 workstreams |
| EPIC | 6+ | 5+ workstreams |

## Agent Types

| Agent | Use Case | Model |
|-------|----------|-------|
| Explore | Read-only codebase scanning | Haiku |
| Plan | Research and planning | Sonnet |
| general-purpose | Implementation, testing | Sonnet |

## Configuration

Create `~/.claude/orchestrator.local.md`:

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
| max_parallel_agents | 3 | Maximum simultaneous agents |
| default_timeout_minutes | 30 | Per-workstream timeout |
| auto_ralph_handoff | true | Offer Ralph Loop for iterative tasks |
| ultrathink_for_plan | true | Apply ULTRATHINK to Plan agents |
| verbose_progress | true | Show detailed execution progress |
| confirm_before_execute | true | Confirm plan before running |

## Integration

### auto-ralph

Iterative workstreams are flagged as `[RALPH-CANDIDATE]` with option to delegate.

### ultrathink

Plan agent workstreams automatically apply deep analysis protocol.

## Examples

See `skills/orchestrator/examples/` for detailed walkthroughs:
- `multi-feature.md` - Auth + logging + rate limiting
- `codebase-migration.md` - JavaScript to TypeScript
- `parallel-research.md` - Multi-agent codebase exploration

## Resources

- `skills/orchestrator/references/agent-routing.md` - Agent selection rules
- `skills/orchestrator/references/decomposition-rules.md` - Task breakdown patterns
- `skills/orchestrator/references/phase-patterns.md` - Execution strategies
- `skills/orchestrator/references/synthesis-rules.md` - Result aggregation

## License

MIT
