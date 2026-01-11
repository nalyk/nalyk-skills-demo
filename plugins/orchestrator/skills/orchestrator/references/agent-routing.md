# Agent Routing Rules

Detailed agent selection rules for orchestration workstreams.

## Available Agent Types

### Explore Agent

**Invocation:** `Task(subagent_type="Explore", prompt="...")`
**Model:** Haiku (fast, cheap)
**Capabilities:** Read-only codebase access
**Best for:**
- Finding files matching patterns
- Tracing code paths
- Mapping dependencies
- Pattern discovery
- Coverage analysis
- Understanding architecture

**Prompt Template:**
```
Investigate [TOPIC]:
1. Find [specific files/patterns]
2. Map [relationships/dependencies]
3. Return [paths, summaries, NOT implementations]

Focus: [specific search focus]
Thoroughness: [quick | medium | very thorough]
```

### Plan Agent

**Invocation:** `Task(subagent_type="Plan", prompt="...")`
**Mode:** Research/planning
**Best for:**
- Architecture decisions
- Trade-off analysis
- Design documentation
- Strategy formulation
- Risk assessment

**Prompt Template:**
```
Analyze [TOPIC]:
1. Consider multiple approaches
2. Evaluate trade-offs
3. Identify risks
4. Recommend strategy with rationale

Context: [background from prior phases]
Constraints: [limitations to consider]
```

### general-purpose Agent

**Invocation:** `Task(subagent_type="general-purpose", prompt="...")`
**Model:** Sonnet (balanced capability/cost)
**Capabilities:** Full tool access (Read, Write, Edit, Bash, etc.)
**Best for:**
- Implementation
- Refactoring
- Test writing
- Documentation
- Any file modifications

**Prompt Template:**
```
Implement [FEATURE]:
Context: [from prior phases]
Requirements: [specific deliverables]
Constraints: [limitations]
Success criteria: [how to verify]
```

## Decision Matrix

| Needs File Writes? | Needs Deep Analysis? | Agent |
|-------------------|---------------------|-------|
| No | No | Explore |
| No | Yes | Plan |
| Yes | No | general-purpose |
| Yes | Yes | general-purpose |

## Decision Tree

```
START
  │
  ▼
[NEEDS FILE MODIFICATIONS?]
  │
  ├── YES ──► general-purpose
  │
  └── NO
      │
      ▼
    [COMPLEX RESEARCH/PLANNING?]
      │
      ├── YES ──► Plan
      │
      └── NO ──► Explore
```

## Task Type Mapping

| Task Type | Recommended Agent | Rationale |
|-----------|-------------------|-----------|
| "Find all X" | Explore | Pattern matching, no writes |
| "How does X work" | Explore | Understanding, no writes |
| "Map dependencies" | Explore | Tracing, no writes |
| "Design X approach" | Plan | Trade-off analysis needed |
| "Choose between X and Y" | Plan | Decision making |
| "Implement X" | general-purpose | File writes needed |
| "Fix bug in X" | general-purpose | Code modifications |
| "Add tests for X" | general-purpose | Test file creation |
| "Refactor X" | general-purpose | Code changes |
| "Document X" | general-purpose | File writes |

## Cost-Effectiveness Rules

1. **Default to Explore** for any read-only operation
   - Cheapest (Haiku model)
   - Fastest execution
   - Sufficient for most research

2. **Use Plan sparingly** for genuine design decisions
   - Higher cost than Explore
   - Reserve for architectural choices
   - Don't use for simple lookups

3. **Use general-purpose** only when writes needed
   - Highest cost
   - Most capable
   - Required for implementation

## Parallel Execution Guidelines

When launching multiple agents in parallel:

```python
# GOOD: Independent research tasks
Task(subagent_type="Explore", prompt="Find auth patterns...")
Task(subagent_type="Explore", prompt="Check test coverage...")
Task(subagent_type="Explore", prompt="Map API routes...")

# BAD: Conflicting file modifications
Task(subagent_type="general-purpose", prompt="Edit file A...")
Task(subagent_type="general-purpose", prompt="Edit file A...")  # CONFLICT!
```

## Agent Limitations

### Explore Agent
- Cannot modify files
- Cannot run tests
- Cannot execute builds
- Limited tool access (Read, Glob, Grep, LS)

### Plan Agent
- All tools available
- Designed for research mode
- May not execute changes

### general-purpose Agent
- Full capabilities
- Higher latency
- Higher cost
