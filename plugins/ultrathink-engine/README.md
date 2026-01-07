# ULTRATHINK Engine

Deep multi-perspective analysis protocol that forces thorough thinking and prevents superficial answers.

## Features

- **4-Phase Analysis**: Problem decomposition, multi-perspective analysis, brutal honesty check, validation checkpoint
- **Anti-Superficiality Rules**: Forbids one-liners, requires reasoning chains
- **Assumption Tracking**: Explicit confidence levels (HIGH/MED/LOW)
- **Failure Mode Analysis**: Edge cases and production concerns

## Triggers

- Say "ULTRATHINK" explicitly
- Ask for "brutally honest" feedback
- Request "all points of view"
- Use words like "rigorous" or "meticulous"
- Say "maximum effectivity"

## Installation

Add to your Claude Code plugins:

```bash
claude plugins add nalyk-skills/ultrathink-engine
```

## Usage

Simply include trigger words in your request:

```
ULTRATHINK: How should I architect this authentication system?
```

Or:

```
Give me a brutally honest assessment of this code structure.
```

## Output Format

Every ULTRATHINK response ends with a summary:

```
ULTRATHINK SUMMARY
==================
Goal: [one sentence]
Approach: [chosen approach with justification]
Assumptions: [list]
Risks: [list]
Verification needed: [list]

Proceed? Or correct my understanding?
```

## License

MIT
