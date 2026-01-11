# Result Synthesis Rules

How to aggregate and present orchestration results.

## Per-Workstream Summary

Each completed workstream should report:

```
### Workstream [N]: [Title]

**Status:** Complete | Failed | Partial
**Duration:** [time]
**Agent:** Explore | Plan | general-purpose

**Deliverables:**
- [what was produced]

**Notes:**
- [important observations]
```

## Cross-Workstream Synthesis

After all workstreams complete:

### Conflict Detection

Check for contradictions between workstreams:
```
CONFLICT DETECTED
─────────────────
Workstream [2] found: Use pattern A
Workstream [3] found: Use pattern B

Resolution needed before proceeding.
```

### Gap Analysis

Identify what was missed:
```
GAP ANALYSIS
─────────────────
Original request: Add auth, logging, AND tests
Completed: auth, logging
Missing: tests (workstream [4] failed)
```

### Dependency Verification

Confirm all dependencies resolved:
```
DEPENDENCY CHECK
─────────────────
[3] depends on [1] ✓ Resolved
[3] depends on [2] ✓ Resolved
[4] depends on [3] ✓ Resolved
```

## Final Output Format

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
- src/auth/middleware.ts (created)
- src/auth/types.ts (created)
- tests/auth.test.ts (created)
- README.md (updated)

**Notes:**
- [important observations]
- [recommendations]

**Verification:**
- [ ] Tests passing
- [ ] Build successful
- [ ] No regressions

══════════════════════════════════════════════
```

## Partial Success Handling

When N-1 of N workstreams succeed:

```
PARTIAL COMPLETION
══════════════════════════════════════════════

**Completed:** [N-1]/[N] workstreams

**Successful:**
1. [Workstream 1] - ✓
2. [Workstream 2] - ✓

**Failed:**
3. [Workstream 3] - ✗
   Error: [description]
   Impact: [what's affected]

**Options:**
1. Retry failed workstream
2. Delegate to auto-ralph for iteration
3. Accept partial results
4. Manual intervention

══════════════════════════════════════════════
```

## Critical Failure Handling

When a blocking workstream fails:

```
CRITICAL FAILURE
══════════════════════════════════════════════

**Failed workstream:** [N]
**Error:** [description]

**Blocked workstreams:**
- [M] - depends on [N]
- [O] - depends on [M]

**Completed before failure:**
- [1] - ✓
- [2] - ✓

**Recovery options:**
1. Fix [N] and resume
2. Provide manual context for [M], [O]
3. Rollback completed work
4. Cancel orchestration

══════════════════════════════════════════════
```

## Quality Metrics

Track and report at end:

| Metric | Description |
|--------|-------------|
| Total time | Wall clock from start to finish |
| Agent utilization | How many agents ran in parallel |
| Parallel efficiency | Actual vs. theoretical speedup |
| Success rate | Completed / Total workstreams |
| Retry count | How many retries needed |

```
METRICS
─────────────────
Total time:        15m 42s
Sequential time:   28m 15s (estimated)
Parallel speedup:  1.8x
Success rate:      5/5 (100%)
Retries:           0
```

## Recommendations Section

Based on orchestration results:

```
RECOMMENDATIONS
─────────────────
1. [Observation] → [Suggestion]
2. [Pattern noticed] → [Future consideration]
3. [Issue found] → [Follow-up action]
```

Example:
```
RECOMMENDATIONS
─────────────────
1. Auth module lacks tests → Consider adding unit tests
2. Similar pattern in 3 files → Consider abstracting
3. Deprecated API used → Schedule migration
```

## Handoff Notes

If follow-up work needed:

```
FOLLOW-UP REQUIRED
─────────────────
[ ] Run full test suite
[ ] Update deployment config
[ ] Notify team of API changes
[ ] Schedule code review
```

## Integration with auto-ralph

If workstream marked as `[RALPH-CANDIDATE]`:

```
RALPH-CANDIDATE DETECTED
─────────────────
Workstream [3] may benefit from Ralph Loop:
- Clear success criteria: tests pass
- Iterative nature: fix-test cycle

Consider: /ralph-loop for follow-up iteration
```
