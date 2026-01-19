# debate

Multi-model adversarial debate plugin for Claude Code. Claude defends positions against external CLI models (Gemini, Codex, Qwen) through structured confrontation.

## The Problem

- **Decision paralysis** - Complex decisions with no obvious answer
- **Blind spots** - Your ideas pass your own review, but what are you missing?
- **Yes-man AI** - Claude agrees too easily, you want genuine pushback
- **No audit trail** - Decisions made without documented reasoning

## The Solution

**Real debate, not theater.**

Claude forms a position, then external AI models challenge it. Claude must defend, accept valid critiques, or synthesize. Different models = different training = different blind spots = genuine adversarial value.

**This plugin refuses to run with Claude-only.** Claude debating itself provides no genuine diversity.

## Requirements

**Minimum:** 1 external CLI installed and authenticated

| CLI | Install | Free Tier |
|-----|---------|-----------|
| Gemini | `npm i -g @google/gemini-cli` | 1000 req/day |
| Codex | `npm i -g @openai/codex` | ChatGPT Plus |
| Qwen | `npm i -g @qwen-code/qwen-code` | 2000 req/day |

## Installation

```bash
# Add marketplace (if not already added)
/plugin marketplace add nalyk/nalyk-skills-demo

# Install plugin
/plugin install debate@nalyk-skills-demo

# Check system health
/debate:doctor
```

## Commands

| Command | Purpose |
|---------|---------|
| `/debate <topic>` | Full adversarial debate on any topic |
| `/debate:doctor` | Check CLI availability and authentication |
| `/debate:adr <topic>` | Debate with formal ADR output |

## How It Works

### The Hybrid Protocol

1. **Claude forms position** on your topic
2. **Parallel challenge** - All external models critique simultaneously
3. **Consensus check** - If all agree → fast exit with high confidence
4. **Sequential confrontation** - If disagreement, back-and-forth debate
5. **Iterate** until consensus OR max rounds (default: 5)
6. **Assumption extraction** - Surface WHY positions differ
7. **Output** - Consensus OR structured tradeoff document

### The Key Innovation

**Disagreement is signal, not failure.**

When models can't agree, the output isn't "we failed" - it's a structured tradeoff document that exposes:
- What each option assumes
- When each option is correct
- The hidden assumptions causing the split

This transforms "who's right?" into **"what would have to be true for each to be right?"**

## Example

```
You: /debate Should we use microservices or monolith for this project?

Claude: I recommend a modular monolith because [reasons]...
        Confidence: MEDIUM
        Assumptions: Team size stays under 10, traffic under 10k req/s

[Gemini challenges]: "Claude ignores scaling. At 100k users you'll regret this."
[Codex challenges]: "Microservices add DevOps overhead Claude underestimates."
[Qwen agrees]: "Modular monolith is correct for this context."

Claude responds to Gemini: "Valid point about scale. But the assumption is
growth to 100k in 18 months. If that's true, I update my position to
recommend microservices. If growth is slower, monolith wins."

[Debate continues until consensus or max rounds]

OUTCOME: TRADEOFF IDENTIFIED

Option A (Monolith): Best if team < 10, growth < 50k users/year
Option B (Microservices): Best if team > 15 or growth > 100k users/year

The real question: What's your realistic growth trajectory?
```

## Configuration

Create `~/.claude/debate.local.md`:

```yaml
---
max_rounds: 5
timeout_per_cli: 120
save_debate_logs: true
debate_log_path: "./debate-logs"
adr_path: "./docs/decisions"
skeptical_of_early_agreement: true
---
```

## Capability Levels

| External CLIs | Status | Quality |
|---------------|--------|---------|
| 0 | DISABLED | Won't run - no genuine diversity |
| 1 | MINIMAL | Functional, limited perspectives |
| 2 | FUNCTIONAL | Good coverage |
| 3+ | OPTIMAL | Maximum adversarial pressure |

## Universal Application

Works for ANY decision:
- Code architecture
- Business strategy
- Product features
- Technical tradeoffs
- Writing and content
- Life decisions

## Academic Foundation

Inspired by:
- **Irving et al. (2018)** - "AI safety via debate" - Scalable oversight via adversarial AI
- **Adversarial-spec** - Multi-LLM consensus for specifications
- **Anthropic alignment research** - Debate as verification mechanism

## Plugin Structure

```
debate/
├── .claude-plugin/plugin.json
├── SKILL.md
├── README.md
├── commands/
│   ├── debate.md
│   ├── doctor.md
│   └── adr.md
├── agents/
│   ├── challenger-gemini.md
│   ├── challenger-codex.md
│   ├── challenger-qwen.md
│   └── assumption-extractor.md
├── templates/
│   ├── tradeoff-document.md
│   └── adr-template.md
└── references/
    ├── debate-protocol.md
    └── cli-invocation.md
```

## License

MIT
