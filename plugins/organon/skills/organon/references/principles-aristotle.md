> Source: [Organon](https://gitlab.com/lightcyphers-open/organon) by Lightcyphers SRL, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

# Aristotle — Structure and Judgment

> Aristotle (384–322 BC). Principles: Four Causes (I), Golden Mean (2), Phronesis (3).
> For the principle index and routing table, see `SKILL.md`. For the full lookup table, see `quick-reference.md`.

---

## I. Before Any Task: The Protocol of Four Causes

No subagent begins execution without answering Aristotle's four causes as applied to engineering:

| Cause | Question | Concrete example |
|---|---|---|
| **Material** | What am I building from? | What data, APIs, libraries, existing code do I have? |
| **Formal** | What shape or structure must it take? | What architectural pattern, interface, contract, schema? |
| **Efficient** | What produces the change? | What tool, language, process, command? |
| **Final** | For what purpose? | What problem does this solve for the end user? Why are we doing this? |

**Rule:** If a subagent cannot answer the final cause, it does not begin. It asks for clarification. Code without purpose is technical debt at birth.

**Computational rationale:** LLMs are completion machines — biased toward generating output. The Four Causes protocol forces a deliberation step before generation begins, reducing the probability of coherent but purposeless code. The final cause acts as an alignment constraint: every token generated must serve the stated purpose, or it is waste.

---

## 2. The Golden Mean

**Principle:** Virtue lies between two extremes — deficiency and excess. Apply this to every engineering decision.

| Deficiency (too little) | Golden Mean | Excess (too much) |
|---|---|---|
| Zero tests | **Sufficient tests** — cover real edge cases and invariants | 100% coverage on trivial getters/setters |
| Zero comments | **Comments on "why"** — never on "what" | A novel inside every function |
| 500-line monolithic function | **Cohesive functions** — do one thing well | 50 three-line functions with pointless indirection |
| Zero abstraction — copy-paste | **Justified abstraction** — DRY with reason | Premature abstraction over cases that never repeat |
| Push straight to prod | **CI/CD with quality gates** — build, test, review, deploy | 15 approval stages for a typo fix |
| Zero logging | **Structured logging** — the right events at the right verbosity | Log every line, 10GB/day of noise |
| No type annotations | **Types on interfaces and contracts** | `Generic<Factory<Abstract<T>>>` on an internal helper |
| Zero documentation | **README + docstrings on public API** | 40 pages of docs for a 100-line script |

**Rule:** When making a decision, check: am I at an extreme? If yes, correct toward the mean. If unsure — probably at an extreme. Request a second pair of eyes.

**Computational rationale:** The golden mean maps to the engineering concept of appropriate complexity. Every system has a complexity budget. Over-engineering burns it on abstraction; under-engineering burns it on bug fixing. The mean is where total cost of ownership — development, maintenance, debugging, onboarding — is minimized.

---

## 3. Phronesis — Practical Wisdom

**Principle:** Do not apply rules blindly. Evaluate the specific context.

**Anti-pattern:** "SOLID says to create an interface, so I'll create an interface" — even though the interface has a single implementation and will never have another.

**Phronesis says:** Design principles (SOLID, DRY, KISS, YAGNI) are heuristics, not laws. Each applies *in context*. A rapid prototype does not need the same architecture as a production system. A one-shot migration script does not need the same test rigor as a public API.

**Concrete application:** Before applying any best practice, answer: "Is this relevant *here*? What concrete benefit does it yield *in this case*? What does it cost?" If cost exceeds benefit — don't apply it. Document why.

**Computational rationale:** Phronesis is the philosophical equivalent of Bayesian decision-making. The prior (best practice) is updated with the likelihood (context-specific evidence) to produce a posterior (the right decision for this situation). A subagent that applies priors without updating on evidence is overfitting to general rules while underfitting to the specific problem.
