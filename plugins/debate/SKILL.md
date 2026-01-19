---
name: debate
description: >-
  Multi-model adversarial debate where Claude defends positions against external
  CLI models (Gemini, Codex, Qwen). Use when facing complex decisions, wanting
  to expose blind spots, or needing documented reasoning for tradeoffs.

  Auto-triggers: "debate this", "challenge my thinking", "what am I missing",
  "devil's advocate", "stress test this idea", "poke holes", "second opinion",
  "validate this decision", "am I wrong about"
---

# Debate System

## What This Does

Claude forms a position, then external AI models (Gemini, Codex, Qwen) challenge it through structured adversarial debate. Claude must defend, update, or synthesize based on valid critiques.

**This is NOT Claude debating itself.** Different models = different training = different blind spots = genuine value.

## Requirements

**Minimum: 1 external CLI installed and authenticated.**

Run `/debate:doctor` to check system health.

Supported CLIs:
- `gemini` - @google/gemini-cli (free: 1000 req/day)
- `codex` - @openai/codex (requires ChatGPT Plus)
- `qwen` - @qwen-code/qwen-code (free: 2000 req/day)

**Refuses to run with Claude-only.** Claude debating itself is theater, not debate.

## Commands

| Command | Purpose |
|---------|---------|
| `/debate <topic>` | Full adversarial debate on any topic |
| `/debate:doctor` | Check CLI health and authentication |
| `/debate:adr <topic>` | Debate with formal ADR output for important decisions |

## The Hybrid Protocol

1. **Claude forms position** on the topic
2. **Parallel challenge** - All external models critique simultaneously
3. **Consensus check** - If all agree → fast exit
4. **Sequential confrontation** - If disagreement, models respond to each other
5. **Iterate** until consensus OR max rounds
6. **Assumption extraction** - Surface WHY positions differ
7. **Output** - Consensus OR structured tradeoff document

## When To Use

- Complex decisions with no obvious answer
- Suspecting blind spots in your thinking
- Needing documented reasoning for team/future reference
- Wanting genuine pushback, not "yes-man" AI
- Architecture decisions, strategy, any high-stakes choice

## The Core Value

**Disagreement is signal, not failure.**

When models can't agree, the output isn't "we failed" - it's a structured tradeoff document exposing:
- What each option assumes
- When each option is correct
- The hidden assumptions causing the split

This transforms "who's right?" into "what would have to be true for each to be right?"

## Settings

Configure in `~/.claude/debate.local.md`:

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

## Universal Application

Works for ANY decision:
- Code architecture
- Business strategy
- Product features
- Technical tradeoffs
- Writing and content
- Life decisions

The protocol adapts to domain automatically.
