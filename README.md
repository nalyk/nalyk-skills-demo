# nalyk-skills

Personal Claude Code plugin marketplace. 10 plugins covering automation, orchestration, code review, debugging, multi-model debate, SEO analysis, Flutter development, OpenClaw infrastructure, and philosophical reasoning.

## Installation

Add the marketplace:

```bash
/plugin marketplace add nalyk/nalyk-skills-demo
```

Install individual plugins:

```bash
/plugin install <plugin-name>@nalyk-skills-demo
```

## Plugins

### auto-ralph (v2.0.0)

Deterministic Ralph Loop activation. A `UserPromptSubmit` hook scores every incoming task (0-4) and auto-invokes the Ralph Loop when the score hits the threshold.

```bash
/plugin install auto-ralph@nalyk-skills-demo
```

**Triggers:** "ralph this", "auto ralph", "loop it" -- or auto-detects bug fixes, features, and refactoring tasks (score >= 3).

**Configuration:** `~/.claude/auto-ralph.local.md`

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_iterations | 25 | Max Ralph Loop iterations |
| score_threshold | 3 | Min score for activation |
| skip_explore_for_score | 4 | Skip Explore phase at this score |
| default_language | ro | Output language (ro/en/ru) |
| auto_execute | false | Skip confirmation prompt |
| docker_analysis | true | Include Docker context |

Output: Romanian. Input: ro/en/ru/mixed.

---

### orchestrator (v1.0.0)

Multi-agent task decomposition and parallel execution. Breaks complex tasks into workstreams, routes them to appropriate agents (Explore, Plan, general-purpose), and synthesizes results.

```bash
/plugin install orchestrator@nalyk-skills-demo
```

**Commands:**

| Command | Purpose |
|---------|---------|
| `/orchestrate <task>` | Full decomposition + parallel execution + synthesis |
| `/parallel <tasks...>` | Quick parallel launch without decomposition |
| `/plan-only <task>` | Preview execution plan without running |

**Auto-detects:** "research and implement", "comprehensive review", multiple AND-connected tasks, migrations, multi-file refactoring.

**Configuration:** `~/.claude/orchestrator.local.md`

---

### audit-agent (v1.0.0)

Three audit frameworks: Steve Jobs (design simplification, 13 questions), George Carlin (BS detection, 13 questions), Vibe (engineering quality, 20 scored metrics).

```bash
/plugin install audit-agent@nalyk-skills-demo
```

**Commands:**

| Command | Purpose |
|---------|---------|
| `/jobs-audit <target>` | Design thinking -- simplification, elegance, restraint |
| `/carlin-audit <target>` | BS detection -- hidden agendas, euphemisms, contradictions |
| `/vibe-audit <target>` | Engineering quality -- 20 metrics, 0-5 scale each |
| `/multi-audit <target>` | Run multiple frameworks + cross-reference synthesis |

**Auto-detects:** "simplify", "too complex", "BS", "jargon", "code review", "production ready", "vibe check".

---

### debate (v1.0.0)

Multi-model adversarial debate. Claude defends a position against external CLI models (Gemini, Codex, Qwen). Produces tradeoff documents when models disagree, exposing hidden assumptions.

Refuses to run with Claude-only. Requires at least 1 external CLI.

```bash
/plugin install debate@nalyk-skills-demo
```

**Prerequisites -- at least one:**

| CLI | Install | Free Tier |
|-----|---------|-----------|
| Gemini | `npm i -g @google/gemini-cli` | 1000 req/day |
| Codex | `npm i -g @openai/codex` | ChatGPT Plus |
| Qwen | `npm i -g @qwen-code/qwen-code` | 2000 req/day |

**Commands:**

| Command | Purpose |
|---------|---------|
| `/debate <topic>` | Full adversarial debate |
| `/debate:doctor` | Check CLI availability and auth |
| `/debate:adr <topic>` | Debate with formal Architecture Decision Record output |

**Configuration:** `~/.claude/debate.local.md`

---

### diagnosticianul (v2026.1.0)

Elite Senior Principal Engineer persona. Four specialized diagnostic protocols for code review, system design, UI analysis, and algorithmic debugging. Romanian-flavored.

```bash
/plugin install diagnosticianul@nalyk-skills-demo
```

**Protocols:**

| Protocol | Trigger | Function |
|----------|---------|----------|
| protocol-critic | Code snippets, PRs | Forensic code autopsy |
| protocol-architect | "Design a system" | Rigid system planning |
| protocol-visual | UI/CSS/frontend | UI quality enforcement |
| protocol-core | Algorithms, bugs | Surgical debugging |

**Auto-detects:** code snippets, PRs, system design, UI issues, algorithm problems, performance bugs.

---

### organon (v1.0.0)

Philosophical reasoning engine. 62 principles from 20 philosophers applied as a decision engine and code review framework. Based on [Organon](https://gitlab.com/lightcyphers-open/organon) by Lightcyphers SRL.

```bash
/plugin install organon@nalyk-skills-demo
```

**Commands:**

| Command | Purpose |
|---------|---------|
| `/organon` | Auto-detect mode and depth from context |
| `/organon:decide <topic>` | Explicit decision analysis |
| `/organon:review <path>` | Philosophical code review |

**Depth levels:** quick (1 principle), standard (multiple principles), deep (full 22-step protocol + Summa Method objections).

**Philosophers:** Aristotle, Aquinas, Kant, Machiavelli, Peirce, Plato, Poincare, Popper, Seneca, Stoics, Swinburne, Wittgenstein, plus Leibniz, Boole, Frege, Godel, Turing, Shannon, Church, Marcus Aurelius, Epictetus.

**License:** CC-BY-SA-4.0

---

### seo-skill (v2.2.0)

Deterministic SEO analysis engine. 98 atomic checks across 7 categories, async multi-page crawler, real Core Web Vitals via PageSpeed Insights, internal link graph with PageRank, auto-fix generation, audit history with regression detection.

```bash
/plugin install seo-skill@nalyk-skills-demo
```

**Post-install -- Python dependencies:**

```bash
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**Requirements:** Python 3.10+. Optional: `PAGESPEED_API_KEY` (free, 25K queries/day).

**Commands:**

| Command | Purpose |
|---------|---------|
| `/seo audit <url>` | Full site audit with deterministic scoring |
| `/seo fix <url>` | Generate ready-to-apply fixes |
| `/seo linkgraph <url>` | Internal link graph + PageRank |
| `/seo technical <url>` | Technical SEO (9 categories) |
| `/seo content <url>` | E-E-A-T and content quality |
| `/seo schema <url>` | Schema detection, validation, generation |
| `/seo page <url>` | Deep single-page analysis |
| `/seo history <url>` | Audit score history |
| `/seo monitor setup` | Generate CI/CD configs (GitHub Actions, GitLab CI) |

16 sub-skills, 7 parallel subagents, CI/CD integration.

---

### flutter (v1.0.0)

Expert-level Flutter and Dart development knowledge. Architecture decisions, state management (Riverpod, BLoC, Provider), project scaffolding, code templates, quality gates, CI/CD.

```bash
/plugin install flutter@nalyk-skills-demo
```

No external dependencies. Knowledge plugin.

**Auto-activates on:** Flutter, Dart, mobile app, widgets, Riverpod, BLoC, GoRouter, iOS/Android build issues.

**Reference material:** ~2,250 lines covering architecture patterns, state management comparison, code templates, and quality gates.

---

### openclaw (v1.1.0)

Deep expertise in OpenClaw (self-hosted multi-channel AI gateway). Complete knowledge from all 279 documentation pages. 14 reference files, ~1.4MB of indexed content.

```bash
/plugin install openclaw@nalyk-skills-demo
```

No external dependencies. Knowledge plugin.

**Coverage:** Architecture, all 20+ channels (WhatsApp, Telegram, Discord, Slack, Signal, etc.), all model providers, all 44 CLI commands, installation methods, gateway configuration, security, sandboxing, automation, platform-specific guides.

**Auto-activates on:** OpenClaw, `openclaw.json`, gateway setup, WhatsApp/Telegram/Discord bot integration, pi-mono, ClawHub.

---

### statusline (v2.0.0)

Powerline-style status bar for Claude Code. Shows model badge, git status, context window usage, vim mode.

```bash
/plugin install statusline@nalyk-skills-demo
```

**Requirements:** `jq`, terminal with Unicode support. Powerline font recommended.

Auto-configures via `SessionStart` hook. No manual setup needed. Restart Claude Code after install.

---

## Scripts

### scripts/enable-session-memory.py

Enables the unreleased Claude Code Session Memory feature by modifying local feature flags in `~/.claude.json`.

```bash
python3 scripts/enable-session-memory.py
# Restart Claude Code after running
```

**What it sets:**

| Setting | Server Default | Script Sets |
|---------|---------------|-------------|
| First trigger | 140,000 tokens | 10,000 tokens |
| Update interval | 10,000 tokens | 5,000 tokens |
| Tool call trigger | 5 calls | 3 calls |

Storage: `~/.claude/projects/{project}/{session-id}/session-memory/summary.md`

The server may reset these flags on sync. Re-run if session memory stops working.

Source: [decodeclaude.com/session-memory](https://decodeclaude.com/session-memory/)

## Plugin Details

See individual plugin READMEs in `plugins/<name>/` for full documentation.

## License

MIT (unless noted otherwise per plugin)
