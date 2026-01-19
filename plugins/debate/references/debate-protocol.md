# Debate Protocol Reference

## The Hybrid Protocol

This plugin uses a hybrid protocol: **parallel first, sequential if needed**.

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEBATE FLOW                                 │
└─────────────────────────────────────────────────────────────────┘

Phase 0: PREFLIGHT
    │
    ├── Check /tmp/debate-available-challengers
    ├── If empty → ABORT (run /debate:doctor)
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
    ├── Launch ALL challengers simultaneously      │
    │   ├── gemini -p "..." --yolo                │
    │   ├── codex -p "..." --full-auto            │
    │   └── qwen -p "..." --yolo                  │
    ├── Collect JSON responses                     │
    └── Parse verdicts                             │
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

### Skepticism Rule

If a challenger agrees in round 1, ask:
- Did they engage seriously or rubber-stamp?
- Is the agreement substantive?

If suspicious, treat as `partial` and continue.

---

## Round Limits

| Setting | Default | Notes |
|---------|---------|-------|
| MAX_ROUNDS | 5 | Configurable in settings |
| TIMEOUT_PER_CLI | 120s | Per CLI invocation |
| MIN_CHALLENGERS | 1 | Hard requirement, not configurable |

After MAX_ROUNDS without consensus → Assumption extraction → Tradeoff document

---

## Position Evolution Tracking

Track every change to Claude's position:

```
Position History:
- v1 (opening): [position]
- v2 (after round 1): [position] — Changed because: [reason from challenger]
- v3 (after round 2): [position] — Changed because: [reason from challenger]
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
| All CLIs fail | Abort debate with error |

### Minimum Viability

A debate can continue if:
- At least 1 challenger responds successfully
- Claude can form and defend a position

A debate must abort if:
- 0 challengers respond
- Repeated failures prevent any confrontation

---

## Output Formats

### Consensus Output

```markdown
## DEBATE OUTCOME: CONSENSUS

**Final position:** [evolved position]
**Confidence:** HIGH
**Rounds to consensus:** N
**What changed:** [list of accepted critiques]
```

### No-Consensus Output

```markdown
## DEBATE OUTCOME: TRADEOFF

**Final position:** [Claude's position, contested]
**Confidence:** MEDIUM
**Rounds:** MAX (no consensus)
**Core disagreement:** [description]
**Assumptions exposed:** [table]
```

---

## Academic Foundation

This protocol is inspired by:

- **Irving et al. (2018)** - "AI safety via debate" - The foundational paper on AI debate for scalable oversight
- **Adversarial-spec plugin** - Multi-LLM consensus for specifications
- **Scalable oversight research** - Debate as a verification mechanism

Key insight from Irving: "It is easier to judge who wins at chess than to play chess at a grandmaster level."

The debate is a **verification mechanism**, not a generation mechanism. External models verify Claude's reasoning.
