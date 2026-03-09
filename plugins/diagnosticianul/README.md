# diagnosticianul

Elite Senior Principal Engineer persona for Claude Code. Four specialized diagnostic protocols for code review, system design, UI analysis, and algorithmic debugging.

Operates in Romanian. Accepts input in any language.

## Installation

```bash
/plugin install diagnosticianul@nalyk-skills-demo
```

## Protocols

| Protocol | Trigger | Function |
|----------|---------|----------|
| `protocol-critic` | Code snippets, PRs, "review this" | Forensic code autopsy. Finds structural defects, antipatterns, dead code. |
| `protocol-architect` | "Design a system", "how to structure" | System design with rigid planning. Refuses underspecified requests. |
| `protocol-visual` | UI work, CSS, "fix this layout" | UI and frontend quality enforcement. Fights default design. |
| `protocol-core` | Algorithms, logic errors, "fix this bug" | Algorithmic debugging and optimization. Surgical precision. |

The main `diagnosticianul` skill triages incoming requests and routes to the correct protocol.

## Auto-activation

Activates on: code snippets, pull requests, system design questions, UI/frontend issues, algorithm problems, performance bugs, or any request requiring technical judgment.

Keywords: "code review", "debug this", "design a system", "architecture review", "fix this UI", "optimize this", "what's wrong with this code", "fix bug", "logic error", "CSS issue", "frontend review".

## Structure

```
diagnosticianul/
├── .claude-plugin/plugin.json
└── skills/
    ├── diagnosticianul/
    │   ├── SKILL.md                    # Triage and routing
    │   └── references/
    │       └── communication-protocol.md
    ├── protocol-critic/SKILL.md        # Code autopsy
    ├── protocol-architect/SKILL.md     # System design
    ├── protocol-visual/SKILL.md        # UI enforcement
    └── protocol-core/SKILL.md          # Algorithmic surgery
```

## License

MIT
