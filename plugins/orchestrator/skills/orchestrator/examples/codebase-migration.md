# Example: Codebase Migration

Orchestrating migration from JavaScript to TypeScript.

## Input

```
User: "Migrate the user service from JavaScript to TypeScript"
```

## Orchestrator Analysis

```
(ORCHESTRATOR) ════════════════════════════════════════
  Mode: auto
  Complexity: EPIC (6 points)
  Workstreams detected: 7
════════════════════════════════════════════════════════
```

### Complexity Scoring

| Indicator | Points |
|-----------|--------|
| Multiple deliverables (types, configs, migrations) | +1 |
| Cross-cutting concerns (all JS files) | +1 |
| >500 lines affected | +1 |
| Multiple file types (.js → .ts) | +1 |
| Integration requirements (build, tests) | +1 |
| Risk (breaking changes possible) | +1 |
| **Total** | **6 = EPIC** |

## Decomposition

```
WORKSTREAM MAP
══════════════════════════════════════

Phase 1 (Sequential - Analysis):
  [1] Explore: Map user service structure
      Agent: Explore | Est: 2min
      Prompt: "Map all JS files in user service, dependencies, exports"

Phase 2 (Sequential - Planning):
  [2] Plan: Design migration strategy
      Agent: Plan | Est: 5min
      Depends: [1]
      Prompt: "Design TypeScript migration for user service:
               - Type definitions needed
               - Conversion order (leaf → root)
               - Potential breaking changes
               - Test strategy"

Phase 3 (Sequential - Setup):
  [3] general-purpose: Configure TypeScript
      Agent: general-purpose | Est: 3min
      Depends: [2]
      Prompt: "Add/update tsconfig.json for user service migration"

Phase 4 (Parallel - Core Migration):
  [4] general-purpose: Migrate models
      Agent: general-purpose | Est: 10min
      Depends: [3]
      Prompt: "Convert user models to TypeScript with proper types"

  [5] general-purpose: Migrate utilities
      Agent: general-purpose | Est: 8min
      Depends: [3]
      Prompt: "Convert user service utilities to TypeScript"

Phase 5 (Sequential - Integration):
  [6] general-purpose: Migrate main service
      Agent: general-purpose | Est: 15min
      Depends: [4], [5]
      Prompt: "Convert main user service file, importing TS modules"

Phase 6 (Sequential - Verification):
  [7] general-purpose: Update tests and verify
      Agent: general-purpose | Est: 10min
      Depends: [6]
      Prompt: "Update tests for TypeScript, run full test suite"

══════════════════════════════════════
```

## Execution Log

### Phase 1: Analysis

```
EXECUTING PHASE 1 (SEQUENTIAL)
────────────────────────────
[1] Launching Explore: Map user service...

[1] ✓ Complete (1m 45s)
    Structure found:
    - src/services/user/
      ├── index.js (main service, 450 lines)
      ├── models/
      │   ├── user.js (User model, 120 lines)
      │   └── profile.js (Profile model, 80 lines)
      ├── utils/
      │   ├── validation.js (60 lines)
      │   └── transform.js (40 lines)
      └── __tests__/
          └── user.test.js (200 lines)

    Dependencies: mongoose, joi, lodash
    Exports: UserService class, createUser, updateUser, deleteUser
────────────────────────────
```

### Phase 2: Planning

```
EXECUTING PHASE 2 (SEQUENTIAL)
────────────────────────────
[2] Launching Plan: Design migration strategy...

[2] ✓ Complete (4m 30s)
    Strategy:
    1. Add tsconfig.json with strict mode
    2. Create types/user.ts with interfaces
    3. Migrate leaf files first (utils/, models/)
    4. Migrate main service last
    5. Update imports progressively

    Type definitions needed:
    - IUser, IProfile interfaces
    - ValidationResult type
    - ServiceResponse generic

    Risk areas:
    - Mongoose typing (use @types/mongoose)
    - Joi schema inference (consider zod)
────────────────────────────
```

### Phase 3-6: Migration

```
EXECUTING PHASE 3 (SEQUENTIAL)
────────────────────────────
[3] ✓ Complete (2m 15s) - tsconfig.json configured

EXECUTING PHASE 4 (PARALLEL)
────────────────────────────
[4] ✓ Complete (8m 45s) - Models migrated
[5] ✓ Complete (6m 30s) - Utils migrated

EXECUTING PHASE 5 (SEQUENTIAL)
────────────────────────────
[6] ✓ Complete (12m 20s) - Main service migrated

EXECUTING PHASE 6 (SEQUENTIAL)
────────────────────────────
[7] ✓ Complete (8m 15s) - Tests updated, all passing
────────────────────────────
```

## Final Synthesis

```
ORCHESTRATION COMPLETE
══════════════════════════════════════════════
Workstreams: 7/7 complete
Total time: 44m 20s
Phases: 6

DELIVERABLES:
1. [Config] TypeScript configuration - tsconfig.json
2. [Types] Type definitions - src/services/user/types/
3. [Models] TypeScript models - src/services/user/models/*.ts
4. [Utils] TypeScript utilities - src/services/user/utils/*.ts
5. [Service] Main service - src/services/user/index.ts
6. [Tests] Updated tests - src/services/user/__tests__/*.ts

FILES CHANGED:
- tsconfig.json (updated)
- src/services/user/types/user.ts (created)
- src/services/user/types/index.ts (created)
- src/services/user/models/user.ts (renamed, converted)
- src/services/user/models/profile.ts (renamed, converted)
- src/services/user/utils/validation.ts (renamed, converted)
- src/services/user/utils/transform.ts (renamed, converted)
- src/services/user/index.ts (renamed, converted)
- src/services/user/__tests__/user.test.ts (renamed, updated)

FILES DELETED:
- src/services/user/**/*.js (9 files)

NOTES:
- Strict TypeScript mode enabled
- All 24 tests passing
- No runtime behavior changes
- Type coverage: 100%

RECOMMENDATIONS:
- Consider migrating other services using same pattern
- Add @types/mongoose to dependencies
- Run tsc --noEmit in CI pipeline

══════════════════════════════════════════════
```
