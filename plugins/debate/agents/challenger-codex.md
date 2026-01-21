---
name: challenger-codex
description: Invokes Codex CLI from debate workspace. Persona loaded from AGENTS.md context file.
tools: Bash
---

# Codex Challenger Agent

Minimal orchestration wrapper. **Persona and critique style defined in workspace/AGENTS.md**.

## Your Role

1. Receive challenge task from orchestrator
2. Execute Codex CLI from workspace directory (where AGENTS.md exists)
3. Return raw response - DO NOT interpret or filter

## Input Expected

- `WORKSPACE_PATH`: Path to debate workspace (contains AGENTS.md)
- `CLAUDE_POSITION`: The position to challenge
- `ROUND`: Current debate round
- `PREVIOUS_CONTEXT`: Prior debate history (if round > 1)

## Prompt Construction

The prompt contains ONLY the task. Persona comes from AGENTS.md.

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
CODEX_OUT="/tmp/codex-debate-$$.txt"

# CRITICAL: Run from workspace so Codex discovers AGENTS.md
cd "$WORKSPACE_PATH"

timeout 120 codex exec "$PROMPT" --full-auto --skip-git-repo-check > "$CODEX_OUT" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo '{"error": "codex_invocation_failed", "model": "codex"}'
else
    cat "$CODEX_OUT"
fi
rm -f "$CODEX_OUT"
```

## Output

Return raw response from Codex. Do not modify.

If non-JSON, wrap:
```json
{
  "raw_response": "[response]",
  "parse_error": true,
  "model": "codex"
}
```

## Error Handling

| Error | Response |
|-------|----------|
| Timeout | `{"error": "timeout", "model": "codex"}` |
| Auth failure | `{"error": "auth_failed", "model": "codex"}` |
| CLI not found | `{"error": "cli_not_found", "model": "codex"}` |
| AGENTS.md missing | `{"error": "context_file_missing", "model": "codex"}` |

## Codex-Specific Notes

- Uses `exec` subcommand for non-interactive mode
- Uses `--full-auto` (not `--yolo`)
- TUI output requires file redirect
- Requires ChatGPT Plus subscription
