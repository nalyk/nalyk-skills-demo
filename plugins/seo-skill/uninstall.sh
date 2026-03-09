#!/usr/bin/env bash
set -euo pipefail
echo "Uninstalling Claude SEO v2..."
rm -rf ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0
rm -rf ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0-*
rm -f ~/.claude/agents/seo-*.md
rm -f ~/.claude/seo-audit-history.db
echo "✓ Claude SEO v2 uninstalled"
