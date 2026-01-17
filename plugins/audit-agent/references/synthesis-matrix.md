# Cross-Framework Synthesis Matrix

Rules for combining insights from Jobs, Carlin, and Vibe audits.

## Priority Escalation Rules

### CRITICAL (Immediate Action Required)

When **all three frameworks** flag the same issue:
- Jobs Question X says "simplify/remove"
- Carlin Question Y exposes "BS/contradiction"
- Vibe Metric Z scores < 3

**This is a fundamental problem.** The feature/component:
- Adds unnecessary complexity (Jobs)
- Isn't honest about what it does (Carlin)
- Isn't well-engineered (Vibe)

**Action:** Remove or completely redesign.

### HIGH CONFIDENCE (Strong Evidence)

When **two frameworks** agree:

| Combo | Meaning | Action |
|-------|---------|--------|
| Jobs + Carlin | Design is overcomplicated AND messaging is BS | Simplify AND be honest about limitations |
| Jobs + Vibe | Complex design AND poor engineering | Simplify to enable better engineering |
| Carlin + Vibe | Marketing BS exposed AND engineering confirms | Remove marketing lies, document real state |

### MEDIUM (Single Framework Finding)

When only **one framework** flags an issue:
- May be legitimate finding from that perspective
- Cross-check with other frameworks before acting
- Could be a blind spot the other frameworks don't cover

## Contradiction Resolution

### Jobs says "keep" but Carlin says "BS"
**Meaning:** Feature has real user value but is marketed dishonestly.
**Action:** Keep the feature, rewrite the messaging.

### Vibe says "solid" but Carlin says "BS"
**Meaning:** Good engineering, bad positioning.
**Action:** Technical work is fine, fix marketing/docs.

### Jobs says "simplify" but Vibe says "needed"
**Meaning:** Complexity is technically justified but poorly surfaced.
**Action:** Keep complexity, improve abstraction/UI.

### Carlin says "BS" but Vibe scores high
**Meaning:** Real capability exists but overclaimed.
**Action:** Tone down claims to match actual delivery.

### Jobs says "elegant" but Vibe scores low
**Meaning:** Looks good but isn't well-built.
**Action:** Prioritize engineering fixes over new features.

## Scoring Normalization

To compare across frameworks:

| Jobs | Carlin | Vibe | Normalized |
|------|--------|------|------------|
| Strong positive answer | Passes BS test | 4-5 | GREEN |
| Neutral/unclear answer | Minor BS detected | 3 | YELLOW |
| Negative answer | Major BS detected | 0-2 | RED |

## Cross-Reference Patterns

### Pattern: "Looks Good, Isn't Real"
- Jobs: Elegant design concept
- Carlin: Major performance gap detected
- Vibe: Low scores on metrics 3, 7, 18
**Diagnosis:** Demo-ware. Prioritize engineering before marketing.

### Pattern: "Over-Engineered BS"
- Jobs: Unnecessary complexity identified
- Carlin: Buzzword-heavy, euphemism-rich
- Vibe: High architecture score, low business logic scores
**Diagnosis:** Engineering theater. Simplify and focus on core.

### Pattern: "Hidden Gem"
- Jobs: Core function is strong
- Carlin: Honest about what it does
- Vibe: Solid scores with clear improvement path
**Diagnosis:** Good foundation. Polish and ship.

### Pattern: "Marketing Mirage"
- Jobs: Users are confused
- Carlin: Every question exposes contradiction
- Vibe: Low scores across all sections
**Diagnosis:** Needs fundamental rethink. Consider pivot or sunset.

## Synthesis Output Template

```markdown
## Multi-Framework Synthesis

### Agreement Matrix
| Area | Jobs | Carlin | Vibe | Consensus |
|------|------|--------|------|-----------|
| [Area 1] | Q# | Q# | M# | AGREE/CONTRADICT |

### Priority Actions
1. [CRITICAL] - All frameworks agree: [action]
2. [HIGH] - Two frameworks agree: [action]
3. [MEDIUM] - Single framework: [action]

### Contradictions Requiring Human Judgment
- [Contradiction 1]: Jobs says X, Carlin says Y. Recommendation: Z
```
