# Debate Protocol Reference

## The Hybrid Protocol

This plugin uses a hybrid protocol: **parallel first, sequential if needed**.

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEBATE FLOW                                 │
└─────────────────────────────────────────────────────────────────┘

Phase 0: WORKSPACE SETUP & PERSONA GENERATION  ← NEW
    │
    ├── Create workspace directory: ./debates/NNN-topic-slug/
    ├── Detect topic domain
    ├── Invoke debate-persona-generator skill
    ├── Generate THREE DISTINCT expert personas:
    │   ├── workspace/GEMINI.md  (Architect perspective)
    │   ├── workspace/AGENTS.md  (Operator perspective)
    │   └── workspace/QWEN.md    (Adversary perspective)
    └── Verify all context files exist
          │
          ▼
Phase 0.5: PREFLIGHT
    │
    ├── Check /tmp/debate-available-challengers
    ├── If empty → ABORT (run /debate:doctor)
    ├── Verify CLIs can read context files (test invocation)
    └── If available → Continue
          │
          ▼
Phase 1: CLAUDE'S OPENING
    │
    ├── Analyze topic
    ├── Form position with reasoning
    ├── State confidence (HIGH/MED/LOW)
    ├── Acknowledge weaknesses
    └── List assumptions
          │
          ▼
Phase 2: PARALLEL CHALLENGE ←─────────────────────┐
    │                                              │
    ├── Launch ALL challengers FROM WORKSPACE:     │
    │   ├── cd workspace && gemini "..." --yolo   │
    │   ├── cd workspace && codex exec "..."      │
    │   └── cd workspace && qwen -p "..." --yolo  │
    │                                              │
    │   Each CLI reads its context file:           │
    │   ├── Gemini reads GEMINI.md (Architect)    │
    │   ├── Codex reads AGENTS.md (Operator)      │
    │   └── Qwen reads QWEN.md (Adversary)        │
    │                                              │
    ├── Collect JSON responses                     │
    └── Parse verdicts (expect DIFFERENT angles)   │
          │                                        │
          ▼                                        │
Phase 3: CONSENSUS CHECK                           │
    │                                              │
    ├── All AGREE? ────────────────────────────────┼──→ FAST EXIT
    ├── All PARTIAL (minor)? ──────────────────────┼──→ FAST EXIT
    └── Any DISAGREE (strong)? ────────────────────┘
          │
          ▼
Phase 4: CLAUDE RESPONDS (Confrontation)
    │
    ├── For each disagreement:
    │   ├── ACCEPT → Update position, explain
    │   ├── PARTIAL → Accept part, explain limit
    │   └── REJECT → Explain why wrong
    └── Output: Position v(N+1)
          │
          ▼
Phase 5: CHALLENGER REBUTTAL
    │
    ├── Send Claude's response to dissenters
    ├── CLIs still run FROM WORKSPACE (same personas)
    ├── Ask: ACCEPT / MAINTAIN / ESCALATE
    └── Collect responses
          │
          ▼
Phase 6: ITERATION CHECK
    │
    ├── All resolved? ────────────────────────────→ CONSENSUS (Phase 8)
    ├── Round < MAX_ROUNDS? ──────────────────────→ Back to Phase 4
    └── Round = MAX_ROUNDS? ──────────────────────→ NO CONSENSUS (Phase 7)
          │
          ▼
Phase 7: ASSUMPTION EXTRACTION
    │
    ├── Ask each party: WHY do you disagree?
    ├── What would make other position correct?
    ├── Extract core assumptions
    └── Map assumptions to positions
          │
          ▼
Phase 8: FINAL OUTPUT
    │
    ├── CONSENSUS: Final position + audit trail
    └── NO CONSENSUS: Tradeoff document + assumptions
```

---

## Phase 0: Persona Generation (NEW)

### Purpose

Generate **three distinct expert challengers** that critique from different angles. This is NOT three copies of the same challenger - each brings unique expertise.

### The Three Perspectives

| Context File | CLI | Perspective | Catches |
|--------------|-----|-------------|---------|
| `GEMINI.md` | Gemini | **Architect** | Scaling, complexity, design flaws |
| `AGENTS.md` | Codex | **Operator** | Maintenance, failure modes, debugging |
| `QWEN.md` | Qwen | **Adversary** | Security, edge cases, abuse scenarios |

### Generation Process

1. **Detect domain** from topic
2. **Invoke `debate-persona-generator` skill**
3. **Write three context files** to workspace
4. **Verify** each file contains distinct persona

### Workspace Structure

```
debates/
└── 001-redis-vs-memcached/
    ├── GEMINI.md          # Architect persona (for Gemini CLI)
    ├── AGENTS.md          # Operator persona (for Codex CLI)
    ├── QWEN.md            # Adversary persona (for Qwen CLI)
    ├── context.md         # Initial context
    ├── state.json         # Session state
    ├── transcript.md      # Combined record
    └── rounds/
        ├── r001_gemini.md
        ├── r001_codex.md
        ├── r001_qwen.md
        └── ...
```

### Context File Persistence

**CRITICAL:** Context files are written ONCE at debate start and remain UNCHANGED throughout all rounds.

- ✅ Personas stay consistent across rounds
- ✅ Each CLI re-reads its context file on each invocation (fresh process)
- ✅ Persona provides stable "expert identity"
- ❌ Do NOT modify context files mid-debate

---

## Consensus Rules

### Fast Exit Conditions

| Condition | Action |
|-----------|--------|
| All challengers return `verdict: "agree"` | Fast exit, high confidence |
| All challengers return `verdict: "partial"` with `objection_strength: "minor"` | Address briefly, fast exit |
| Unanimous agreement after round 1 | Be skeptical, but allow if substantive |

### Continue to Confrontation

| Condition | Action |
|-----------|--------|
| Any `verdict: "disagree"` | Confrontation required |
| Any `objection_strength: "strong"` | Confrontation required |
| Mixed verdicts (some agree, some disagree) | Confrontation required |

### Multi-Perspective Value

Because each challenger has a DIFFERENT expertise angle:
- Agreement from all three = strong signal (validated from multiple angles)
- Disagreement reveals which ASPECT has flaws (scaling? operations? security?)
- Partial consensus shows where position is solid vs. weak

### Skepticism Rule

If a challenger agrees in round 1, check:
- Did they engage from their specific expertise angle?
- Is the agreement substantive to their domain?

If suspicious, treat as `partial` and continue.

---

## Round Limits

| Setting | Default | Notes |
|---------|---------|-------|
| MAX_ROUNDS | 5 | Configurable in settings |
| TIMEOUT_PER_CLI | 120s | Per CLI invocation |
| MIN_CHALLENGERS | 1 | At least one must respond |

After MAX_ROUNDS without consensus → Assumption extraction → Tradeoff document

---

## Position Evolution Tracking

Track every change to Claude's position:

```
Position History:
- v1 (opening): [position]
- v2 (after round 1): [position]
  └── Changed because: Architect found scaling flaw
  └── Changed because: Operator identified observability gap
- v3 (after round 2): [position]
  └── Changed because: Adversary found trust boundary issue
- vN (final): [position]
```

This evolution is the audit trail that makes debates valuable.

---

## Error Handling

### CLI Failures

| Error | Handling |
|-------|----------|
| Timeout | Log, continue with other challengers |
| Auth failure | Log, continue with other challengers |
| Parse error | Wrap raw response, continue |
| Context file missing | Abort that challenger, log error |
| All CLIs fail | Abort debate with error |

### Minimum Viability

A debate can continue if:
- At least 1 challenger responds successfully
- Claude can form and defend a position

A debate must abort if:
- 0 challengers respond
- Workspace creation fails
- All context file writes fail

---

## Output Formats

### Consensus Output

```markdown
## DEBATE OUTCOME: CONSENSUS

**Final position:** [evolved position]
**Confidence:** HIGH
**Rounds to consensus:** N
**Perspectives validated:**
- ✅ Architect (Gemini): [summary of their validation]
- ✅ Operator (Codex): [summary of their validation]
- ✅ Adversary (Qwen): [summary of their validation]
**What changed:** [list of accepted critiques by perspective]
```

### No-Consensus Output

```markdown
## DEBATE OUTCOME: TRADEOFF

**Final position:** [Claude's position, contested]
**Confidence:** MEDIUM
**Rounds:** MAX (no consensus)

**Perspective Breakdown:**
- Architect (Gemini): [AGREE/DISAGREE] - [their concern]
- Operator (Codex): [AGREE/DISAGREE] - [their concern]
- Adversary (Qwen): [AGREE/DISAGREE] - [their concern]

**Core disagreement:** [which perspective couldn't be resolved]
**Assumptions exposed:** [table mapping assumptions to perspectives]
```

---

## Academic Foundation

This protocol is inspired by:

- **Irving et al. (2018)** - "AI safety via debate" - The foundational paper on AI debate for scalable oversight
- **ExpertPrompting (2023)** - LLM-generated detailed personas outperform simple role prompts
- **Jekyll & Hyde (2024)** - Ensembling persona and neutral perspectives improves reasoning by ~10%
- **Multi-agent debate research** - Diverse perspectives catch more flaws than homogeneous critics

Key insight: **Different expertise angles catch different flaws**. A security expert sees attack vectors an architect misses. An operator sees maintenance nightmares a security expert ignores.
