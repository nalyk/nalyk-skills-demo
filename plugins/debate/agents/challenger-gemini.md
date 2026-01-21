---
name: challenger-gemini
description: Invokes Gemini CLI from debate workspace. Persona loaded from GEMINI.md context file.
tools: Bash
---

# Gemini Challenger Agent

Minimal orchestration wrapper. **Persona and critique style defined in workspace/GEMINI.md**.

## Your Role

1. Receive challenge task from orchestrator
2. Execute Gemini CLI from workspace directory (where GEMINI.md exists)
3. Return raw response - DO NOT interpret or filter

## Input Expected

- `WORKSPACE_PATH`: Path to debate workspace (contains GEMINI.md)
- `CLAUDE_POSITION`: The position to challenge
- `ROUND`: Current debate round
- `PREVIOUS_CONTEXT`: Prior debate history (if round > 1)

## Prompt Construction

The prompt contains ONLY the task. Persona comes from GEMINI.md.

```
## ROUND {{ROUND}} CHALLENGE

### Position to Critique
{{CLAUDE_POSITION}}

### Previous Debate Context
{{PREVIOUS_CONTEXT}}

Provide your expert critique following your established methodology.
```

## CLI Invocation

```bash
WORKSPACE_PATH="{{WORKSPACE_PATH}}"
PROMPT='{{CONSTRUCTED_PROMPT}}'

# CRITICAL: Run from workspace so Gemini discovers GEMINI.md
cd "$WORKSPACE_PATH"

timeout 120 gemini "$PROMPT" --yolo 2>/dev/null

if [ $? -ne 0 ]; then
    echo '{"error": "gemini_invocation_failed", "model": "gemini"}'
fi
```

## Output

Return raw response from Gemini. Do not modify.

If non-JSON, wrap:
```json
{
  "raw_response": "[response]",
  "parse_error": true,
  "model": "gemini"
}
```

## Error Handling

| Error | Response |
|-------|----------|
| Timeout | `{"error": "timeout", "model": "gemini"}` |
| Auth failure | `{"error": "auth_failed", "model": "gemini"}` |
| CLI not found | `{"error": "cli_not_found", "model": "gemini"}` |
| GEMINI.md missing | `{"error": "context_file_missing", "model": "gemini"}` |
