---
name: decide
description: "Organon decision engine — apply philosophical principles to an engineering decision. Identifies applicable principles, runs protocol steps, produces structured recommendation."
---

# /organon:decide — Decision Engine

Invoke the `organon` skill explicitly in **decision mode**.

## Behavior

1. Take the decision/situation from arguments or conversation context
2. Match situation to applicable principles using the routing table
3. Run the decision protocol at the appropriate depth
4. Produce structured output:
   - Applicable principles with concrete actions
   - Protocol steps traversed (Standard/Deep)
   - Summa Method objections addressed (Deep)
   - Confidence rating with cumulative case evidence

## Arguments

Required: A decision or situation to analyze.

- `/organon:decide should we use REST or GraphQL for this API`
- `/organon:decide all our options seem bad — tight deadline, complex feature, team is small`
- `/organon:decide deep how should we handle the migration from v1 to v2`

Optional depth prefix: `quick`, `standard`, `deep`

## Output Format

```
ORGANON — Decision Analysis
===========================
Situation: [the decision]
Depth: [level]

Applicable Principles:
  #XX Principle (Philosopher) -> Concrete action
  ...

Protocol Steps:
 1. Four Causes -> [analysis]
 ...

Decision: [recommendation]
Confidence: [High|Medium|Low] — [evidence]
```
