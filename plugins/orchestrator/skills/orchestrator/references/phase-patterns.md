# Phase Execution Patterns

Common patterns for organizing workstreams into execution phases.

## Research-First Pattern

**Best for:** Unknown codebases, new features, unfamiliar domains

```
Phase 1 (Parallel - Research):
  [1] Explore: Find existing patterns
  [2] Explore: Map dependencies
  [3] Explore: Check test structure

Phase 2 (Sequential - Implementation):
  [4] general-purpose: Implement feature
      Context: patterns from [1], deps from [2], test style from [3]

Phase 3 (Parallel - Verification):
  [5] general-purpose: Write tests
  [6] general-purpose: Update docs
```

**Rationale:**
- Front-load context gathering
- Implementation informed by research
- Parallel verification at end

## Implement-Then-Verify Pattern

**Best for:** Known codebases, clear requirements, simple features

```
Phase 1 (Sequential - Implementation):
  [1] general-purpose: Implement feature

Phase 2 (Parallel - Verification):
  [2] general-purpose: Write tests
  [3] general-purpose: Update docs
  [4] Explore: Verify no regressions
```

**Rationale:**
- Fast to first implementation
- Parallel verification tasks
- Good for confident changes

## Deep-Analysis Pattern

**Best for:** Architecture decisions, risky changes, technical debt

```
Phase 1 (Sequential - Analysis):
  [1] Plan: Analyze approaches and trade-offs

Phase 2 (Parallel - Validation):
  [2] Explore: Verify approach A feasibility
  [3] Explore: Verify approach B feasibility

Phase 3 (Sequential - Implementation):
  [4] general-purpose: Implement chosen approach
      Context: decision from [1], validation from [2,3]
```

**Rationale:**
- Thoughtful planning first
- Validate assumptions
- Informed implementation

## Distributed Modification Pattern

**Best for:** Cross-cutting changes, bulk updates, migrations

```
Phase 1 (Sequential - Research):
  [1] Explore: Map all affected locations

Phase 2 (Parallel - Implementation):
  [2] general-purpose: Update module A
  [3] general-purpose: Update module B
  [4] general-purpose: Update module C
      (All depend on [1] for location info)

Phase 3 (Sequential - Integration):
  [5] general-purpose: Integration tests
```

**Rationale:**
- Single source of truth for locations
- Parallel independent modifications
- Final integration verification

## Progressive Enhancement Pattern

**Best for:** Incremental features, backward-compatible changes

```
Phase 1 (Sequential - Base):
  [1] general-purpose: Implement minimal version

Phase 2 (Parallel - Enhancements):
  [2] general-purpose: Add enhancement A
  [3] general-purpose: Add enhancement B
      (Both depend on [1])

Phase 3 (Sequential - Polish):
  [4] general-purpose: Integration and cleanup
```

**Rationale:**
- Working base first
- Parallel feature additions
- Final integration

## Context Accumulation

Each phase passes context forward to dependent phases.

### What to Pass

**From Explore phases:**
- File paths discovered
- Patterns identified
- Summary of findings
- Relevant code snippets

**From Plan phases:**
- Decisions made
- Rationale for choices
- Constraints identified
- Recommended approach

**From general-purpose phases:**
- Files modified
- Functions created
- Tests written
- API changes

### Context Format

```
## Context from Phase N

### Workstream [1]: Pattern Research
**Summary:** Found auth implementation in src/auth/
**Key files:**
- src/auth/middleware.ts - JWT validation
- src/auth/types.ts - User types
**Pattern:** Uses decorator-based guards

### Workstream [2]: Dependency Check
**Summary:** No breaking changes needed
**Dependencies:**
- express: ^4.18.0 (compatible)
- jsonwebtoken: ^9.0.0 (already installed)
```

## Execution Progress Display

```
EXECUTING PHASE 1 (PARALLEL)
────────────────────────────
[1] Explore: Pattern research    ... ⏳
[2] Explore: Dependency check    ... ⏳

[1] ✓ Complete (45s)
[2] ✓ Complete (32s)

EXECUTING PHASE 2 (SEQUENTIAL)
────────────────────────────
[3] general-purpose: Implementation
    Context from [1], [2] provided

[3] ✓ Complete (8m 23s)

EXECUTING PHASE 3 (PARALLEL)
────────────────────────────
[4] general-purpose: Tests       ... ⏳
[5] general-purpose: Docs        ... ⏳

[4] ✓ Complete (3m 12s)
[5] ✓ Complete (1m 45s)
────────────────────────────
```

## Failure Handling by Phase

### Phase 1 Failure (Research)
- Low impact - retry or skip
- Provide manual context if needed

### Mid-Phase Failure (Implementation)
- Higher impact - dependent phases blocked
- Options: retry, delegate to auto-ralph, manual fix

### Final Phase Failure (Verification)
- Implementation complete but unverified
- Options: retry tests, manual verification, accept partial
