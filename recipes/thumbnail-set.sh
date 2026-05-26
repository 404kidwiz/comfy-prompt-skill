#!/usr/bin/env bash
# thumbnail-set.sh — YouTube thumbnail set generator (16:9 + 1:1 + 4:3 variants).
#
# Pipeline (est. ~$0.15 total):
#   1. Hero 16:9 thumbnail   (flux-pro)      ~$0.04
#   2. Square 1:1 variant    (flux-pro)      ~$0.04
#   3. Classic 4:3 variant   (flux-pro)      ~$0.04
#   4. Vertical 9:16 short   (flux-pro)      ~$0.04
#
# Usage:
#   ./thumbnail-set.sh "video about AI agents replacing devs" "shocked face, code on screen, bold red title overlay"
#   ./thumbnail-set.sh "topic" "scene" --retry 2 --skip-on-fail
#
# Requires: COMFY_API_KEY. Output: ~/Comfy-Output/<YYYY-MM>/thumbnails/

set -uo pipefail

TOPIC=""
SCENE=""
MAX_RETRIES=1
SKIP_ON_FAIL=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --retry)        MAX_RETRIES="$2"; shift 2 ;;
        --skip-on-fail) SKIP_ON_FAIL=1; shift ;;
        -*)             echo "unknown flag: $1" >&2; exit 1 ;;
        *)
            if [[ -z "$TOPIC" ]]; then  TOPIC="$1"
            elif [[ -z "$SCENE" ]]; then SCENE="$1"
            fi
            shift ;;
    esac
done

if [[ -z "$TOPIC" || -z "$SCENE" ]]; then
    echo "usage: $0 \"video topic\" \"scene description\" [--retry N] [--skip-on-fail]" >&2
    exit 1
fi

if [[ -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2; exit 1
fi

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag thumbnails | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# Shared thumbnail design language
STYLE="high-contrast colors, bold composition, eye-catching, sharp focal point, professional thumbnail design, vibrant saturation, clear focal subject filling 60% of frame, dramatic lighting"

FAILED_STEPS=()
run_step() {
    local label="$1" cost="$2"; shift 2; [[ "${1:-}" == "--" ]] && shift
    local attempt=0 rc=0
    echo "▶ $label  (est. $cost)"
    while [[ $attempt -le $MAX_RETRIES ]]; do
        [[ $attempt -gt 0 ]] && echo "  ↻ retry $attempt/$MAX_RETRIES"
        if "$@"; then rc=0; break; else rc=$?; attempt=$((attempt+1)); fi
    done
    if [[ $rc -ne 0 ]]; then
        echo "  ✗ $label FAILED" | tee -a "$FAIL_LOG"
        FAILED_STEPS+=("$label")
        [[ $SKIP_ON_FAIL -eq 0 ]] && { echo "Aborting. Use --skip-on-fail to continue."; exit $rc; }
        return 1
    fi
    echo "  ✓ done"
}

echo "━━━ Thumbnail Set Pipeline ━━━"
echo "  Topic: $TOPIC"
echo "  Scene: $SCENE"
echo "  Output: $OUT_DIR"
echo ""

PROMPT="thumbnail for video about $TOPIC, $SCENE, $STYLE"

run_step "1/4: YouTube 16:9 thumbnail (1920×1080)" "~\$0.04" -- \
    comfy generate flux-pro --prompt "$PROMPT, 16:9 widescreen composition" \
        $(AF flux-pro 16:9) --download "$OUT_DIR/01_youtube_16x9.png"

run_step "2/4: Square 1:1 variant (Instagram/podcast)" "~\$0.04" -- \
    comfy generate flux-pro --prompt "$PROMPT, square composition, focal subject centered" \
        $(AF flux-pro 1:1) --download "$OUT_DIR/02_square_1x1.png"

run_step "3/4: Classic 4:3 (TV/podcast)" "~\$0.04" -- \
    comfy generate flux-pro --prompt "$PROMPT, classic 4:3 composition" \
        $(AF flux-pro 4:3) --download "$OUT_DIR/03_classic_4x3.png"

run_step "4/4: Vertical 9:16 (Shorts/TikTok cover)" "~\$0.04" -- \
    comfy generate flux-pro --prompt "$PROMPT, vertical composition, hero subject tall" \
        $(AF flux-pro 9:16) --download "$OUT_DIR/04_short_9x16.png"

# Generate gallery
python3 "$SKILL_DIR/scripts/gallery.py" "$OUT_DIR" 2>/dev/null && \
    echo "   gallery: $OUT_DIR/index.html" || true

echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  ${#FAILED_STEPS[@]} step(s) failed:"
    for s in "${FAILED_STEPS[@]}"; do echo "     ✗ $s"; done
else
    echo "✅ Thumbnail set complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
