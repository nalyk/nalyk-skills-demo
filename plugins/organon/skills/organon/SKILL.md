---
name: organon
description: >-
  This skill should be used when the user faces an engineering decision, asks "should we...",
  "which approach...", "trade-off between...", "how to structure...", "evaluate this design",
  "review this code philosophically", "think through this", "analyze this approach",
  "what principles apply here", or invokes /organon, /organon:decide, /organon:review.
  Also auto-triggers on architectural decisions, debugging sessions, code reviews,
  design evaluations, and any situation where structured philosophical reasoning
  improves the outcome. This skill turns 62 philosophical principles from 20
  philosophers into a live reasoning engine for engineering.
version: 1.0.0
---

# Organon — Philosophical Reasoning Engine

> Source: [Organon](https://gitlab.com/lightcyphers-open/organon) by Lightcyphers SRL, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

A decision engine and review framework that applies 62 principles from 20 philosophers to engineering problems. Not a reference — an engine. Detect the situation, select principles, run the protocol, produce structured output.

## Modes

**Auto-detect** (default): Read context, determine if this is a decision or a review, select depth, execute.

**Decision mode** (`/organon:decide`): Engineering decision analysis. Takes a situation, identifies applicable principles, runs protocol steps, produces recommendation with objections addressed.

**Review mode** (`/organon:review`): Philosophical code/design review. Takes code or design, systematically evaluates against quality dimensions derived from the 62 principles.

## Depth Levels

| Level | When | Context loaded | Output |
|-------|------|---------------|--------|
| **Quick** | Clear situation, single principle applies | This SKILL.md only | 3-5 lines: principle + action |
| **Standard** | Non-trivial, multiple principles apply | + relevant philosopher references | Principles with rationale + protocol summary |
| **Deep** | Architectural, irreversible, high-stakes | Full protocol via philosopher-council agent | 22-step walk + Summa objections + confidence |

Auto-select depth by: Quick if one principle clearly maps. Standard if 2+ principles or ambiguity. Deep if irreversible decision, architectural choice, or conflicting principles. User can override with `/organon quick`, `/organon standard`, `/organon deep`.

## Execution Protocol

### Step 1: Detect Situation

Read the current context — what is the user doing? Map to one of these categories:

| Context signal | Mode | Typical depth |
|---|---|---|
| "should we", "which approach", "trade-off" | Decision | Standard |
| "review this", "what's wrong with", code snippet | Review | Standard |
| "debug", "why does this", "root cause" | Decision (abductive) | Standard |
| "architecture", "design system", "how to structure" | Decision | Deep |
| Routine question, clear answer exists | Decision | Quick |
| Explicit `/organon:decide` or `/organon:review` | As specified | As specified or auto |

### Step 2: Route to Principles

Use the compact routing table below. Match the situation to applicable principles, then load the relevant reference files for those principles.

### Step 3: Apply and Produce Output

**Decision mode output format:**

```
ORGANON — Decision Analysis
===========================
Situation: [detected/stated]
Depth: Quick | Standard | Deep

Applicable Principles:
  #XX Principle (Philosopher) -> Concrete action for this situation
  #XX Principle (Philosopher) -> Concrete action for this situation

[Standard/Deep only:]
Protocol Steps:
 1. Four Causes -> Material: X | Formal: Y | Efficient: Z | Final: W
 2. Effectual Truth -> Verified: [what was checked]
 ...

[Deep only:]
Summa Method — Objections:
 Videtur quod non 1: [objection] -> Ad 1: [resolution]
 Videtur quod non 2: [objection] -> Ad 2: [resolution]

Decision: [recommendation]
Confidence: [High|Medium|Low] — Cumulative case: [N signals listed]
```

**Review mode output format:**

```
ORGANON — Philosophical Review
===============================
Target: [file/code/design]

Quality Dimensions:
  Kalokagathia (beauty=good):       [pass|warn|fail] [finding]
  Golden Mean (balance):             [pass|warn|fail] [finding]
  Structural Stability:              [pass|warn|fail] [finding]
  Falsifiability (tests):            [pass|warn|fail] [finding]
  Proportionate Causality:           [pass|warn|fail] [finding]
  Beetle in the Box (contracts):     [pass|warn|fail] [finding]
  Information Theory (S/N ratio):    [pass|warn|fail] [finding]
  Categorical Imperative:            [pass|warn|fail] [finding]
  Simplicity Prior:                  [pass|warn|fail] [finding]
  Paradox of Tolerance (validation): [pass|warn|fail] [finding]
  Layer Separation (what vs how):    [pass|warn|fail] [finding]
  Scope Discipline (bindings):       [pass|warn|fail] [finding]

Principle Violations: [list with specific references]
Strengths: [what the code does well]
Recommendation: [concrete next actions]
```

## Compact Routing Table

Map situations to principles. For full detail on any principle, load the relevant reference file.

| Situation | Principle | Action | Detail |
|---|---|---|---|
| Don't understand requirement | Dialectic (8) | Ask 1-2 maximally clarifying questions | `references/principles-plato.md` |
| Don't know where to start | Four Causes (I) | Decompose: Material, Formal, Efficient, Final | `references/principles-aristotle.md` |
| Blocked by dependency/bug | Obstacle is the Way (4) | The blocker IS the task now | `references/principles-stoics.md` |
| About to deploy/execute | Praemeditatio (5) | Risk checklist. Confirm if irreversible | `references/principles-stoics.md` |
| Writing docs/PR/messages | Brevity (12) | Maximum density, zero filler | `references/principles-seneca.md` |
| Aggressive code review | De Ira (18) | Respond on substance, ignore tone | `references/principles-seneca.md` |
| "Trivial" task | Askesis (6) | Same quality standard as major tasks | `references/principles-stoics.md` |
| Output OK but not excellent | Kalokagathia (10) | Is it clear, not just correct? | `references/principles-plato.md` |
| Everything on fire | Tranquillitas (14) | Reduce scope, not quality | `references/principles-seneca.md` |
| Applying a design pattern | Phronesis (3) | Relevant here? Benefit vs. cost? | `references/principles-aristotle.md` |
| Docs don't match reality | Verita effettuale (19) | Trust code over documentation | `references/principles-machiavelli.md` |
| All options are bad | Necessita (23) | Least harmful, document trade-off | `references/principles-machiavelli.md` |
| Problem resists direct attack | Lion/Fox (21) | Try indirection: strangler fig, facade | `references/principles-machiavelli.md` |
| Breaking change needed | Economy of Force (22) | One clean cut with full communication | `references/principles-machiavelli.md` |
| Perfect blocking good | Virtu (20) | Ship, observe, iterate | `references/principles-machiavelli.md` |
| Ambiguous naming/requirements | Characteristica (26) | Formalize first, then implement | `references/principles-engineers.md` |
| Debate measurement can settle | Calculemus (27) | Calculate, don't argue | `references/principles-engineers.md` |
| Complex system design | Alphabet of Thought (28) | Decompose into composable primitives | `references/principles-engineers.md` |
| API design / validation | Syntax vs. Semantics (30) | Separate interface from implementation | `references/principles-engineers.md` |
| Verification strategy | Incompleteness (32) | Defense in depth; no single method catches all | `references/principles-engineers.md` |
| Two designs seem equal | Conventionalism (54) | It's a convention. Pick for simplicity. Document. | `references/principles-poincare.md` |
| One spec change touches many files | Structural Stability (55) | Abstraction boundaries are wrong. Refactor. | `references/principles-poincare.md` |
| Stuck on a design problem | Creative Recombination (56) | Decompose into known patterns, recombine | `references/principles-poincare.md` |
| Making architectural recommendation | Copernican Turn (38) | State your bias: "I'm more familiar with X" | `references/principles-kant.md` |
| Analyzing code not fully read | Noumena (42) | Say "in the files I've reviewed" | `references/principles-kant.md` |
| Tempted to skip tests | Categorical Imperative (40) | If everyone skipped this, would the system survive? | `references/principles-kant.md` |
| Writing tests | Falsifiability (45) | Try to destroy, not confirm | `references/principles-popper.md` |
| Designing API input validation | Paradox of Tolerance (47) | Define what it will NOT accept | `references/principles-popper.md` |
| Two teams disagree on requirements | Language Games (48) | Same word, different meaning? Align first | `references/principles-wittgenstein.md` |
| Don't know the answer | Silence (50) | Say "I don't know." No filler. | `references/principles-wittgenstein.md` |
| Architecture debate, no clear winner | Pragmatic Maxim (51) | What concrete difference in 6 months? | `references/principles-peirce.md` |
| Debugging / incident response | Abduction (52) | Reason from specific evidence, not pattern matching | `references/principles-peirce.md` |
| Choosing a tech stack | Fallibilism (53) | All choices are provisional. Build for migration. | `references/principles-peirce.md` |
| Proposing a design | Summa Method (57) | Enumerate 2-4 strongest objections before presenting | `references/principles-aquinas.md` |
| Claiming "fully tested" | Proportionate Causality (59) | Confidence bounded by weakest link | `references/principles-aquinas.md` |
| Many options, limited time | Bayesian Focus (60) | Investigate highest-probability option first | `references/principles-swinburne.md` |
| Simple vs complex approach | Simplicity Prior (61) | Simple starts with higher confidence | `references/principles-swinburne.md` |
| Single test passes but feels fragile | Cumulative Case (62) | Count independent signals | `references/principles-swinburne.md` |

For the complete 82-row lookup table: `references/quick-reference.md`

## Decision Protocol Summary

For Standard/Deep depth, traverse applicable steps:

```
 1. ARISTOTLE — Four Causes          -> Purpose clear?
 2. MACHIAVELLI — Effectual Truth     -> Verified actual state?
 2b. SWINBURNE — Bayesian Focus       -> Where does evidence concentrate?
 3. MARCUS — Dichotomy of Control     -> What do I control?
 3b. KANT — Copernican Turn           -> Aware of my biases?
 4. MACHIAVELLI — Fortuna + Virtu     -> Built structural optionality?
 5. ARISTOTLE — Golden Mean           -> Am I at an extreme?
 6. ARISTOTLE — Phronesis             -> Does this practice apply HERE?
 7. EPICTETUS — Praemeditatio         -> Failure modes addressed?
 7b. KANT — Categories                -> Quantity, Quality, Relation, Modality sweep?
 8. MACHIAVELLI — Necessita           -> No clean solution? Least harmful?
 8b. KANT — Categorical Imperative    -> Universalizable?
 8c. POINCARE — Conventionalism       -> Equivalent options? Pick for stability.
 8d. AQUINAS — Summa Method           -> Strongest objections enumerated?
 9. MACHIAVELLI — Occasione           -> One-way or two-way door?
10. SENECA — Action                   -> Enough analysis. Execute.
11. PLATO — Kalokagathia              -> Correct AND clear?
12. MACHIAVELLI — Effectual Gate      -> Does it ship?
13. KANT — Epistemic Honesty Gate     -> Claiming only what observed?
14. POPPER — Falsification Gate       -> Tried to break my own solution?
15. WITTGENSTEIN — Language Gate       -> All key terms defined?
16. PEIRCE — Pragmatic Gate (FINAL)   -> What concrete difference does this produce?
```

For the full 22-step protocol with rationale: `references/decision-protocol.md`

## Deep Mode

For deep analysis, delegate to the `philosopher-council` agent. The agent runs the full 22-step protocol, loading all relevant reference files, producing comprehensive analysis with Summa Method objections.

## Reference Files

Detailed principles, examples, anti-patterns, and computational rationale:

- **`references/principles-aristotle.md`** — Four Causes, Golden Mean, Phronesis
- **`references/principles-stoics.md`** — Dichotomy of Control, Obstacle, Praemeditatio, Askesis, View from Above, Prohairesis
- **`references/principles-plato.md`** — Dialectic, Cave, Kalokagathia, Tripartite Soul, Philosopher-King
- **`references/principles-seneca.md`** — Brevity, Mentorship, Tranquillitas, Otium, De Ira
- **`references/principles-machiavelli.md`** — Verita effettuale, Fortuna/Virtu, Lion/Fox, Economy of Force, Necessita, Occasione, Intelligence
- **`references/principles-engineers.md`** — Characteristica, Calculemus, Alphabet, Laws of Thought, Syntax/Semantics, Scope/Recursion, Incompleteness, Universal Machine, Computability, Layer Separation, Information Theory, Lambda Calculus
- **`references/principles-kant.md`** — Copernican Turn, Categories, Categorical Imperative, Synthetic A Priori, Noumena, Antinomies, Duty
- **`references/principles-popper.md`** — Falsifiability, Conjectures and Refutations, Paradox of Tolerance
- **`references/principles-wittgenstein.md`** — Language Games, Beetle in the Box, Whereof One Cannot Speak
- **`references/principles-peirce.md`** — Pragmatic Maxim, Abductive Reasoning, Fallibilism
- **`references/principles-poincare.md`** — Conventionalism, Structural Stability, Creative Recombination
- **`references/principles-aquinas.md`** — Summa Method, Essence/Existence, Proportionate Causality
- **`references/principles-swinburne.md`** — Bayesian Focus, Simplicity Prior, Cumulative Case
- **`references/quick-reference.md`** — Complete 82-row situation-to-action lookup table
- **`references/decision-protocol.md`** — Full 22-step decision protocol with rationale
