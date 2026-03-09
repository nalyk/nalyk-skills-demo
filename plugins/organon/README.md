# organon

Philosophical reasoning engine for Claude Code. Turns 62 principles from 20 philosophers into a live decision engine and code review framework.

> Based on [Organon](https://gitlab.com/lightcyphers-open/organon) by [Lightcyphers SRL](https://lightcyphers.com), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## What It Does

The organon is not a reference document — it is a **reasoning engine**. It auto-detects your engineering situation, selects the relevant philosophical principles, runs a structured decision protocol, and produces actionable output.

**Two modes:**
- **Decision mode** — Engineering decisions: "should we...", "which approach...", "trade-off between..."
- **Review mode** — Code/design quality: systematic evaluation against 62 principles

**Three depth levels:**
- **Quick** — One principle + action (3-5 lines)
- **Standard** — Multiple principles + protocol summary
- **Deep** — Full 22-step protocol via philosopher-council agent + Summa Method objections + confidence rating

## Installation

```bash
/plugin install organon@nalyk-skills-demo
```

## Usage

### Auto-detect (recommended)
```
/organon
```
Reads conversation context, determines mode and depth automatically.

### Explicit decision analysis
```
/organon:decide should we use microservices or monolith
/organon:decide deep how to handle the v1 to v2 migration
```

### Explicit philosophical review
```
/organon:review src/auth/handler.ts
/organon:review deep src/core/
```

### Depth override
```
/organon quick
/organon deep
```

## The Philosophers

| Group | Philosophers | Domain |
|---|---|---|
| **Idealists** | Aristotle, Marcus Aurelius, Epictetus, Plato, Seneca | What is right |
| **Realist** | Machiavelli | What works |
| **Engineers** | Leibniz, Boole, Frege, Godel, Turing, Shannon, Church | What is computable |
| **Conventionalist** | Poincare | How to choose between equivalents |
| **Integrator** | Aquinas | How to synthesize traditions |
| **Bayesian** | Swinburne | Where to focus investigation |
| **Auditor** | Kant | What can be known |
| **Closers** | Popper, Wittgenstein, Peirce | What survives reality |

## The 62 Principles

| # | Principle | Philosopher | One-liner |
|---|---|---|---|
| I | Four Causes | Aristotle | Material, Formal, Efficient, Final — answer before starting |
| 1 | Dichotomy of Control | Marcus Aurelius | 100% effort on what you control |
| 2 | Golden Mean | Aristotle | Virtue between extremes |
| 3 | Phronesis | Aristotle | Apply rules in context, not blindly |
| 4 | Obstacle is the Way | Marcus Aurelius | The blocker IS your task |
| 5 | Praemeditatio | Epictetus | Anticipate failure modes |
| 6 | Askesis | Epictetus | Every commit is training |
| 7 | View from Above | Marcus Aurelius | Lost in details? Zoom out |
| 8 | Dialectic | Plato | Good question beats premature answer |
| 9 | Cave Allegory | Plato | Execute request, flag root cause |
| 10 | Kalokagathia | Plato | Beautiful code is good code |
| 11 | Tripartite Soul | Plato | Reason leads, detect filler |
| 12 | Brevity | Seneca | Maximum information per symbol |
| 13 | Mentorship | Seneca | Mentor tone, not lecture |
| 14 | Tranquillitas | Seneca | Reduce scope, not quality |
| 15 | Philosopher-King | Plato | Power = responsibility |
| 16 | Prohairesis | Epictetus | Judgment quality constant under degradation |
| 17 | Otium | Seneca | 10% research saves hours |
| 18 | De Ira | Seneca | Respond on substance, not emotion |
| 19 | Verita effettuale | Machiavelli | Start from observed reality |
| 20 | Fortuna/Virtu | Machiavelli | Build structural optionality |
| 21 | Lion and Fox | Machiavelli | Direct force or cunning indirection |
| 22 | Economy of Force | Machiavelli | Disruption: once, sharp, complete |
| 23 | Necessita | Machiavelli | All options bad? Least harmful |
| 24 | Occasione | Machiavelli | Right action at wrong time = wrong |
| 25 | Intelligence | Machiavelli | Verify before acting |
| 26 | Characteristica | Leibniz | Name everything precisely |
| 27 | Calculemus | Leibniz | Calculate, don't argue |
| 28 | Alphabet of Thought | Leibniz | Decompose into composable primitives |
| 29 | Laws of Thought | Boole | Simplify Boolean conditions |
| 30 | Syntax vs. Semantics | Frege | Separate interface from implementation |
| 31 | Scope & Recursion | Frege | Minimize scope, think recursively |
| 32 | Incompleteness | Godel | No single method catches all |
| 33 | Universal Machine | Turing | If describable, then automatable |
| 34 | Computability | Turing | Some problems are undecidable |
| 35 | Layer Separation | Shannon | Separate what from how |
| 36 | Information Theory | Shannon | Maximize signal-to-noise |
| 37 | Lambda Calculus | Church | Functions as primitives |
| 38 | Copernican Turn | Kant | Be aware of your structuring lens |
| 39 | Categories | Kant | Quantity, Quality, Relation, Modality sweep |
| 40 | Categorical Imperative | Kant | Universalize your actions |
| 41 | Synthetic A Priori | Kant | Types (analytic), tests (empirical), algorithms (necessary) |
| 42 | Noumena | Kant | State observed vs. inferred |
| 43 | Antinomies | Kant | Contradictory practices? Reframe |
| 44 | Duty | Kant | Same quality whether or not anyone watches |
| 45 | Falsifiability | Popper | Tests that try to destroy |
| 46 | Conjectures | Popper | All solutions are conjectures |
| 47 | Paradox of Tolerance | Popper | Define what system will NOT accept |
| 48 | Language Games | Wittgenstein | Meaning is use. Align first |
| 49 | Beetle in the Box | Wittgenstein | Only public contract matters |
| 50 | Silence | Wittgenstein | Can't say it clearly? Say nothing |
| 51 | Pragmatic Maxim | Peirce | What concrete difference? |
| 52 | Abduction | Peirce | Debug from specific evidence |
| 53 | Fallibilism | Peirce | All knowledge is provisional |
| 54 | Conventionalism | Poincare | Equivalent options are conventions |
| 55 | Structural Stability | Poincare | Small changes stay local |
| 56 | Creative Recombination | Poincare | Recombine known patterns |
| 57 | Summa Method | Aquinas | Enumerate objections before claiming |
| 58 | Essence/Existence | Aquinas | Type vs. instantiation |
| 59 | Proportionate Causality | Aquinas | Output bounded by weakest input |
| 60 | Bayesian Focus | Swinburne | Investigate where probability concentrates |
| 61 | Simplicity Prior | Swinburne | Complexity must justify itself |
| 62 | Cumulative Case | Swinburne | Many weak signals = strong evidence |

## License

Based on [Organon](https://gitlab.com/lightcyphers-open/organon) by [Lightcyphers SRL](https://lightcyphers.com).
Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
