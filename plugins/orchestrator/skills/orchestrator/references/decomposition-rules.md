# Task Decomposition Rules

How to break complex tasks into orchestrable workstreams.

## Core Principles

1. **Atomicity**: Each workstream should do ONE thing
2. **Independence**: Parallel workstreams must not conflict
3. **Completeness**: All workstreams together fulfill the original task
4. **Efficiency**: Minimize total execution time through parallelization

## Pattern Recognition

### Multi-Feature Pattern

**Keywords:** "and", "also", "plus", "as well as", "along with"
**Structure:** Feature1 AND Feature2 AND Feature3
**Strategy:** Parallel if independent, sequential if dependent

**Example:**
```
Input: "Add authentication AND logging AND rate limiting"

Decomposition:
Phase 1 (Parallel - Research):
  [1] Explore: Find auth patterns
  [2] Explore: Find logging patterns
  [3] Explore: Find rate limiting libs

Phase 2 (Parallel - Implementation):
  [4] general-purpose: Implement auth (depends: 1)
  [5] general-purpose: Implement logging (depends: 2)
  [6] general-purpose: Implement rate limiting (depends: 3)
```

### Layered Pattern

**Keywords:** "then", "after", "once", "when done", "first...then"
**Structure:** Layer1 -> Layer2 -> Layer3
**Strategy:** Strictly sequential

**Example:**
```
Input: "Create database schema THEN implement API THEN add tests"

Decomposition:
Phase 1: [1] general-purpose: Create schema
Phase 2: [2] general-purpose: Implement API (depends: 1)
Phase 3: [3] general-purpose: Add tests (depends: 2)
```

### Cross-Cutting Pattern

**Keywords:** "across", "throughout", "everywhere", "all files"
**Structure:** Same change affects multiple modules
**Strategy:** Explore first, then parallel implementation per module

**Example:**
```
Input: "Update error handling across all services"

Decomposition:
Phase 1: [1] Explore: Map all services and error handling patterns
Phase 2 (Parallel):
  [2] general-purpose: Update service A (depends: 1)
  [3] general-purpose: Update service B (depends: 1)
  [4] general-purpose: Update service C (depends: 1)
```

### Research-Then-Implement Pattern

**Keywords:** "understand", "learn", "figure out", then action words
**Structure:** Research -> Design -> Implement
**Strategy:** Sequential with increasing commitment

**Example:**
```
Input: "Figure out how auth works and fix the login bug"

Decomposition:
Phase 1: [1] Explore: Map auth system
Phase 2: [2] Plan: Design fix approach (depends: 1)
Phase 3: [3] general-purpose: Implement fix (depends: 2)
```

### Migration Pattern

**Keywords:** "migrate", "upgrade", "convert", "move from X to Y"
**Structure:** Research -> Plan -> Backup -> Execute -> Verify
**Strategy:** Sequential with checkpoints

**Example:**
```
Input: "Migrate from REST to GraphQL"

Decomposition:
Phase 1: [1] Explore: Map current REST endpoints
Phase 2: [2] Plan: Design GraphQL schema (depends: 1)
Phase 3: [3] general-purpose: Implement GraphQL (depends: 2)
Phase 4: [4] general-purpose: Update clients (depends: 3)
Phase 5: [5] general-purpose: Add tests (depends: 4)
```

### Review Pattern

**Keywords:** "audit", "review", "check", multiple concerns
**Structure:** Parallel reviews of different aspects
**Strategy:** All Explore agents in parallel

**Example:**
```
Input: "Review the codebase for security, performance, and style issues"

Decomposition:
Phase 1 (Parallel):
  [1] Explore: Security audit
  [2] Explore: Performance analysis
  [3] Explore: Style/lint check
```

## Workstream Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| Minimum | 2 | Otherwise no orchestration needed |
| Optimal | 3-5 | Best balance of parallelism and coherence |
| Maximum | 7 | Human cognitive limit |

## Dependency Detection

Check for these dependency types:

### Data Dependencies
Output of A is input to B.
```
[1] Create user model
[2] Create user API (needs model from 1)
```

### State Dependencies
A modifies what B reads.
```
[1] Update config file
[2] Run build (reads config)
```

### Order Dependencies
A must logically precede B.
```
[1] Write code
[2] Write tests (needs code to exist)
```

## Dependency Rules

1. **If no dependencies detected:** PARALLEL
2. **If data dependency:** SEQUENTIAL within dependency chain
3. **If state dependency:** SEQUENTIAL (avoid conflicts)
4. **If order dependency:** SEQUENTIAL

## Conflict Detection

Never parallelize workstreams that:

1. **Modify the same file**
   ```
   # BAD - will conflict
   [1] Edit src/app.ts (add feature A)
   [2] Edit src/app.ts (add feature B)
   ```

2. **Have overlapping scope**
   ```
   # BAD - overlapping
   [1] Refactor auth module
   [2] Fix auth login bug
   ```

3. **Depend on each other's output**
   ```
   # BAD - dependency
   [1] Create types
   [2] Use types (needs 1 to complete)
   ```

## Decomposition Checklist

Before finalizing workstream map:

- [ ] Each workstream is atomic (single responsibility)
- [ ] Parallel workstreams are truly independent
- [ ] Dependencies are correctly identified
- [ ] No file conflicts in parallel workstreams
- [ ] Total workstreams <= 7
- [ ] All original requirements covered
