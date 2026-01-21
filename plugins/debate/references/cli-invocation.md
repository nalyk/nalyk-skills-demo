# CLI Invocation Reference

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT FILE LOADING                          │
└─────────────────────────────────────────────────────────────────┘

  debate-workspace/
  ├── GEMINI.md    ──→  gemini reads at process start (Architect persona)
  ├── AGENTS.md    ──→  codex reads at process start (Operator persona)
  └── QWEN.md      ──→  qwen reads at process start (Adversary persona)

  CRITICAL: All CLIs must run FROM the workspace directory
            so they discover their respective context files.
```

## Supported CLIs

| CLI | Package | Context File | Auth | Free Tier | Headless Flag |
|-----|---------|--------------|------|-----------|---------------|
| Gemini | `@google/gemini-cli` | `GEMINI.md` | Google OAuth | 1000 req/day | `--yolo` |
| Codex | `@openai/codex` | `AGENTS.md` | ChatGPT Plus | Subscription | `--full-auto` |
| Qwen | `@qwen-code/qwen-code` | `QWEN.md` | Qwen OAuth | 2000 req/day | `--yolo` |

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

## Workspace-Based Invocation (NEW)

### Why Workspace Matters

Each CLI loads its context file **at process initialization**:
- Gemini discovers `GEMINI.md` in CWD
- Codex discovers `AGENTS.md` in CWD
- Qwen discovers `QWEN.md` in CWD

**You MUST `cd` to workspace before invoking CLI.**

### Gemini (from workspace)

```bash
WORKSPACE="/path/to/debates/001-topic"
PROMPT="Challenge this position: ..."

cd "$WORKSPACE"  # CRITICAL: Gemini reads GEMINI.md from CWD
timeout 120 gemini "$PROMPT" --yolo 2>/dev/null

if [ $? -ne 0 ]; then
    echo '{"error":"gemini_failed"}'
fi
```

**Context file loaded:** `$WORKSPACE/GEMINI.md`

### Codex (from workspace)

```bash
WORKSPACE="/path/to/debates/001-topic"
PROMPT="Challenge this position: ..."
CODEX_OUT="/tmp/codex-out-$$.txt"

cd "$WORKSPACE"  # CRITICAL: Codex reads AGENTS.md from CWD
timeout 120 codex exec "$PROMPT" --full-auto --skip-git-repo-check > "$CODEX_OUT" 2>&1

if [ $? -ne 0 ]; then
    echo '{"error":"codex_failed"}'
else
    cat "$CODEX_OUT"
fi
rm -f "$CODEX_OUT"
```

**Context file loaded:** `$WORKSPACE/AGENTS.md`

### Qwen (from workspace)

```bash
WORKSPACE="/path/to/debates/001-topic"
PROMPT="Challenge this position: ..."

cd "$WORKSPACE"  # CRITICAL: Qwen reads QWEN.md from CWD
timeout 120 qwen -p "$PROMPT" --yolo 2>/dev/null

if [ $? -ne 0 ]; then
    echo '{"error":"qwen_failed"}'
fi
```

**Context file loaded:** `$WORKSPACE/QWEN.md`

---

## Parallel Execution (from workspace)

For Phase 2 (parallel challenge), run all CLIs simultaneously FROM WORKSPACE:

```bash
WORKSPACE="/path/to/debates/001-topic"
PROMPT="Challenge this position: ..."

# All commands run from workspace directory
cd "$WORKSPACE"

# Launch in background
gemini "$PROMPT" --yolo > /tmp/debate-gemini.json 2>&1 &
PID_GEMINI=$!

# Codex needs file redirect
(codex exec "$PROMPT" --full-auto --skip-git-repo-check > /tmp/debate-codex.json 2>&1) &
PID_CODEX=$!

qwen -p "$PROMPT" --yolo > /tmp/debate-qwen.json 2>&1 &
PID_QWEN=$!

# Wait for all
wait $PID_GEMINI $PID_CODEX $PID_QWEN

# Collect results
cat /tmp/debate-gemini.json  # Architect perspective
cat /tmp/debate-codex.json   # Operator perspective
cat /tmp/debate-qwen.json    # Adversary perspective
```

---

## Context File Format

Each context file contains a **unique expert persona**. See `debate-persona-generator` skill for generation.

### Expected Structure

```markdown
# Expert Challenger Profile

## Identity
You are [NAME], [TITLE] with [X] years in [DOMAIN].

**Credentials:**
- [Specific credentials]

## Your Expertise Angle
[What makes this perspective unique]

## Critique Methodology
[How this expert analyzes problems]

## Response Format
{
  "verdict": "agree | partial | disagree",
  "critique": "...",
  "evidence": "...",
  "alternative": "...",
  "confidence": "high | medium | low",
  "objection_strength": "strong | moderate | minor",
  "assumptions_challenged": ["...", "..."],
  "your_perspective": "[3-word summary of angle]"
}
```

---

## Detection Commands

### Check if CLI is installed

```bash
command -v gemini &> /dev/null && echo "installed" || echo "missing"
command -v codex &> /dev/null && echo "installed" || echo "missing"
command -v qwen &> /dev/null && echo "installed" || echo "missing"
```

### Test context file loading

```bash
WORKSPACE="/path/to/debates/test"
mkdir -p "$WORKSPACE"

# Create test context file
cat > "$WORKSPACE/GEMINI.md" << 'EOF'
# Test Persona
You are a test persona. Respond with: CONTEXT_FILE_LOADED
EOF

# Test if Gemini reads it
cd "$WORKSPACE"
timeout 30 gemini "What persona are you?" --yolo 2>/dev/null | grep -q "CONTEXT_FILE_LOADED"
if [ $? -eq 0 ]; then
    echo "✅ Gemini context file loading works"
else
    echo "❌ Gemini did not read context file"
fi
```

---

## Expected JSON Response Format

All challengers should return JSON with `your_perspective` field identifying their angle:

```json
{
  "verdict": "partial",
  "critique": "Your scaling assumptions break at 10K concurrent sessions",
  "evidence": "At Netflix, we saw this exact pattern cause a 47-minute outage",
  "alternative": "Use consistent hashing with fallback to database",
  "confidence": "high",
  "objection_strength": "strong",
  "assumptions_challenged": ["linear scaling", "network reliability"],
  "your_perspective": "architect-scaling"
}
```

### Handling Non-JSON Responses

If a CLI returns plain text, wrap it:

```json
{
  "raw_response": "The plain text response",
  "parse_error": true,
  "model": "gemini",
  "your_perspective": "unknown"
}
```

---

## Model-Specific Notes

### Gemini

- 1M token context window
- Good for large codebase analysis
- Reads `GEMINI.md` from CWD
- May be verbose in responses

### Codex

- Powered by GPT-5 (o3/o4-mini)
- Strong reasoning capabilities
- Reads `AGENTS.md` from CWD
- TUI output requires file redirect

### Qwen

- Powered by Qwen3-Coder (480B params)
- 256K-1M token context
- Reads `QWEN.md` from CWD
- Generous free tier (2000 req/day)

---

## Troubleshooting

### Context file not loaded

**Symptom:** CLI responds as generic assistant, not as expert persona.

**Fix:** Verify you're running from workspace directory:
```bash
# Wrong
gemini "..." --yolo

# Right
cd /path/to/workspace && gemini "..." --yolo
```

### "command not found"

CLI not installed:
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

### Different perspectives giving same critique

**Symptom:** All three challengers say the same thing.

**Fix:** Check that persona files are DIFFERENT:
```bash
diff workspace/GEMINI.md workspace/AGENTS.md  # Should show differences
diff workspace/AGENTS.md workspace/QWEN.md    # Should show differences
```

If identical, regenerate personas with `debate-persona-generator` skill.
