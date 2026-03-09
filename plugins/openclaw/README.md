# openclaw

Deep expertise plugin for OpenClaw -- the self-hosted, open-source multi-channel AI gateway. Knowledge extracted from all 279 documentation pages at docs.openclaw.ai.

## Installation

```bash
/plugin install openclaw@nalyk-skills-demo
```

No external dependencies. This is a pure knowledge plugin.

## What It Knows

Complete coverage of the OpenClaw system:

| Topic | Reference File | Content |
|-------|---------------|---------|
| Channels | `channels.md` | WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Google Chat, MS Teams, Matrix, Mattermost, Line, Zalo, IRC, Feishu, BlueBubbles, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch |
| Architecture | `concepts.md` | Agent runtime, agent loop, sessions, memory, compaction, multi-agent, streaming, retry, queue |
| Gateway & Ops | `gateway-ops.md` | Configuration, authentication, security, sandboxing, networking, remote access, Tailscale, WebChat |
| Tools | `tools.md` | Lobster tool, LLM task, exec, browser, agent send, sub-agents, skills, ClawHub, plugins |
| CLI | `cli.md` | All 44 CLI commands |
| Installation | `install.md` | npm, curl, Docker, Nix, Ansible, Bun |
| Platforms | `platforms.md` | macOS, Linux, Windows/WSL2, iOS, Android, Hetzner, GCP, Fly |
| Templates | `templates-reference.md` | AGENTS.md, BOOT, BOOTSTRAP, HEARTBEAT, IDENTITY, SOUL, TOOLS, USER templates |
| Automation | `automation.md` | Cron, hooks, webhooks, Gmail PubSub |
| Providers | `providers.md` | Anthropic, OpenAI, OpenRouter, Bedrock, Mistral, LiteLLM, local models |
| Getting Started | `getting-started.md` | Onboarding, CLI wizard, setup |
| Nodes & Media | `nodes-media.md` | Audio, voice, camera, images, talk mode |
| Troubleshooting | `troubleshooting.md` | FAQ, common fixes, debug workflows |
| Plugins | `plugins-extensions.md` | Voice call, community plugins, experiments |

Total: ~1.4MB of reference content across 14 files.

## How It Works

The skill reads the relevant reference file based on the user's question, then answers with specific configuration patterns, CLI commands, and concrete details. No guessing.

## Auto-activation

Triggers on: OpenClaw, `openclaw.json`, gateway setup, WhatsApp/Telegram/Discord bot integration, pi-mono, ClawHub, multi-channel AI agent configuration.

## Structure

```
openclaw/
├── .claude-plugin/plugin.json
└── skills/
    └── openclaw-expert/
        ├── SKILL.md
        └── reference/
            ├── automation.md
            ├── channels.md
            ├── cli.md
            ├── concepts.md
            ├── gateway-ops.md
            ├── getting-started.md
            ├── install.md
            ├── nodes-media.md
            ├── platforms.md
            ├── plugins-extensions.md
            ├── providers.md
            ├── templates-reference.md
            ├── tools.md
            └── troubleshooting.md
```

## License

MIT
