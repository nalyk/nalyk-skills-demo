#!/bin/bash

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CLAUDE CODE PREMIUM STATUSLINE v2.0                                     ║
# ║  Powerline-inspired • Information-dense • Actually impressive            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

input=$(cat)

# ═══════════════════════════════════════════════════════════════════════════
# DATA EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════
model=$(echo "$input" | jq -r '.model.display_name // "Claude"')
cwd=$(echo "$input" | jq -r '.workspace.current_dir // empty')
style=$(echo "$input" | jq -r '.output_style.name // empty')
vim_mode=$(echo "$input" | jq -r '.vim.mode // empty')
agent=$(echo "$input" | jq -r '.agent.name // empty')
remaining=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')
total_in=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
total_out=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')

# ═══════════════════════════════════════════════════════════════════════════
# POWERLINE CHARACTERS
# ═══════════════════════════════════════════════════════════════════════════
PL_R=""      # Powerline right arrow (solid)
PL_RS=""     # Powerline right arrow (thin)
PL_L=""      # Powerline left arrow (solid)

# ═══════════════════════════════════════════════════════════════════════════
# DIRECTORY
# ═══════════════════════════════════════════════════════════════════════════
if [ -n "$cwd" ] && [ "$cwd" != "null" ]; then
    dir=$(basename "$cwd")
    # Smart path shortening for deep paths
    parent=$(dirname "$cwd" | sed "s|^$HOME|~|" | awk -F'/' '{if(NF>3) print "…/"$(NF-1)"/"$NF; else print $0}')
    if [ "$parent" != "." ] && [ "$parent" != "~" ]; then
        dir_display="${parent##*/}/${dir}"
    else
        dir_display="$dir"
    fi
else
    dir_display=$(basename "$(pwd)")
fi

# ═══════════════════════════════════════════════════════════════════════════
# GIT - Rich status with upstream tracking
# ═══════════════════════════════════════════════════════════════════════════
git_seg=""
work="${cwd:-$(pwd)}"
if [ -d "$work" ] && git -C "$work" rev-parse --git-dir >/dev/null 2>&1; then
    branch=$(git -C "$work" --no-optional-locks branch --show-current 2>/dev/null)

    if [ -z "$branch" ]; then
        sha=$(git -C "$work" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
        branch="➦ ${sha}"
    fi

    # Upstream status (ahead/behind)
    upstream=""
    ahead=$(git -C "$work" --no-optional-locks rev-list --count @{upstream}..HEAD 2>/dev/null || echo 0)
    behind=$(git -C "$work" --no-optional-locks rev-list --count HEAD..@{upstream} 2>/dev/null || echo 0)
    [ "$ahead" -gt 0 ] 2>/dev/null && upstream="⇡${ahead}"
    [ "$behind" -gt 0 ] 2>/dev/null && upstream="${upstream}⇣${behind}"

    # Working tree status
    status=$(git -C "$work" --no-optional-locks status --porcelain 2>/dev/null)

    staged=$(echo "$status" | grep -c "^[MADRC]" 2>/dev/null | tr -d '[:space:]') || staged=0
    modified=$(echo "$status" | grep -c "^.M" 2>/dev/null | tr -d '[:space:]') || modified=0
    untracked=$(echo "$status" | grep -c "^??" 2>/dev/null | tr -d '[:space:]') || untracked=0

    staged=${staged:-0}; modified=${modified:-0}; untracked=${untracked:-0}

    # Build status string with icons
    gstatus=""
    [ "$staged" -gt 0 ] && gstatus="${gstatus}●${staged} "
    [ "$modified" -gt 0 ] && gstatus="${gstatus}✎${modified} "
    [ "$untracked" -gt 0 ] && gstatus="${gstatus}◌${untracked} "

    if [ -z "$gstatus" ]; then
        gstatus="✔"
    else
        gstatus="${gstatus% }"
    fi

    git_seg=" ${branch} ${upstream}${upstream:+ }${gstatus} ${PL_RS}"
fi

# ═══════════════════════════════════════════════════════════════════════════
# CONTEXT WINDOW - Visual meter with smart formatting
# ═══════════════════════════════════════════════════════════════════════════
ctx_seg=""
if [ -n "$remaining" ] && [ "$remaining" != "null" ]; then
    pct=${remaining%.*}
    total_k=$(( (total_in + total_out) / 1000 ))

    # 10-segment visual meter
    filled=$((pct / 10))
    empty=$((10 - filled))

    meter=""
    for ((i=0; i<filled; i++)); do meter="${meter}▰"; done
    for ((i=0; i<empty; i++)); do meter="${meter}▱"; done

    # Status indicator
    if [ "$pct" -ge 60 ]; then
        indicator="◉"
    elif [ "$pct" -ge 30 ]; then
        indicator="◎"
    else
        indicator="○"
    fi

    ctx_seg=" ${indicator} ${meter} ${pct}% ${PL_RS} ⚡${total_k}k"
fi

# ═══════════════════════════════════════════════════════════════════════════
# OPTIONAL SEGMENTS
# ═══════════════════════════════════════════════════════════════════════════
style_seg=""
if [ -n "$style" ] && [ "$style" != "null" ] && [ "$style" != "default" ]; then
    style_seg=" ${PL_RS} ◈ ${style}"
fi

agent_seg=""
if [ -n "$agent" ] && [ "$agent" != "null" ]; then
    agent_seg=" ${PL_RS} ⚡${agent}"
fi

vim_seg=""
if [ -n "$vim_mode" ] && [ "$vim_mode" != "null" ]; then
    case "$vim_mode" in
        NORMAL)  vim_icon="◆" ;;
        INSERT)  vim_icon="●" ;;
        VISUAL)  vim_icon="◈" ;;
        *)       vim_icon="○" ;;
    esac
    vim_seg=" ${PL_RS} ${vim_icon} ${vim_mode}"
fi

# ═══════════════════════════════════════════════════════════════════════════
# TIME WITH SMART FORMAT
# ═══════════════════════════════════════════════════════════════════════════
now=$(date +"%H:%M")
hour=$(date +"%H")
if [ "$hour" -ge 6 ] && [ "$hour" -lt 12 ]; then
    time_icon="☀"
elif [ "$hour" -ge 12 ] && [ "$hour" -lt 18 ]; then
    time_icon="◐"
elif [ "$hour" -ge 18 ] && [ "$hour" -lt 21 ]; then
    time_icon="◑"
else
    time_icon="☽"
fi

# ═══════════════════════════════════════════════════════════════════════════
# MODEL BADGE
# ═══════════════════════════════════════════════════════════════════════════
# Shorten model name elegantly
case "$model" in
    *"Opus"*)     model_badge="◆ OPUS" ;;
    *"Sonnet"*)   model_badge="◇ SONNET" ;;
    *"Haiku"*)    model_badge="○ HAIKU" ;;
    *)            model_badge="◈ ${model}" ;;
esac

# ═══════════════════════════════════════════════════════════════════════════
# FINAL ASSEMBLY - Powerline style
# ═══════════════════════════════════════════════════════════════════════════
printf "╭─ %s %s 📂 %s%s%s%s%s%s %s %s %s\n" \
    "$model_badge" \
    "$PL_R" \
    "$dir_display" \
    "$git_seg" \
    "$ctx_seg" \
    "$style_seg" \
    "$agent_seg" \
    "$vim_seg" \
    "$PL_L" \
    "$time_icon" \
    "$now"
