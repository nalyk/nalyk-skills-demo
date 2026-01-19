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
# Basic invocation
gemini -p "Your prompt here" --output-format json --yolo

# With timeout
timeout 120 gemini -p "Your prompt here" --output-format json --yolo 2>/dev/null

# Error handling
timeout 120 gemini -p "..." --output-format json --yolo 2>/dev/null || echo '{"error":"gemini_failed"}'
```

**Flags:**
- `-p "prompt"` - Non-interactive prompt mode
- `--output-format json` - JSON output for parsing
- `--yolo` - Skip confirmation prompts (for automation)

### Codex

```bash
# Basic invocation
codex -p "Your prompt here" --output-format json --full-auto

# With timeout
timeout 120 codex -p "Your prompt here" --output-format json --full-auto 2>/dev/null

# Error handling
timeout 120 codex -p "..." --output-format json --full-auto 2>/dev/null || echo '{"error":"codex_failed"}'
```

**Flags:**
- `-p "prompt"` - Non-interactive prompt mode
- `--output-format json` - JSON output for parsing
- `--full-auto` - Full automation mode (no confirmations)

### Qwen

```bash
# Basic invocation
qwen -p "Your prompt here" --output-format json --yolo

# With timeout
timeout 120 qwen -p "Your prompt here" --output-format json --yolo 2>/dev/null

# Error handling
timeout 120 qwen -p "..." --output-format json --yolo 2>/dev/null || echo '{"error":"qwen_failed"}'
```

**Flags:**
- `-p "prompt"` - Non-interactive prompt mode (same as Gemini, it's a fork)
- `--output-format json` - JSON output for parsing
- `--yolo` - Skip confirmation prompts

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
timeout 30 gemini -p "respond with exactly: DEBATE_AUTH_OK" --yolo 2>/dev/null | grep -q "DEBATE_AUTH_OK"

timeout 30 codex -p "respond with exactly: DEBATE_AUTH_OK" --full-auto 2>/dev/null | grep -q "DEBATE_AUTH_OK"

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
timeout 120 gemini -p "..." --output-format json --yolo

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
gemini -p "..." --output-format json --yolo > /tmp/debate-gemini.json 2>&1 &
PID_GEMINI=$!

codex -p "..." --output-format json --full-auto > /tmp/debate-codex.json 2>&1 &
PID_CODEX=$!

qwen -p "..." --output-format json --yolo > /tmp/debate-qwen.json 2>&1 &
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
