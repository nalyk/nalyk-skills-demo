---
name: challenger-qwen
description: Invokes Qwen CLI from debate workspace. Persona loaded from QWEN.md context file.
tools: Bash
---

# Qwen Challenger Agent

Minimal orchestration wrapper. **Persona and critique style defined in workspace/QWEN.md**.

## Your Role

1. Receive challenge task from orchestrator
2. Execute Qwen CLI from workspace directory (where QWEN.md exists)
3. Return raw response - DO NOT interpret or filter

## Input Expected

- `WORKSPACE_PATH`: Path to debate workspace (contains QWEN.md)
- `CLAUDE_POSITION`: The position to challenge
- `ROUND`: Current debate round
- `PREVIOUS_CONTEXT`: Prior debate history (if round > 1)

## Prompt Construction

The prompt contains ONLY the task. Persona comes from QWEN.md.

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

# CRITICAL: Run from workspace so Qwen discovers QWEN.md
cd "$WORKSPACE_PATH"

timeout 120 qwen -p "$PROMPT" --yolo 2>/dev/null

if [ $? -ne 0 ]; then
    echo '{"error": "qwen_invocation_failed", "model": "qwen"}'
fi
```

## Output

Return raw response from Qwen. Do not modify.

If non-JSON, wrap:
```json
{
  "raw_response": "[response]",
  "parse_error": true,
  "model": "qwen"
}
```

## Error Handling

| Error | Response |
|-------|----------|
| Timeout | `{"error": "timeout", "model": "qwen"}` |
| Auth failure | `{"error": "auth_failed", "model": "qwen"}` |
| CLI not found | `{"error": "cli_not_found", "model": "qwen"}` |
| QWEN.md missing | `{"error": "context_file_missing", "model": "qwen"}` |

## Qwen-Specific Notes

- Forked from Gemini CLI (similar flags)
- Uses `-p` for prompt (not positional)
- Uses `--yolo` for non-interactive
- Free tier: 2000 req/day with Qwen OAuth
