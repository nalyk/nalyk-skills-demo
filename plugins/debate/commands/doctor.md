---
description: Check debate system health - verifies external CLI availability and authentication
allowed-tools: Bash
---

# Debate System Health Check

Verify that external CLI models are installed and authenticated.

---

## Step 1: Detect Installed CLIs

Run detection for each supported CLI:

```bash
echo "=== DEBATE SYSTEM DIAGNOSTIC ==="
echo ""
echo "Checking installed CLIs..."
echo ""

# Create temp file for results
RESULTS_FILE="/tmp/debate-doctor-results"
rm -f "$RESULTS_FILE"
touch "$RESULTS_FILE"

# Check Gemini
echo -n "gemini:  "
if command -v gemini &> /dev/null; then
    VERSION=$(gemini --version 2>/dev/null | head -1 || echo "version unknown")
    echo "INSTALLED ($VERSION)"
    echo "gemini:installed" >> "$RESULTS_FILE"
else
    echo "NOT FOUND"
    echo "gemini:missing" >> "$RESULTS_FILE"
fi

# Check Codex
echo -n "codex:   "
if command -v codex &> /dev/null; then
    VERSION=$(codex --version 2>/dev/null | head -1 || echo "version unknown")
    echo "INSTALLED ($VERSION)"
    echo "codex:installed" >> "$RESULTS_FILE"
else
    echo "NOT FOUND"
    echo "codex:missing" >> "$RESULTS_FILE"
fi

# Check Qwen
echo -n "qwen:    "
if command -v qwen &> /dev/null; then
    VERSION=$(qwen --version 2>/dev/null | head -1 || echo "version unknown")
    echo "INSTALLED ($VERSION)"
    echo "qwen:installed" >> "$RESULTS_FILE"
else
    echo "NOT FOUND"
    echo "qwen:missing" >> "$RESULTS_FILE"
fi

echo ""

# Count installed
INSTALLED_COUNT=$(grep -c ":installed" "$RESULTS_FILE" 2>/dev/null || echo "0")
echo "External CLIs found: $INSTALLED_COUNT"
```

---

## Step 2: Test Authentication (for installed CLIs)

For each installed CLI, run a quick authentication probe:

```bash
echo ""
echo "Testing authentication..."
echo ""

AUTH_RESULTS="/tmp/debate-doctor-auth"
rm -f "$AUTH_RESULTS"
touch "$AUTH_RESULTS"

# Test Gemini auth
if grep -q "gemini:installed" "$RESULTS_FILE" 2>/dev/null; then
    echo -n "gemini auth: "
    if timeout 30 gemini "respond with exactly: DEBATE_AUTH_OK" --yolo 2>/dev/null | grep -q "DEBATE_AUTH_OK"; then
        echo "VERIFIED"
        echo "gemini:auth_ok" >> "$AUTH_RESULTS"
    else
        echo "FAILED (check: gemini auth login)"
        echo "gemini:auth_fail" >> "$AUTH_RESULTS"
    fi
fi

# Test Codex auth (uses file redirect due to TUI output not piping correctly)
if grep -q "codex:installed" "$RESULTS_FILE" 2>/dev/null; then
    echo -n "codex auth:  "
    CODEX_OUT="/tmp/debate-codex-auth-$$.txt"
    cd /tmp && timeout 60 codex exec "respond with exactly: DEBATE_AUTH_OK" --full-auto --skip-git-repo-check > "$CODEX_OUT" 2>&1
    if grep -q "DEBATE_AUTH_OK" "$CODEX_OUT" 2>/dev/null; then
        echo "VERIFIED"
        echo "codex:auth_ok" >> "$AUTH_RESULTS"
    else
        echo "FAILED (check: codex auth)"
        echo "codex:auth_fail" >> "$AUTH_RESULTS"
    fi
    rm -f "$CODEX_OUT"
fi

# Test Qwen auth
if grep -q "qwen:installed" "$RESULTS_FILE" 2>/dev/null; then
    echo -n "qwen auth:   "
    if timeout 30 qwen -p "respond with exactly: DEBATE_AUTH_OK" --yolo 2>/dev/null | grep -q "DEBATE_AUTH_OK"; then
        echo "VERIFIED"
        echo "qwen:auth_ok" >> "$AUTH_RESULTS"
    else
        echo "FAILED (check: qwen auth login)"
        echo "qwen:auth_fail" >> "$AUTH_RESULTS"
    fi
fi

# Count authenticated
AUTH_COUNT=$(grep -c ":auth_ok" "$AUTH_RESULTS" 2>/dev/null || echo "0")
echo ""
echo "Authenticated CLIs: $AUTH_COUNT"
```

---

## Step 3: Report System Status

Based on the results, display the appropriate status:

### If 0 external CLIs authenticated:

```
+================================================================+
|  DEBATE SYSTEM: DISABLED                                        |
+================================================================+
|                                                                  |
|  Claude debating itself is theater, not debate.                  |
|  Genuine model diversity requires external CLIs.                 |
|                                                                  |
|  Install and authenticate at least ONE:                          |
|                                                                  |
|  npm i -g @google/gemini-cli      # Free: 1000 req/day           |
|    Then: gemini auth login                                       |
|                                                                  |
|  npm i -g @openai/codex           # Requires ChatGPT Plus        |
|    Then: codex auth                                              |
|                                                                  |
|  npm i -g @qwen-code/qwen-code    # Free: 2000 req/day           |
|    Then: qwen auth login                                         |
|                                                                  |
|  After installing, run: /debate:doctor                           |
|                                                                  |
+================================================================+
```

**STOP.** Do not allow debate commands until at least 1 external CLI is available.

### If 1 external CLI authenticated:

```
+================================================================+
|  DEBATE SYSTEM: MINIMAL                                          |
+================================================================+
|                                                                  |
|  Challengers available: [list]                                   |
|  Debate capability: FUNCTIONAL                                   |
|                                                                  |
|  You can run debates, but perspective diversity is limited.      |
|  Consider installing additional CLIs for stronger coverage.      |
|                                                                  |
+================================================================+
```

### If 2 external CLIs authenticated:

```
+================================================================+
|  DEBATE SYSTEM: FUNCTIONAL                                       |
+================================================================+
|                                                                  |
|  Challengers available: [list]                                   |
|  Debate capability: GOOD                                         |
|                                                                  |
|  Good perspective diversity. Blind spots will be caught.         |
|                                                                  |
+================================================================+
```

### If 3+ external CLIs authenticated:

```
+================================================================+
|  DEBATE SYSTEM: OPTIMAL                                          |
+================================================================+
|                                                                  |
|  Challengers available: [list]                                   |
|  Debate capability: MAXIMUM                                      |
|                                                                  |
|  Full adversarial coverage. Ready for production debates.        |
|                                                                  |
+================================================================+
```

---

## Step 4: Cache Results

Save the authenticated CLI list for use by debate commands:

```bash
# Save available challengers
grep ":auth_ok" "$AUTH_RESULTS" 2>/dev/null | cut -d: -f1 > /tmp/debate-available-challengers
echo ""
echo "Available challengers cached to /tmp/debate-available-challengers"
```

---

## Output Summary Table

Display a final summary:

```
+------------------------------------------------------------------+
|  CLI       | Installed | Authenticated | Free Tier               |
+------------+-----------+---------------+-------------------------+
|  gemini    | [Y/N]     | [Y/N/-]       | 1000 req/day            |
|  codex     | [Y/N]     | [Y/N/-]       | ChatGPT Plus required   |
|  qwen      | [Y/N]     | [Y/N/-]       | 2000 req/day            |
+------------------------------------------------------------------+
|  EXTERNAL CHALLENGERS: [N] available                              |
|  DEBATE CAPABILITY: [DISABLED/MINIMAL/FUNCTIONAL/OPTIMAL]         |
+------------------------------------------------------------------+
```
