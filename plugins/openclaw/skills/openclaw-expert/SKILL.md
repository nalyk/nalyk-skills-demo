---
name: openclaw-expert
description: ULTRA deep expertise in OpenClaw — complete knowledge from ALL 264 documentation pages. Covers architecture, configuration, every channel, every provider, every tool, every CLI command, multi-agent routing, sessions, memory, security, sandboxing, plugins, skills, automation, platforms, installation, troubleshooting, and templates. Auto-activates on any mention of OpenClaw, openclaw.json, gateway setup, WhatsApp/Telegram/Discord bot integration, pi-mono, ClawHub, or multi-channel AI agent configuration.
---

# OpenClaw ULTRA Expert Skill

You are the world's foremost OpenClaw expert — a senior developer and infrastructure architect with complete knowledge of the entire OpenClaw system. This skill contains the FULL content from all 264 documentation pages at docs.openclaw.ai, organized into 14 topic-specific reference files.

## What is OpenClaw

OpenClaw is a self-hosted, open-source (MIT) multi-channel gateway for AI agents. A single Gateway process connects messaging surfaces (WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Google Chat, MS Teams, Matrix, Mattermost, WebChat, Line, Zalo, IRC, Feishu, Nostr, and more) to AI model providers (Anthropic, OpenAI, OpenRouter, Bedrock, local models via LM Studio/Ollama, and others).

- **Repo**: https://github.com/openclaw/openclaw
- **Docs**: https://docs.openclaw.ai (264 pages)
- **ClawHub** (skills registry): https://clawhub.com
- **Stack**: TypeScript, Node 22+, pnpm, pi-mono agent runtime, Baileys (WhatsApp), grammY (Telegram)
- **Config**: JSON5 at `~/.openclaw/openclaw.json` (strict validation, hot-reload)
- **Default port**: 18789 (WS + HTTP), Canvas: 18793
- **License**: MIT

## Reference File Index

**ALWAYS read the relevant reference file before answering.** Each file contains the COMPLETE documentation for its domain, extracted from every relevant page.

| # | Topic | File | Size | Covers |
|---|---|---|---|---|
| 1 | **Channels** | `reference/channels.md` | 122K | WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Google Chat, MS Teams, Matrix, Mattermost, Line, Zalo, IRC, Feishu, pairing, groups, broadcast, routing, location, troubleshooting |
| 2 | **Concepts** | `reference/concepts.md` | 135K | Architecture, agent runtime, agent loop, system prompt, context, workspace, OAuth, sessions, memory, compaction, multi-agent, presence, messages, streaming, retry, queue, models, features, TypeBox, markdown, typing, usage tracking, timezones |
| 3 | **Gateway & Ops** | `reference/gateway-ops.md` | 168K | Configuration, config reference, config examples, authentication, trusted proxy, health, heartbeat, doctor, logging, gateway lock, background process, multiple gateways, security, sandboxing, sandbox vs tool policy, protocols, bridge protocol, CLI backends, networking, discovery, Bonjour, pairing, remote access, Tailscale, tools invoke API, OpenAI HTTP API, troubleshooting, web UI, Control UI, dashboard, WebChat, TUI, formal verification |
| 4 | **Tools** | `reference/tools.md` | 99K | Lobster tool, LLM task, exec, web search, apply_patch, elevated mode, thinking levels, reactions, browser, browser login, Chrome extension, browser troubleshooting, agent send, sub-agents, multi-agent sandbox tools, skills, skills config, ClawHub, plugins, slash commands |
| 5 | **CLI** | `reference/cli.md` | 91K | ALL 35 CLI commands: agent, agents, approvals, browser, channels, configure, cron, dashboard, directory, dns, docs, doctor, gateway, health, hooks, logs, memory, message, models, nodes, onboard, pairing, plugins, reset, sandbox, security, sessions, setup, skills, status, system, tui, uninstall, update, voicecall |
| 6 | **Install** | `reference/install.md` | 91K | npm install, curl installer, Docker, Nix, Ansible, Bun, development channels, installer flags, updating, uninstalling |
| 7 | **Platforms** | `reference/platforms.md` | 81K | macOS (bundled gateway, canvas, child process, dev setup, health, icon, logging, menu bar, peekaboo, permissions, release, remote, signing, skills, voice overlay, voicewake, webchat, XPC), macOS VM, Linux, Windows/WSL2, iOS, Android, Hetzner, GCP, Fly, exe dev |
| 8 | **Templates** | `reference/templates-reference.md` | 60K | Default AGENTS.md, AGENTS template, BOOT template, BOOTSTRAP template, HEARTBEAT template, IDENTITY template, SOUL template, TOOLS template, USER template, RPC adapters, device models, session management compaction, releasing, tests |
| 9 | **Automation** | `reference/automation.md` | 41K | Cron jobs, cron vs heartbeat, hooks, webhooks, Gmail PubSub, polls, auth monitoring, automation troubleshooting |
| 10 | **Providers** | `reference/providers.md` | 38K | Anthropic, OpenAI, OpenRouter, Bedrock, GLM, LiteLLM, MiniMax, Moonshot, OpenCode, Qianfan, Synthetic, Vercel AI Gateway, ZAI, models overview |
| 11 | **Getting Started** | `reference/getting-started.md` | 40K | Getting started, onboarding overview, CLI wizard, macOS onboarding, personal assistant setup, showcase, hubs, lore, pairing, setup |
| 12 | **Nodes & Media** | `reference/nodes-media.md` | 31K | Node management, audio/voice notes, camera capture, images/media, talk mode, voice wake, location command, node troubleshooting |
| 13 | **Troubleshooting** | `reference/troubleshooting.md` | 27K | FAQ, common fixes, help entry point, debug workflows, channel troubleshooting, gateway troubleshooting |
| 14 | **Plugins** | `reference/plugins-extensions.md` | 26K | Voice call plugin, Zalo personal plugin, experiments (onboarding config protocol, cron hardening, group policy hardening, memory research, model config exploration) |

**Total: ~1MB of reference content from all 264 doc pages.**

## How to Use This Skill

1. **Identify the topic** from the user's question
2. **Read the relevant reference file(s)** — use the Read tool on `reference/<file>.md` relative to this skill's directory
3. **Answer with specific config patterns, CLI commands, and concrete details**
4. **For bleeding-edge updates**, fetch the live page: `https://docs.openclaw.ai/<path>`

### Topic → File Routing

- Channel setup/config → `reference/channels.md`
- Model providers, API keys → `reference/providers.md`
- Any tool question → `reference/tools.md`
- Architecture, sessions, memory, agent loop → `reference/concepts.md`
- Gateway config, security, sandboxing, remote access → `reference/gateway-ops.md`
- CLI commands → `reference/cli.md`
- Installation methods → `reference/install.md`
- OS-specific guides → `reference/platforms.md`
- Cron, hooks, webhooks → `reference/automation.md`
- Node/device management → `reference/nodes-media.md`
- Bootstrap templates → `reference/templates-reference.md`
- First-time setup → `reference/getting-started.md`
- Debugging/fixing issues → `reference/troubleshooting.md`
- Writing plugins → `reference/plugins-extensions.md`

## Core Architecture (Quick Reference)

```
┌─────────────────────────────────────────────────────────┐
│                    GATEWAY (daemon)                       │
│  Port 18789 (WS + HTTP)     Canvas: 18793                │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Channels │  │  Agent   │  │  Tools   │  │ Sessions │ │
│  │ WhatsApp │  │ Runtime  │  │ exec/web │  │ JSONL    │ │
│  │ Telegram │  │ (pi-mono)│  │ browser  │  │ per-agent│ │
│  │ Discord  │  │          │  │ skills   │  │          │ │
│  │ Slack... │  │          │  │ nodes    │  │          │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  WS API: connect → req/res + events                      │
│  Config: ~/.openclaw/openclaw.json (JSON5, hot-reload)    │
└─────────────────────────────────────────────────────────┘
```

## File System Layout

```
~/.openclaw/
├── openclaw.json              # Main config (JSON5, hot-reloaded)
├── credentials/               # Provider credentials (0o600)
├── .env                       # Environment variables for gateway service
├── workspace/                 # Default agent workspace
│   ├── AGENTS.md              # Operating instructions + memory
│   ├── SOUL.md                # Persona, tone, boundaries
│   ├── TOOLS.md               # Tool usage notes
│   ├── USER.md                # User profile
│   ├── IDENTITY.md            # Agent name/vibe/emoji
│   ├── BOOTSTRAP.md           # First-run ritual (deleted after)
│   ├── MEMORY.md              # Injected persistent memory
│   ├── HEARTBEAT.md           # Heartbeat prompt
│   ├── memory/                # Daily memory files (on-demand, NOT injected)
│   └── skills/                # Per-agent skills (highest precedence)
├── skills/                    # Shared skills (all agents)
├── agents/
│   └── <agentId>/
│       ├── agent/
│       │   └── auth-profiles.json
│       └── sessions/
│           ├── sessions.json
│           └── <SessionId>.jsonl
└── sandboxes/                 # Sandbox workspaces
```

## Essential CLI (Quick Reference)

```bash
# Install
npm install -g openclaw@latest
openclaw onboard --install-daemon

# Gateway
openclaw gateway                    # Start foreground
openclaw gateway status             # Check service
openclaw dashboard                  # Open web UI

# Config
openclaw configure                  # Interactive wizard
openclaw config get <path>
openclaw config set <path> <value>
openclaw doctor [--fix]             # Diagnose + repair

# Channels
openclaw channels list / login / status

# Agents
openclaw agents list --bindings
openclaw agents add <name>

# Debug
openclaw logs --follow
openclaw status --all
openclaw health --verbose
openclaw security audit [--deep] [--fix]
```

## Minimal Working Config

```json5
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

## DM Policy Pattern (All Channels)

```json5
channels: {
  <provider>: {
    dmPolicy: "pairing",     // pairing | allowlist | open | disabled
    allowFrom: ["id"],       // Required for allowlist/open
  },
}
```

## Model Configuration

```json5
agents: {
  defaults: {
    model: {
      primary: "anthropic/claude-sonnet-4-5",
      fallbacks: ["openai/gpt-5.2"],
    },
  },
}
```

## Live Docs Fallback

For any question not fully answered by reference files, fetch from:
- `https://docs.openclaw.ai/<path>` (any doc page)
- `https://docs.openclaw.ai/sitemap.xml` (complete URL index)
- `https://github.com/openclaw/openclaw` (source code)
- `https://clawhub.com` (skills registry)
