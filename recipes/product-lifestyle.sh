#!/usr/bin/env bash
# product-lifestyle.sh — Generate same product in 4 lifestyle contexts.
#
# Pipeline (est. ~$0.38 total):
#   Hero on white seamless    (flux-ultra)        ~$0.10
#   Background remove         (recraft-rmbg)      ~$0.02
#   4× lifestyle composites   (recraft-replace-bg) ~$0.07 each → $0.28
#   [optional] 2×2 grid       (ImageMagick)       free
#
# Usage:
#   ./product-lifestyle.sh "matte black coffee mug"
#   ./product-lifestyle.sh "product" --platform square
#   ./product-lifestyle.sh "product" --retry 2 --skip-on-fail
#
# Output: ~/Comfy-Output/<YYYY-MM>/product-lifestyle/

set -uo pipefail

# ── ARGS ──────────────────────────────────────────────────────────────────────
PRODUCT=""
PLATFORM="square"   # default for product: square
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
        *)              PRODUCT="$1"; shift ;;
    esac
done

if [[ -z "$PRODUCT" ]]; then
    echo "usage: $0 \"product description\" [--quality s|a|b|c] [--budget] [--platform square|reel|wide]" >&2
    exit 1
fi

if [[ "$DRY_RUN" -ne 1 && -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2; exit 1
fi

# ── PLATFORM → ASPECT ─────────────────────────────────────────────────────────
case "$PLATFORM" in
    square|1:1|instagram)         ASPECT="1:1" ;;
    portrait|4:5|feed)            ASPECT="4:5" ;;
    tiktok|reel|vertical|9:16)   ASPECT="9:16" ;;
    wide|16:9|landscape|youtube)  ASPECT="16:9" ;;
    *)                            ASPECT="1:1" ;;
esac

# ── PATHS ─────────────────────────────────────────────────────────────────────
SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag product-lifestyle | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# Tier resolver — premium first
TIER() {
    local task="$1" q="${2:-$QUALITY}"
    local b=""; [[ "$BUDGET" == "1" ]] && b="--budget"
    python3 "$SKILL_DIR/scripts/tiers.py" "$task" --quality "$q" $b 2>/dev/null
}

HERO_MODEL="$(TIER image)"
HERO_SUB="$(python3 "$SKILL_DIR/scripts/tiers.py" image --quality "$QUALITY" $([[ "$BUDGET" == "1" ]] && echo --budget) --sub-flags 2>/dev/null)"
BG_REMOVE_MODEL="$(TIER bg-remove)"
BG_REPLACE_MODEL="$(TIER bg-replace)"

# Lifestyle scenes
declare -a SCENES=(
    "sunlit Scandinavian kitchen, light wood counter, white tile backsplash, plants in window, morning light"
    "cozy dim study at night, mahogany desk, brass lamp glow, leather-bound books, reading register"
    "modern minimalist office, white desk, single houseplant, large window with city view, midday natural light"
    "outdoor patio at golden hour, weathered wood table, terracotta pots, blurred garden background, warm sunset glow"
)
declare -a TAGS=("scandi-morning" "study-night" "office-midday" "patio-sunset")

# ── HELPERS ───────────────────────────────────────────────────────────────────
FAILED_STEPS=()

run_step() {
    local label="$1"
    local cost="$2"
    shift 2
    [[ "${1:-}" == "--" ]] && shift

    local attempt=0
    local rc=0

    echo "▶ $label  (est. $cost)"
    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "  [DRY-RUN] would execute: $*"
        return 0
    fi
    while [[ $attempt -le $MAX_RETRIES ]]; do
        [[ $attempt -gt 0 ]] && echo "  ↻ retry $attempt/$MAX_RETRIES ..."
        if "$@"; then rc=0; break
        else rc=$?; attempt=$((attempt + 1))
        fi
    done

    if [[ $rc -ne 0 ]]; then
        echo "  ✗ $label FAILED (exit $rc)" | tee -a "$FAIL_LOG"
        FAILED_STEPS+=("$label")
        if [[ $SKIP_ON_FAIL -eq 0 ]]; then
            echo "  Aborting. Re-run with --skip-on-fail to continue past failures." >&2
            exit $rc
        fi
        return 1
    fi
    echo "  ✓ $label done"
    return 0
}

# ── PIPELINE ──────────────────────────────────────────────────────────────────
echo "━━━ Product Lifestyle Pipeline ━━━"
echo "  Product : $PRODUCT"
echo "  Platform: $PLATFORM ($ASPECT)"
echo "  Output  : $OUT_DIR"
echo ""

HERO="$OUT_DIR/00_hero.png"
# shellcheck disable=SC2086
run_step "Hero on white seamless ($HERO_MODEL)" "~\$0.15 (premium)" -- \
    comfy generate $HERO_MODEL $HERO_SUB \
        --prompt "$PRODUCT on seamless white background, MCU static locked-off camera, soft overhead key with even fill, catalog photography, ultra-sharp, color-accurate, deep blacks, no clutter, photoreal" \
        $(AF $HERO_MODEL 1:1) \
        --download "$HERO" || { HERO=""; }

CUTOUT="$OUT_DIR/00_cutout.png"
if [[ -n "${HERO:-}" && -f "$HERO" ]]; then
    run_step "Background remove ($BG_REMOVE_MODEL)" "~\$0.02" -- \
        comfy generate "$BG_REMOVE_MODEL" --image "$HERO" --download "$CUTOUT" || { CUTOUT=""; }
else
    echo "  ⏭  Cutout skipped — hero not available"; CUTOUT=""
fi

INPUT="${CUTOUT:-${HERO:-}}"
SCENE_OUTPUTS=()

for i in "${!SCENES[@]}"; do
    n=$((i + 1))
    tag="${TAGS[$i]}"
    scene="${SCENES[$i]}"
    out="$OUT_DIR/0${n}_${tag}.png"

    if [[ -n "${INPUT:-}" && -f "$INPUT" ]]; then
        run_step "Scene $n/4: $tag ($BG_REPLACE_MODEL)" "~\$0.07" -- \
            comfy generate "$BG_REPLACE_MODEL" \
                --image "$INPUT" \
                --prompt "$scene, keep product lighting consistent with new environment, product remains hero focus, sharp product, soft environmental blur" \
                --download "$out" && SCENE_OUTPUTS+=("$out") || true
    else
        echo "  ⏭  Scene $n skipped — no cutout/hero available"
    fi
done

# Optional 2×2 grid
if command -v magick >/dev/null 2>&1 && [[ ${#SCENE_OUTPUTS[@]} -ge 2 ]]; then
    GRID="$OUT_DIR/00_grid.png"
    magick montage "${SCENE_OUTPUTS[@]}" -tile 2x2 -geometry +5+5 -background black "$GRID" 2>/dev/null && \
        echo "   grid: $GRID" || true
fi

# ── SUMMARY ───────────────────────────────────────────────────────────────────
echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  Pipeline completed with ${#FAILED_STEPS[@]} failed step(s):"
    for s in "${FAILED_STEPS[@]}"; do echo "     ✗ $s"; done
    echo "   See: $FAIL_LOG"
else
    echo "✅ Product lifestyle complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
