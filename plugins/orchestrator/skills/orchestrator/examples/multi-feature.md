# Example: Multi-Feature Implementation

Orchestrating implementation of auth, logging, and rate limiting.

## Input

```
User: "Add user authentication with JWT, logging middleware, and rate limiting to the API"
```

## Orchestrator Analysis

```
(ORCHESTRATOR) ════════════════════════════════════════
  Mode: auto
  Complexity: COMPLEX (4 points)
  Workstreams detected: 8
════════════════════════════════════════════════════════
```

### Complexity Scoring

| Indicator | Points |
|-----------|--------|
| Multiple deliverables (3 features) | +1 |
| Cross-cutting concerns (middleware) | +1 |
| >500 lines estimate | +1 |
| Multiple domains (auth, logging, rate-limit) | +1 |
| **Total** | **4 = COMPLEX** |

## Decomposition

```
WORKSTREAM MAP
══════════════════════════════════════

Phase 1 (Parallel - Research):
  [1] Explore: Find existing auth patterns
      Agent: Explore | Est: 1min
      Prompt: "Find authentication patterns, JWT usage, middleware structure"

  [2] Explore: Check current middleware structure
      Agent: Explore | Est: 1min
      Prompt: "Map existing middleware, request/response flow"

  [3] Explore: Find rate limiting libraries
      Agent: Explore | Est: 30s
      Prompt: "Check package.json for rate-limit libs, find usage patterns"

Phase 2 (Sequential - Core Implementation):
  [4] general-purpose: Implement JWT authentication
      Agent: general-purpose | Est: 15min
      Depends: [1], [2]
      Prompt: "Implement JWT auth middleware using patterns from [1], structure from [2]"

Phase 3 (Parallel - Secondary Features):
  [5] general-purpose: Implement logging middleware
      Agent: general-purpose | Est: 8min
      Depends: [2]
      Prompt: "Add request logging middleware following structure from [2]"

  [6] general-purpose: Implement rate limiting
      Agent: general-purpose | Est: 10min
      Depends: [2], [3]
      Prompt: "Add rate limiting using libs from [3], structure from [2]"

Phase 4 (Parallel - Verification):
  [7] general-purpose: Write integration tests
      Agent: general-purpose | Est: 5min
      Depends: [4], [5], [6]
      Prompt: "Write tests for auth, logging, and rate limiting"

  [8] general-purpose: Update documentation
      Agent: general-purpose | Est: 3min
      Depends: [4], [5], [6]
      Prompt: "Update README with middleware usage and configuration"

══════════════════════════════════════
```

## Execution Log

### Phase 1 Execution

```
EXECUTING PHASE 1 (PARALLEL)
────────────────────────────
[1] Launching Explore: Auth patterns...
[2] Launching Explore: Middleware structure...
[3] Launching Explore: Rate limit libs...

[3] ✓ Complete (28s)
    Found: express-rate-limit in devDependencies
    Pattern: app.use(rateLimit({ windowMs, max }))

[1] ✓ Complete (45s)
    Found: src/middleware/sample-auth.ts
    Pattern: Bearer token validation, req.user injection
    Related: src/types/user.ts

[2] ✓ Complete (52s)
    Found: Middleware chain in src/app.ts
    Pattern: app.use() calls, error handler last
    Structure: cors -> json -> routes -> error
────────────────────────────
```

### Phase 2 Execution

```
EXECUTING PHASE 2 (SEQUENTIAL)
────────────────────────────
[4] Launching general-purpose: JWT Authentication
    Context provided:
    - Auth pattern from [1]: Bearer token, req.user injection
    - Middleware structure from [2]: Insert after json, before routes

[4] ✓ Complete (12m 15s)
    Created: src/middleware/auth.ts
    Created: src/types/jwt.ts
    Updated: src/app.ts (middleware registration)
────────────────────────────
```

### Phase 3 Execution

```
EXECUTING PHASE 3 (PARALLEL)
────────────────────────────
[5] Launching general-purpose: Logging middleware...
[6] Launching general-purpose: Rate limiting...

[5] ✓ Complete (6m 45s)
    Created: src/middleware/logger.ts
    Updated: src/app.ts

[6] ✓ Complete (8m 30s)
    Created: src/middleware/rateLimiter.ts
    Updated: src/app.ts
    Updated: package.json (express-rate-limit moved to dependencies)
────────────────────────────
```

### Phase 4 Execution

```
EXECUTING PHASE 4 (PARALLEL)
────────────────────────────
[7] Launching general-purpose: Integration tests...
[8] Launching general-purpose: Documentation...

[7] ✓ Complete (4m 20s)
    Created: tests/middleware/auth.test.ts
    Created: tests/middleware/logger.test.ts
    Created: tests/middleware/rateLimiter.test.ts

[8] ✓ Complete (2m 15s)
    Updated: README.md (Middleware section)
    Created: docs/middleware.md
────────────────────────────
```

## Final Synthesis

```
ORCHESTRATION COMPLETE
══════════════════════════════════════════════
Workstreams: 8/8 complete
Total time: 28m 15s
Phases: 4

DELIVERABLES:
1. [Auth] JWT authentication - src/middleware/auth.ts
2. [Logging] Request logger - src/middleware/logger.ts
3. [Rate Limit] Rate limiter - src/middleware/rateLimiter.ts
4. [Types] JWT types - src/types/jwt.ts
5. [Tests] Integration tests - tests/middleware/
6. [Docs] Middleware docs - docs/middleware.md, README.md

FILES MODIFIED:
- src/middleware/auth.ts (created)
- src/middleware/logger.ts (created)
- src/middleware/rateLimiter.ts (created)
- src/types/jwt.ts (created)
- src/app.ts (updated)
- package.json (updated)
- tests/middleware/*.test.ts (created)
- docs/middleware.md (created)
- README.md (updated)

NOTES:
- Used existing middleware pattern from sample-auth.ts
- Rate limiting uses express-rate-limit (already in devDeps, moved to deps)
- All 15 tests passing

METRICS:
- Total time: 28m 15s
- Sequential estimate: 45m
- Parallel speedup: 1.6x
- Success rate: 100%

══════════════════════════════════════════════
```
