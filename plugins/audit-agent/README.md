# Audit Agent

Multi-framework audit agent with three complementary lenses for comprehensive product and code analysis.

## The Three Frameworks

| Framework | Focus | Best For | Questions/Metrics |
|-----------|-------|----------|-------------------|
| **Jobs** | Design simplification | UX, features, workflows | 13 questions |
| **Carlin** | BS detection | Marketing, docs, pitches | 13 questions |
| **Vibe** | Engineering quality | Code, architecture, infra | 20 metrics |

## Quick Start

### Individual Audits

```bash
# Design thinking audit
/jobs-audit my-product-feature

# BS detection
/carlin-audit our-marketing-copy

# Engineering quality
/vibe-audit ./src
```

### Combined Analysis

```bash
# Run all three
/multi-audit my-product --all

# Run specific combination
/multi-audit my-feature --jobs --carlin

# Run two frameworks
/multi-audit ./codebase --vibe --carlin
```

## When to Use Each

### Steve Jobs Design Thinking (`/jobs-audit`)

Use when:
- Something feels "too complex"
- Users are confused
- Evaluating new features
- Deciding what to cut
- Product design reviews

Key questions address: simplification, elegance, beginner's mind, restraint.

### George Carlin BS Detector (`/carlin-audit`)

Use when:
- Marketing copy feels hollow
- Documentation promises don't match reality
- Evaluating competitor claims
- Preparing honest positioning
- Internal communication audit

Key questions address: hidden agendas, euphemisms, contradictions, performance vs reality.

### Brutal Vibe Audit (`/vibe-audit`)

Use when:
- Assessing code quality
- Technical due diligence
- Evaluating AI-generated code
- Pre-launch review
- Architecture decisions

Scores 20 metrics across architecture, engineering, performance, security, and operations.

## Framework Synergy

| Combination | Power | Use Case |
|-------------|-------|----------|
| Jobs + Carlin | Design + Marketing alignment | Product launches |
| Jobs + Vibe | Simple AND solid | Core features, MVPs |
| Carlin + Vibe | Honest AND production-ready | Technical due diligence |
| All Three | Complete product audit | Major releases, acquisitions |

## Auto-Detection

Skills auto-activate on relevant keywords:

**Jobs triggers:** "simplify", "too complex", "UX review", "feature bloat"

**Carlin triggers:** "BS", "jargon", "sounds fake", "marketing speak"

**Vibe triggers:** "code review", "production ready", "vibe check", "slop check"

## Output Expectations

### Jobs Audit Output
- 13 answered questions with evidence
- Completion checklist (13/13)
- Top 3 immediate actions
- THE ONE GREAT IDEA

### Carlin Audit Output
- 13 answered questions in Carlin's voice
- Completion checklist (13/13)
- Top 3 BS to eliminate
- THE ONE THING TO SAY OUT LOUD

### Vibe Audit Output
- 20 scored metrics (0-5 each)
- Section and total scores
- Verdict band (0-100 scale)
- 10-item Pareto fix plan
- Deployment confidence level

### Multi-Audit Output
- Summary from each framework
- Cross-reference matrix
- Priority escalation analysis
- Unified 10-item action plan
- Meta-insight from combined analysis

## Philosophy

**Jobs:** "Simplicity is the ultimate sophistication."

**Carlin:** "The reason I talk to myself is because I'm the only one whose answers I accept."

**Vibe:** "Assume every README is lying until proven otherwise."

## File Structure

```
audit-agent/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── jobs-audit.md
│   ├── carlin-audit.md
│   ├── vibe-audit.md
│   └── multi-audit.md
├── skills/
│   ├── jobs-audit/SKILL.md
│   ├── carlin-audit/SKILL.md
│   └── vibe-audit/SKILL.md
├── references/
│   ├── synthesis-matrix.md
│   └── audit-protocol.md
└── README.md
```

## License

MIT
