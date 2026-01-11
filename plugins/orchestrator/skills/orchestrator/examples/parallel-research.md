# Example: Parallel Research

Using multiple Explore agents to gather information quickly.

## Input

```
User: "Understand how the authentication system works across the codebase"
```

## Orchestrator Analysis

```
(ORCHESTRATOR) ════════════════════════════════════════
  Mode: auto
  Complexity: MODERATE (3 points)
  Workstreams detected: 4
════════════════════════════════════════════════════════
```

### Complexity Scoring

| Indicator | Points |
|-----------|--------|
| Multiple aspects (frontend, backend, middleware) | +1 |
| Cross-cutting (spans multiple modules) | +1 |
| Research scope (understand, not modify) | +1 |
| **Total** | **3 = MODERATE** |

## Decomposition

```
WORKSTREAM MAP
══════════════════════════════════════

Phase 1 (Parallel - Research):
  [1] Explore: Backend auth implementation
      Agent: Explore | Est: 2min
      Prompt: "Find backend authentication:
               - Auth middleware
               - Token validation
               - Session handling
               - User model auth fields"

  [2] Explore: Frontend auth flow
      Agent: Explore | Est: 2min
      Prompt: "Find frontend authentication:
               - Login components
               - Auth context/store
               - Token storage
               - Protected routes"

  [3] Explore: Auth configuration
      Agent: Explore | Est: 1min
      Prompt: "Find auth configuration:
               - Environment variables
               - JWT secrets
               - Token expiration
               - OAuth settings"

  [4] Explore: Auth-related tests
      Agent: Explore | Est: 1min
      Prompt: "Find authentication tests:
               - Unit tests
               - Integration tests
               - E2E auth flows
               - Test utilities/mocks"

══════════════════════════════════════
```

## Execution Log

```
EXECUTING PHASE 1 (PARALLEL)
────────────────────────────
[1] Launching Explore: Backend auth...
[2] Launching Explore: Frontend auth...
[3] Launching Explore: Auth config...
[4] Launching Explore: Auth tests...

[3] ✓ Complete (42s)
[4] ✓ Complete (55s)
[2] ✓ Complete (1m 30s)
[1] ✓ Complete (1m 45s)
────────────────────────────
```

## Results Synthesis

```
ORCHESTRATION COMPLETE
══════════════════════════════════════════════
Workstreams: 4/4 complete
Total time: 1m 45s (parallel)
Sequential estimate: 6m 30s
Parallel speedup: 3.7x
Phases: 1

AUTHENTICATION SYSTEM OVERVIEW
══════════════════════════════════════════════

## Backend Auth [1]

**Location:** src/middleware/auth/
**Pattern:** JWT-based authentication

Key files:
- src/middleware/auth/jwt.ts - Token validation
- src/middleware/auth/passport.ts - Strategy configuration
- src/models/user.ts - User model with password hash

Flow:
1. Request → jwt.ts middleware
2. Extract Bearer token from header
3. Verify with passport-jwt strategy
4. Attach user to req.user
5. Continue to route handler

Protected routes use: `@Authenticated()` decorator

## Frontend Auth [2]

**Location:** src/app/auth/
**Pattern:** React Context + localStorage

Key files:
- src/app/auth/AuthContext.tsx - Auth state provider
- src/app/auth/LoginForm.tsx - Login UI
- src/app/auth/ProtectedRoute.tsx - Route guard
- src/app/hooks/useAuth.ts - Auth hook

Flow:
1. User submits credentials
2. POST /api/auth/login
3. Store JWT in localStorage
4. Update AuthContext
5. Redirect to dashboard

## Configuration [3]

**Location:** .env, src/config/auth.ts

Variables:
- JWT_SECRET - Token signing secret
- JWT_EXPIRES_IN - Token lifetime (24h default)
- REFRESH_TOKEN_EXPIRES - Refresh lifetime (7d)
- OAUTH_GOOGLE_CLIENT_ID - Google OAuth

Security notes:
- Secrets loaded from .env (not committed)
- Refresh token rotation enabled
- CORS configured for specific origins

## Tests [4]

**Location:** tests/auth/, cypress/e2e/auth/

Coverage:
- Unit: 45 tests (jwt.test.ts, user.test.ts)
- Integration: 12 tests (auth-flow.test.ts)
- E2E: 8 tests (login.cy.ts, register.cy.ts)

Test utilities:
- tests/utils/auth.ts - createMockUser, generateTestToken
- tests/fixtures/users.json - Test user data

══════════════════════════════════════════════

ARCHITECTURE DIAGRAM
────────────────────
Frontend                     Backend
────────────────────         ────────────────────
LoginForm.tsx                POST /api/auth/login
     │                            │
     ▼                            ▼
AuthContext.tsx ──────────► jwt.ts middleware
     │                            │
     ▼                            ▼
localStorage ◄─── JWT ───► passport-jwt verify
     │                            │
     ▼                            ▼
ProtectedRoute.tsx           Route handler
                                  │
                                  ▼
                              User model

══════════════════════════════════════════════

RECOMMENDATIONS
────────────────────
1. Consider adding rate limiting to login endpoint
2. Refresh token rotation is good, consider adding jti blacklist
3. E2E tests cover happy path, add failure scenarios
4. Document auth flow in README

══════════════════════════════════════════════
```

## Usage Notes

This example shows:
- **Pure research** - no file modifications needed
- **Maximum parallelization** - all 4 agents run simultaneously
- **Fast execution** - 1m 45s vs 6m 30s sequential
- **Comprehensive synthesis** - combines findings into unified view

Best for:
- Understanding unfamiliar codebases
- Pre-implementation research
- Architecture documentation
- Onboarding new team members
