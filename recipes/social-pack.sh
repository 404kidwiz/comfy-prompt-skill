#!/usr/bin/env bash
# social-pack.sh — Same logo / hero on 4 social backgrounds.
#
# Pipeline (est. ~$0.30 total):
#   1. Background removal              (recraft-rmbg)      ~$0.02
#   2. Background swap × 4 (different scenes)  (recraft-replace-bg) ~$0.07 × 4 = $0.28
#   [optional] gallery
#
# Usage:
#   ./social-pack.sh <hero_image.png> "brand name or product"
#   ./social-pack.sh ./logo.png "Nova Coffee" --platform reel
#
# Output: ~/Comfy-Output/<YYYY-MM>/social-pack/

set -uo pipefail

HERO=""
BRAND=""
PLATFORM="square"
MAX_RETRIES=1
SKIP_ON_FAIL=0
DRY_RUN=0
QUALITY="s"
BUDGET=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --platform)     PLATFORM="$2"; shift 2 ;;
        --dry-run)      DRY_RUN=1; shift ;;
        --retry)        MAX_RETRIES="$2"; shift 2 ;;
        --skip-on-fail) SKIP_ON_FAIL=1; shift ;;
        --quality|-q)   QUALITY="$2"; shift 2 ;;
        --budget)       BUDGET=1; shift ;;
        -*)             echo "unknown flag: $1" >&2; exit 1 ;;
        *)
            if [[ -z "$HERO" ]]; then HERO="$1"
            elif [[ -z "$BRAND" ]]; then BRAND="$1"
            fi
            shift ;;
    esac
done

if [[ -z "$HERO" || -z "$BRAND" ]]; then
    echo "usage: $0 <hero_image> \"brand/product name\" [--quality s|a|b|c] [--budget] [--platform square|reel|wide]" >&2
    exit 1
fi

if [[ ! -f "$HERO" ]]; then
    echo "error: hero image not found: $HERO" >&2; exit 1
fi
if [[ "$DRY_RUN" -ne 1 && -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2; exit 1
fi

case "$PLATFORM" in
    square|1:1|instagram)        ASPECT="1:1" ;;
    portrait|4:5|feed)           ASPECT="4:5" ;;
    tiktok|reel|vertical|9:16)  ASPECT="9:16" ;;
    wide|16:9|landscape)         ASPECT="16:9" ;;
    *)                           ASPECT="1:1" ;;
esac

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag social-pack | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

# Tier resolver
TIER() {
    local task="$1" q="${2:-$QUALITY}"
    local b=""; [[ "$BUDGET" == "1" ]] && b="--budget"
    python3 "$SKILL_DIR/scripts/tiers.py" "$task" --quality "$q" $b 2>/dev/null
}

BG_REMOVE_MODEL="$(TIER bg-remove)"
BG_REPLACE_MODEL="$(TIER bg-replace)"

# 4 social background scenes
declare -a SCENES=(
    "sunlit minimal studio backdrop, soft pastel gradient, golden-hour lighting"
    "urban concrete texture, warm street light, slight rain reflection, moody"
    "natural lifestyle setting, hands holding the $BRAND, café tabletop, warm coffee shop bokeh"
    "abstract bold color gradient, premium-feel, soft contemporary lighting, magazine cover register"
)
declare -a TAGS=("studio" "urban" "lifestyle" "abstract")

FAILED_STEPS=()
run_step() {
    local label="$1" cost="$2"; shift 2; [[ "${1:-}" == "--" ]] && shift
    local attempt=0 rc=0
    echo "▶ $label  (est. $cost)"
    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "  [DRY-RUN] would execute: $*"
        return 0
    fi
    while [[ $attempt -le $MAX_RETRIES ]]; do
        [[ $attempt -gt 0 ]] && echo "  ↻ retry $attempt/$MAX_RETRIES"
        if "$@"; then rc=0; break; else rc=$?; attempt=$((attempt+1)); fi
    done
    if [[ $rc -ne 0 ]]; then
        echo "  ✗ $label FAILED" | tee -a "$FAIL_LOG"
        FAILED_STEPS+=("$label")
        [[ $SKIP_ON_FAIL -eq 0 ]] && { exit $rc; }
        return 1
    fi
    echo "  ✓ done"
}

echo "━━━ Social Pack Pipeline ━━━"
echo "  Hero: $HERO"
echo "  Brand: $BRAND"
echo "  Aspect: $ASPECT ($PLATFORM)"
echo "  Output: $OUT_DIR"
echo ""

CUTOUT="$OUT_DIR/00_cutout.png"
run_step "Background remove ($BG_REMOVE_MODEL)" "~\$0.02" -- \
    comfy generate "$BG_REMOVE_MODEL" --image "$HERO" --download "$CUTOUT" || { CUTOUT=""; }

if [[ -n "${CUTOUT:-}" && -f "$CUTOUT" ]]; then
    for i in "${!SCENES[@]}"; do
        n=$((i+1))
        tag="${TAGS[$i]}"
        scene="${SCENES[$i]}"
        run_step "Scene $n/4: $tag ($BG_REPLACE_MODEL)" "~\$0.07" -- \
            comfy generate "$BG_REPLACE_MODEL" \
                --image "$CUTOUT" \
                --prompt "$scene, $BRAND remains hero focus, sharp foreground, soft background blur, professional social media composition" \
                --download "$OUT_DIR/0${n}_${tag}.png" || true
    done
else
    echo "  ⏭  All scenes skipped — cutout failed"
fi

# Gallery
python3 "$SKILL_DIR/scripts/gallery.py" "$OUT_DIR" 2>/dev/null && \
    echo "   gallery: $OUT_DIR/index.html" || true

echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  ${#FAILED_STEPS[@]} step(s) failed"
else
    echo "✅ Social pack complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
