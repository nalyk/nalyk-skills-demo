---
name: review
description: "Organon philosophical review — evaluate code or design against 62 engineering principles from 20 philosophers. Systematic quality audit."
---

# /organon:review — Philosophical Review

Invoke the `organon` skill explicitly in **review mode**.

## Behavior

1. Take the target from arguments or conversation context (file, code snippet, design, PR)
2. Read the target code/design
3. Systematically evaluate against quality dimensions derived from the 62 principles
4. Produce structured review with pass/warn/fail ratings per dimension

## Arguments

Required: A target to review.

- `/organon:review src/auth/handler.ts` — Review a specific file
- `/organon:review` — Review whatever is in current context (last code written, current PR)
- `/organon:review deep src/core/` — Deep philosophical review of a directory

## Quality Dimensions Evaluated

| Dimension | Source Principle | What it checks |
|---|---|---|
| Kalokagathia | Plato (10) | Beautiful = good. Readable, clear, self-documenting |
| Golden Mean | Aristotle (2) | Balance — not over/under-engineered |
| Structural Stability | Poincare (55) | Small requirement changes stay local |
| Falsifiability | Popper (45) | Tests try to destroy, not confirm |
| Proportionate Causality | Aquinas (59) | Output quality matches input quality |
| Beetle in the Box | Wittgenstein (49) | Depends on contracts, not internals |
| Information Theory | Shannon (36) | Signal-to-noise ratio in code and comments |
| Categorical Imperative | Kant (40) | If everyone did this, would the codebase survive? |
| Simplicity Prior | Swinburne (61) | Complexity justified by evidence? |
| Paradox of Tolerance | Popper (47) | Defines what it will NOT accept (input validation) |
| Layer Separation | Shannon (35) | What separated from how |
| Scope Discipline | Frege (31) | Minimal scope, clean bindings |

## Output Format

```
ORGANON — Philosophical Review
===============================
Target: [file/design]

Quality Dimensions:
  Kalokagathia:          [pass|warn|fail] [finding]
  Golden Mean:           [pass|warn|fail] [finding]
  ...

Principle Violations: [specific issues with line references]
Strengths: [what the code does well]
Recommendation: [concrete next actions]
```
