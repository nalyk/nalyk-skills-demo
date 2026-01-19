---
description: "Multi-model adversarial debate. Claude defends position against external CLI models. Usage: /debate <topic, question, or decision>"
argument-hint: "<topic to debate - question, decision, code, architecture, anything>"
allowed-tools: Bash, Task, Read, Write, Glob, Grep, TodoWrite
---

# Multi-Model Adversarial Debate

**TOPIC:** $ARGUMENTS

---

## PHASE 0: PREFLIGHT CHECK

### Check for available challengers

```bash
if [ -f /tmp/debate-available-challengers ]; then
    CHALLENGERS=$(cat /tmp/debate-available-challengers | tr '\n' ' ')
    COUNT=$(cat /tmp/debate-available-challengers | wc -l)
    echo "Available challengers: $CHALLENGERS"
    echo "Count: $COUNT"
else
    echo "No challenger cache found. Run /debate:doctor first."
    echo "COUNT: 0"
fi
```

### If no challengers available:

```
+================================================================+
|  DEBATE ABORTED: No external challengers available               |
+================================================================+
|                                                                  |
|  Claude debating itself provides no genuine diversity.           |
|                                                                  |
|  Run: /debate:doctor                                             |
|  Then install at least ONE external CLI.                         |
|                                                                  |
+================================================================+
```

**STOP HERE** if no challengers. Do not proceed.

### If challengers available:

Display activation banner:

```
(DEBATE) ════════════════════════════════════════════════════════
  Topic: [first 60 chars of $ARGUMENTS]
  Challengers: [list of available]
  Protocol: Hybrid (parallel challenge → sequential confrontation)
  Max rounds: 5
══════════════════════════════════════════════════════════════════
```

---

## PHASE 1: CLAUDE'S OPENING POSITION

Analyze the topic thoroughly. Form your position.

### Your opening must include:

1. **Position statement** - Clear, specific stance on the topic
2. **Reasoning** - Step-by-step logic for why you hold this position
3. **Confidence level** - HIGH / MEDIUM / LOW
4. **Acknowledged weaknesses** - What might be wrong with your position?
5. **Key assumptions** - What are you assuming to be true?

### Format:

```
## CLAUDE'S OPENING POSITION

**Topic:** [restate topic]

**My position:** [clear statement]

**Reasoning:**
1. [point 1]
2. [point 2]
3. [point 3]

**Confidence:** [HIGH/MEDIUM/LOW]

**Potential weaknesses I see:**
- [weakness 1]
- [weakness 2]

**My assumptions:**
- [assumption 1]
- [assumption 2]
```

---

## PHASE 2: PARALLEL CHALLENGE (Round 1)

Launch ALL available challengers simultaneously using Task tool.

For EACH challenger in `/tmp/debate-available-challengers`, spawn a Task:

### Challenger prompt template:

```
You are challenging another AI's position. Your job is to find flaws, not to agree.

## THE POSITION TO CHALLENGE

[INSERT CLAUDE'S OPENING POSITION FROM PHASE 1]

## YOUR TASK

1. What is WRONG with this position? Be specific, not vague.
2. What edge cases, failure modes, or risks are missed?
3. What assumptions are unstated or questionable?
4. What would YOU recommend instead?
5. Rate your objection: STRONG / MODERATE / MINOR

## REQUIRED RESPONSE FORMAT

{
  "verdict": "agree | partial | disagree",
  "critique": "Your specific objections - be concrete",
  "evidence": "Concrete example or scenario proving your point",
  "alternative": "What you recommend instead",
  "confidence": "high | medium | low",
  "objection_strength": "strong | moderate | minor",
  "assumptions_challenged": ["assumption 1", "assumption 2"]
}

IMPORTANT: If you agree too easily, you're not helping. Find problems.
If you truly agree after honest analysis, explain WHY the position is solid.
```

### CLI invocation:

For Gemini:
```bash
timeout 120 gemini "[PROMPT]" --yolo 2>/dev/null || echo '{"error":"gemini_timeout"}'
```

For Codex:
```bash
timeout 120 codex exec "[PROMPT]" --full-auto 2>/dev/null || echo '{"error":"codex_timeout"}'
```

For Qwen:
```bash
timeout 120 qwen -p "[PROMPT]" --yolo 2>/dev/null || echo '{"error":"qwen_timeout"}'
```

### Collect all critiques

Parse JSON responses. Handle errors gracefully - if a CLI fails, continue with others.

Display critiques received:

```
## CHALLENGER CRITIQUES (Round 1)

### Gemini says:
**Verdict:** [agree/partial/disagree]
**Critique:** [their objection]
**Evidence:** [their example]
**Alternative:** [their recommendation]
**Assumptions challenged:** [list]

### Codex says:
[same format]

### Qwen says:
[same format]
```

---

## PHASE 3: CONSENSUS CHECK

Evaluate the critiques:

| Challenger | Verdict | Objection Strength | Blocking? |
|------------|---------|-------------------|-----------|
| Gemini | [v] | [s] | [Y/N] |
| Codex | [v] | [s] | [Y/N] |
| Qwen | [v] | [s] | [Y/N] |

### CONSENSUS RULES:

- **All AGREE with high confidence** → FAST EXIT (Phase 8)
- **All PARTIAL with minor objections** → Address briefly, then FAST EXIT
- **Any DISAGREE with STRONG objection** → Continue to PHASE 4
- **Mixed verdicts** → Continue to PHASE 4

### Skepticism check:

If ANY challenger agreed in round 1, be skeptical. Ask yourself:
- Did they engage seriously or rubber-stamp?
- Is the agreement substantive or superficial?

If suspicious, treat as PARTIAL and continue to confrontation.

---

## PHASE 4: CLAUDE RESPONDS (Confrontation)

For EACH critique that requires response:

### Response format:

```
## CLAUDE'S RESPONSE TO [CHALLENGER]

**Their critique:** [summarize]

**My response:**

[ ] ACCEPT - This critique is valid. Here's how it changes my position:
    [explain what changed and why]

[ ] PARTIALLY ACCEPT - Valid point, but limited scope:
    [explain what you accept and what you don't]

[ ] REJECT - This critique is not valid because:
    [explain why they're wrong with specifics]

**Updated position (if changed):**
[state new position or "unchanged"]
```

### Track changes:

```
## POSITION EVOLUTION

**Original position:** [v1]

**After Round 1:**
- Accepted from Gemini: [what]
- Accepted from Codex: [what]
- Rejected from Qwen: [what, why]

**Current position (v2):** [updated]
```

---

## PHASE 5: CHALLENGER REBUTTAL

For each challenger that DISAGREED and whose critique was REJECTED:

Send follow-up via CLI:

```
Claude has responded to your critique.

YOUR ORIGINAL CRITIQUE:
[their critique]

CLAUDE'S RESPONSE:
[Claude's rejection/partial acceptance with reasoning]

YOUR OPTIONS:
1. ACCEPT - Claude's response addresses your concern
2. MAINTAIN - You still disagree, here's why: [explain]
3. ESCALATE - Claude missed the point entirely, let me clarify: [clarify]

Respond with your choice and reasoning.
```

### Collect rebuttals

Parse responses. If challenger:
- **ACCEPTS** → Issue resolved
- **MAINTAINS** → Log disagreement, continue
- **ESCALATES** → Return to PHASE 4 with clarified critique

---

## PHASE 6: ITERATION CHECK

```
Current round: [N]
Max rounds: 5

Unresolved disagreements: [count]
Challengers still objecting: [list]
```

### Decision:

- **All issues resolved** → PHASE 8 (Consensus)
- **Round < 5 AND unresolved issues** → Return to PHASE 4
- **Round = 5 AND unresolved issues** → PHASE 7 (No consensus)

---

## PHASE 7: ASSUMPTION EXTRACTION (No Consensus)

If debate reached max rounds without consensus:

### Ask each party:

```
The debate has reached maximum rounds without consensus.

YOUR FINAL POSITION: [their position]
CLAUDE'S FINAL POSITION: [Claude's position]

FINAL QUESTIONS:
1. WHY do you still disagree? What's the core issue?
2. What would have to be TRUE for Claude's position to be correct?
3. What assumption are you making that Claude is not?
```

### Synthesize assumptions:

```
## ASSUMPTION EXTRACTION

The disagreement persists because of different assumptions:

| Party | Core Assumption | If True → |
|-------|-----------------|-----------|
| Claude | [assumption] | Claude's position correct |
| Gemini | [assumption] | Gemini's position correct |
| Codex | [assumption] | Codex's position correct |

**The real question is:** Which assumption matches YOUR reality?
```

---

## PHASE 8: FINAL OUTPUT

### If CONSENSUS reached:

```
## DEBATE OUTCOME: CONSENSUS

**Topic:** $ARGUMENTS

**Final position:** [Claude's position, potentially evolved]

**Confidence:** HIGH

**What Claude learned:**
- From Gemini: [insight]
- From Codex: [insight]
- From Qwen: [insight]

**Position evolution:**
v1 → v2 → v3 (final)

**Rounds to consensus:** [N]

---

### Audit Trail

<details>
<summary>Full debate history</summary>

[Complete log of all rounds]

</details>
```

### If NO CONSENSUS:

Generate tradeoff document using template from `templates/tradeoff-document.md`:

```
## DEBATE OUTCOME: TRADEOFF IDENTIFIED

**Topic:** $ARGUMENTS

**Rounds:** [N] (max reached)

**Status:** Genuine disagreement - not a failure, but a signal

---

[Full tradeoff document with Options A/B/C, assumptions, recommendations]
```

---

## SETTINGS REFERENCE

Check for user settings in `~/.claude/debate.local.md`:

```yaml
---
max_rounds: 5              # Override max confrontation rounds
timeout_per_cli: 120       # CLI timeout in seconds
save_debate_logs: true     # Save to debate_log_path
debate_log_path: "./debate-logs"
skeptical_of_early_agreement: true
---
```

---

## ERROR HANDLING

### If a CLI fails mid-debate:

1. Log the failure
2. Continue with remaining challengers
3. If ALL challengers fail → abort with error
4. Minimum requirement: Claude + 1 working challenger

### If timeout:

1. Note which CLI timed out
2. Proceed with available responses
3. Mention in final output: "[Model] timed out in round [N]"
