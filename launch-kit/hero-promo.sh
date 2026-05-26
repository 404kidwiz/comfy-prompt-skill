#!/usr/bin/env bash
# hero-promo.sh — Generate the hero promo image for launching comfy-prompt.
#
# Self-promotional: the skill generates its own marketing asset.
# Total cost: ~$0.10. Takes ~10s.
#
# Output: ~/Comfy-Output/<YYYY-MM>/launch-kit/hero-launch.png

set -euo pipefail

if [[ -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2
    echo "  export COMFY_API_KEY=comfyui-..." >&2
    exit 1
fi

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"

# Hero composition: cinematic command-line operator on a dark workstation,
# multiple monitors showing comfy outputs, neon accent lighting.
# Visual register matches "Claude Code + Comfy" — high-end developer-tool vibes.
PROMPT="cinematic wide shot of a dimly lit modern workstation at night, multiple ultrawide monitors arranged in a curved arc displaying terminal sessions with green text and image generation grids, mechanical keyboard backlit cyan, condensed steam rising from a matte black coffee mug to camera-right, soft amber bias light glowing behind monitors, deep navy and charcoal color palette with single amber accent, slight anamorphic letterbox crop, 35mm film grain, crushed blacks, no people visible, hands of a developer typing partially in frame from extreme bottom edge, photoreal, cinematic depth of field, hero shot composition with negative space for text overlay, no text"

NEGATIVE_REGISTER="bright daylight, cartoon, illustration, low quality, watermark, signature, multiple people, busy background, cluttered desk, harsh fluorescent lighting"

OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag launch-kit | xargs dirname)"
mkdir -p "$OUT_DIR"
HERO="$OUT_DIR/hero-launch.png"

echo "━━━ Hero Promo Generation ━━━"
echo "  Model: flux-ultra (cinematic quality)"
echo "  Aspect: 16:9 (LinkedIn + X compatible)"
echo "  Output: $HERO"
echo ""

# Pre-spend lint
echo "▶ Lint check..."
python3 "$SKILL_DIR/scripts/lint.py" "$PROMPT" --model flux-ultra --type image --aspect 16:9 --quiet || true

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

echo "▶ Generating hero (flux-ultra, ~10s, ~\$0.10, 1920x1080)..."
comfy generate flux-ultra \
    --prompt "$PROMPT" \
    $(AF flux-ultra 16:9) \
    --download "$HERO"

# Embed metadata so downstream gallery/EXIF tooling shows context
echo "▶ Embedding metadata..."
python3 "$SKILL_DIR/scripts/embed.py" "$HERO" \
    --prompt "$PROMPT" \
    --model flux-ultra \
    --cost 0.10 \
    --aspect 16:9 2>/dev/null || true

# Generate gallery
python3 "$SKILL_DIR/scripts/gallery.py" "$OUT_DIR" 2>/dev/null || true

echo ""
echo "✅ Hero ready: $HERO"
echo ""
echo "  Use on LinkedIn / X post as the first attachment."
echo "  Gallery: $OUT_DIR/index.html"

# Auto-open if env set
if [[ "${COMFY_AUTO_OPEN:-0}" == "1" ]]; then
    open "$HERO" 2>/dev/null || xdg-open "$HERO" 2>/dev/null || true
fi
