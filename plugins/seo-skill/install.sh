#!/usr/bin/env bash
set -euo pipefail

main() {
    SKILL_DIR="${HOME}/.claude/skills/seo"
    AGENT_DIR="${HOME}/.claude/agents"
    REPO_URL="https://github.com/claude-seo-v2/claude-seo"

    echo "════════════════════════════════════════"
    echo "║   Claude SEO v2 — Installer          ║"
    echo "║   Deterministic SEO Engine            ║"
    echo "════════════════════════════════════════"
    echo ""

    command -v python3 >/dev/null 2>&1 || { echo "✗ Python 3 required"; exit 1; }
    command -v git >/dev/null 2>&1 || { echo "✗ Git required"; exit 1; }

    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo "✓ Python ${PYTHON_VERSION} detected"

    mkdir -p "${SKILL_DIR}" "${AGENT_DIR}"

    TEMP_DIR=$(mktemp -d)
    trap "rm -rf ${TEMP_DIR}" EXIT

    echo "↓ Downloading Claude SEO v2..."
    git clone --depth 1 "${REPO_URL}" "${TEMP_DIR}/claude-seo" 2>/dev/null

    # Main skill + references
    echo "→ Installing skill files..."
    cp -r "${TEMP_DIR}/claude-seo/seo/"* "${SKILL_DIR}/"

    # Sub-skills
    for skill_dir in "${TEMP_DIR}/claude-seo/skills"/*/; do
        skill_name=$(basename "${skill_dir}")
        target="${HOME}/.claude/skills/${skill_name}"
        mkdir -p "${target}"
        cp -r "${skill_dir}"* "${target}/"
    done

    # Engine
    echo "→ Installing engine..."
    mkdir -p "${SKILL_DIR}/engine"
    cp -r "${TEMP_DIR}/claude-seo/engine/"* "${SKILL_DIR}/engine/"

    # Integrations
    mkdir -p "${SKILL_DIR}/integrations"
    cp -r "${TEMP_DIR}/claude-seo/integrations/"* "${SKILL_DIR}/integrations/"

    # Schema templates
    mkdir -p "${SKILL_DIR}/schema"
    cp -r "${TEMP_DIR}/claude-seo/schema/"* "${SKILL_DIR}/schema/"

    # Agents
    echo "→ Installing subagents..."
    cp "${TEMP_DIR}/claude-seo/agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true

    # Hooks
    mkdir -p "${SKILL_DIR}/hooks"
    cp -r "${TEMP_DIR}/claude-seo/hooks/"* "${SKILL_DIR}/hooks/" 2>/dev/null || true
    chmod +x "${SKILL_DIR}/hooks/"*.sh 2>/dev/null || true

    # CI templates
    mkdir -p "${SKILL_DIR}/ci"
    cp -r "${TEMP_DIR}/claude-seo/ci/"* "${SKILL_DIR}/ci/" 2>/dev/null || true

    # Requirements file (needed for fallback install instructions)
    cp "${TEMP_DIR}/claude-seo/requirements.txt" "${SKILL_DIR}/requirements.txt"

    # Python dependencies
    echo "→ Installing Python dependencies..."
    VENV_DIR="${SKILL_DIR}/.venv"
    if python3 -m venv "${VENV_DIR}" 2>/dev/null; then
        "${VENV_DIR}/bin/pip" install --quiet -r "${TEMP_DIR}/claude-seo/requirements.txt" 2>/dev/null && \
            echo "  ✓ Installed in venv" || \
            echo "  ⚠  Venv pip failed. Run: ${VENV_DIR}/bin/pip install -r ${SKILL_DIR}/requirements.txt"
    else
        pip install --quiet --user -r "${TEMP_DIR}/claude-seo/requirements.txt" 2>/dev/null || \
        echo "  ⚠  Auto-install failed. Run: pip install --user -r ${SKILL_DIR}/requirements.txt"
    fi

    echo ""
    echo "✓ Claude SEO v2 installed!"
    echo ""
    echo "Usage:"
    echo "  claude"
    echo "  /seo audit https://example.com"
    echo "  /seo audit https://example.com --compare"
    echo "  /seo fix https://example.com"
    echo "  /seo linkgraph https://example.com"
    echo "  /seo history https://example.com"
    echo ""
    echo "Engine CLI:"
    echo "  python -m engine.cli audit https://example.com --output report.md"
}

main "$@"
