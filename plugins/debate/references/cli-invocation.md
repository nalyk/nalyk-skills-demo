# CLI Invocation Reference

## Supported CLIs

| CLI | Package | Auth | Free Tier | Headless Flag |
|-----|---------|------|-----------|---------------|
| Gemini | `@google/gemini-cli` | Google OAuth | 1000 req/day | `--yolo` |
| Codex | `@openai/codex` | ChatGPT Plus | Subscription | `--full-auto` |
| Qwen | `@qwen-code/qwen-code` | Qwen OAuth | 2000 req/day | `--yolo` |

---

## Installation Commands

### Gemini CLI

```bash
npm i -g @google/gemini-cli

# Authenticate
gemini auth login
```

### Codex CLI

```bash
npm i -g @openai/codex

# Authenticate (requires ChatGPT Plus)
codex auth
```

### Qwen CLI

```bash
npm i -g @qwen-code/qwen-code

# Authenticate
qwen auth login
```

---

## Headless Invocation Patterns

### Gemini

```bash
# Basic invocation (positional prompt)
gemini "Your prompt here" --yolo

# With timeout
timeout 120 gemini "Your prompt here" --yolo 2>/dev/null

# Error handling
timeout 120 gemini "..." --yolo 2>/dev/null || echo '{"error":"gemini_failed"}'
```

**Flags:**
- Positional prompt - First argument is the prompt (non-interactive mode)
- `--yolo` - Skip confirmation prompts (for automation)
- Note: `--output-format json` is deprecated, CLI returns plain text

### Codex

```bash
# Basic invocation (exec subcommand for non-interactive)
codex exec "Your prompt here" --full-auto

# With timeout (NOTE: redirect to file due to TUI output quirk)
CODEX_OUT="/tmp/codex-out-$$.txt"
cd /tmp && timeout 120 codex exec "Your prompt here" --full-auto --skip-git-repo-check > "$CODEX_OUT" 2>&1
cat "$CODEX_OUT"
rm -f "$CODEX_OUT"

# Error handling
CODEX_OUT="/tmp/codex-out-$$.txt"
cd /tmp && timeout 120 codex exec "..." --full-auto --skip-git-repo-check > "$CODEX_OUT" 2>&1 || echo '{"error":"codex_failed"}'
```

**Flags:**
- `exec` - Non-interactive subcommand (required for headless operation)
- Positional prompt - First argument after `exec` is the prompt
- `--full-auto` - Full automation mode (no confirmations, sandboxed)
- `--skip-git-repo-check` - Required when running from /tmp or non-git directories

**IMPORTANT:** Codex CLI uses a TUI that doesn't pipe correctly. Always redirect to a file first, then read the file.

### Qwen

```bash
# Basic invocation
qwen -p "Your prompt here" --yolo

# With timeout
timeout 120 qwen -p "Your prompt here" --yolo 2>/dev/null

# Error handling
timeout 120 qwen -p "..." --yolo 2>/dev/null || echo '{"error":"qwen_failed"}'
```

**Flags:**
- `-p "prompt"` - Non-interactive prompt mode
- `--yolo` - Skip confirmation prompts
- Note: `--output-format json` is deprecated, CLI returns plain text

---

## Detection Commands

### Check if CLI is installed

```bash
command -v gemini &> /dev/null && echo "installed" || echo "missing"
command -v codex &> /dev/null && echo "installed" || echo "missing"
command -v qwen &> /dev/null && echo "installed" || echo "missing"
```

### Get version

```bash
gemini --version 2>/dev/null | head -1
codex --version 2>/dev/null | head -1
qwen --version 2>/dev/null | head -1
```

### Test authentication

```bash
# Quick auth test - ask for a specific response
timeout 30 gemini "respond with exactly: DEBATE_AUTH_OK" --yolo 2>/dev/null | grep -q "DEBATE_AUTH_OK"

# Codex requires file redirect due to TUI output
CODEX_OUT="/tmp/codex-auth-$$.txt"
cd /tmp && timeout 60 codex exec "respond with exactly: DEBATE_AUTH_OK" --full-auto --skip-git-repo-check > "$CODEX_OUT" 2>&1
grep -q "DEBATE_AUTH_OK" "$CODEX_OUT"; rm -f "$CODEX_OUT"

timeout 30 qwen -p "respond with exactly: DEBATE_AUTH_OK" --yolo 2>/dev/null | grep -q "DEBATE_AUTH_OK"
```

---

## Expected JSON Response Format

All CLIs should return JSON when using `--output-format json`. The debate plugin expects this structure:

```json
{
  "verdict": "agree | partial | disagree",
  "critique": "Specific objections",
  "evidence": "Concrete example",
  "alternative": "What they recommend instead",
  "confidence": "high | medium | low",
  "objection_strength": "strong | moderate | minor",
  "assumptions_challenged": ["assumption 1", "assumption 2"]
}
```

### Handling Non-JSON Responses

If a CLI returns plain text instead of JSON, wrap it:

```json
{
  "raw_response": "The plain text response",
  "parse_error": true,
  "model": "gemini"
}
```

---

## Timeout Handling

Default timeout: 120 seconds per CLI invocation.

```bash
# Using timeout command
timeout 120 gemini "..." --yolo

# Check exit code
if [ $? -eq 124 ]; then
    echo "Timeout occurred"
fi
```

---

## Parallel Execution

For Phase 2 (parallel challenge), run all CLIs simultaneously:

```bash
# Launch in background
gemini "..." --yolo > /tmp/debate-gemini.json 2>&1 &
PID_GEMINI=$!

# Codex must run from /tmp with skip-git-repo-check
(cd /tmp && codex exec "..." --full-auto --skip-git-repo-check > /tmp/debate-codex.json 2>&1) &
PID_CODEX=$!

qwen -p "..." --yolo > /tmp/debate-qwen.json 2>&1 &
PID_QWEN=$!

# Wait for all
wait $PID_GEMINI $PID_CODEX $PID_QWEN

# Collect results
cat /tmp/debate-gemini.json
cat /tmp/debate-codex.json
cat /tmp/debate-qwen.json
```

---

## Model-Specific Notes

### Gemini

- 1M token context window
- Good for large codebase analysis
- May be verbose in responses
- Free tier resets daily

### Codex

- Powered by GPT-5 (o3/o4-mini)
- Strong reasoning capabilities
- Requires paid subscription
- May have different JSON formatting

### Qwen

- Forked from Gemini CLI (same flags)
- Powered by Qwen3-Coder (480B params)
- 256K-1M token context
- Generous free tier (2000 req/day)

---

## Troubleshooting

### "command not found"

CLI not installed. Run:
```bash
npm i -g @google/gemini-cli  # or codex/qwen
```

### "auth failed" or empty response

Need to authenticate:
```bash
gemini auth login
codex auth
qwen auth login
```

### Timeout on every request

- Check internet connection
- Check if CLI service is down
- Increase timeout in settings

### JSON parse error

- CLI may be returning plain text
- Check if `--output-format json` is supported in current version
- Update CLI to latest version
