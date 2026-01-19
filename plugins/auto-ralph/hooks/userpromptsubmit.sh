#!/bin/bash
# auto-ralph: UserPromptSubmit hook
# Injects scoring reminder for every user prompt to ensure deterministic skill activation
#
# This hook solves the "probabilistic skill detection" gap identified in the debate:
# - Skills rely on Claude recognizing when to invoke them (not guaranteed)
# - This hook ensures Claude ALWAYS evaluates tasks for auto-ralph scoring
#
# Output: JSON with systemMessage that Claude sees before processing the user's request

# Read stdin (contains user prompt data as JSON)
# We don't need to parse it - we just inject our reminder unconditionally
cat > /dev/null

# Output the system message injection
# This appears in Claude's context BEFORE it processes the user's message
cat << 'EOF'
{
  "systemMessage": "AUTO-RALPH CHECK: Score this task (0-4 points):\n+1 if clear success criteria (fix/implement/test/refactor keywords)\n+1 if benefits from iteration (not a question/explanation)\n+1 if scope well-defined (specific files/functions mentioned)\n+1 if completion verifiable (tests available or error to fix)\n\nIf score >= 3: Invoke the auto-ralph skill IMMEDIATELY.\nIf score < 3: Respond normally.\nForce triggers (always invoke): 'ralph this', 'auto ralph', 'loop it', 'iterate'\nForce skip (never invoke): 'just answer', 'explain', 'don't loop'"
}
EOF

# Always exit 0 - never block user prompts
exit 0
