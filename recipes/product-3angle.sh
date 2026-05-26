#!/usr/bin/env bash
# product-3angle.sh — Product hero + 3 angles (front, side, back).
#
# Pipeline (est. ~$0.34):
#   1. Hero front 3/4         (flux-ultra)    ~$0.10
#   2. Side profile           (flux-kontext)  ~$0.08
#   3. Back three-quarter     (flux-kontext)  ~$0.08
#   4. Top-down detail        (flux-kontext)  ~$0.08
#
# Identity locked via flux-kontext using the hero as reference image.
#
# Usage:
#   ./product-3angle.sh "matte black coffee mug"
#   ./product-3angle.sh "product" --retry 2

set -uo pipefail

PRODUCT=""
MAX_RETRIES=1
SKIP_ON_FAIL=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --retry)        MAX_RETRIES="$2"; shift 2 ;;
        --skip-on-fail) SKIP_ON_FAIL=1; shift ;;
        -*)             echo "unknown flag: $1" >&2; exit 1 ;;
        *)              PRODUCT="$1"; shift ;;
    esac
done

if [[ -z "$PRODUCT" ]]; then
    echo "usage: $0 \"product description\" [--retry N] [--skip-on-fail]" >&2
    exit 1
fi
if [[ -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2; exit 1
fi

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag product-3angle | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

LIGHTING="soft overhead key with even fill, gentle rim from camera-back-left, catalog photography register"
STYLE="seamless white background, ultra-sharp, color-accurate, no environmental clutter, photoreal commercial photography"

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
        [[ $SKIP_ON_FAIL -eq 0 ]] && exit $rc
        return 1
    fi
    echo "  ✓ done"
}

echo "━━━ Product 3-Angle Pipeline ━━━"
echo "  Product: $PRODUCT"
echo "  Output: $OUT_DIR"
echo ""

HERO="$OUT_DIR/01_hero.png"
run_step "1/4: Hero front 3/4 (flux-ultra)" "~\$0.10" -- \
    comfy generate flux-ultra \
        --prompt "MCU three-quarter front view of $PRODUCT, $LIGHTING, $STYLE" \
        $(AF flux-ultra 1:1) \
        --download "$HERO" || { HERO=""; }

if [[ -n "${HERO:-}" && -f "$HERO" ]]; then
    run_step "2/4: Side profile (flux-kontext)" "~\$0.08" -- \
        comfy generate flux-kontext \
            --image "$HERO" \
            --prompt "same product as reference image, identity locked, same materials and finish, now in pure side profile view from camera-right, same $LIGHTING, same $STYLE" \
            --download "$OUT_DIR/02_side.png" || true

    run_step "3/4: Back three-quarter (flux-kontext)" "~\$0.08" -- \
        comfy generate flux-kontext \
            --image "$HERO" \
            --prompt "same product as reference image, identity locked, now in three-quarter back view, same $LIGHTING, same $STYLE" \
            --download "$OUT_DIR/03_back.png" || true

    run_step "4/4: Top-down detail (flux-kontext)" "~\$0.08" -- \
        comfy generate flux-kontext \
            --image "$HERO" \
            --prompt "same product as reference image, identity locked, now top-down overhead view showing surface detail, same $LIGHTING, same $STYLE" \
            --download "$OUT_DIR/04_top.png" || true
fi

# Grid composite if magick available
if command -v magick >/dev/null 2>&1; then
    IMAGES=()
    for img in "$OUT_DIR/01_hero.png" "$OUT_DIR/02_side.png" "$OUT_DIR/03_back.png" "$OUT_DIR/04_top.png"; do
        [[ -f "$img" ]] && IMAGES+=("$img")
    done
    if [[ ${#IMAGES[@]} -ge 2 ]]; then
        magick montage "${IMAGES[@]}" -tile 2x2 -geometry +10+10 -background white "$OUT_DIR/00_sheet.png" && \
            echo "   grid: $OUT_DIR/00_sheet.png"
    fi
fi

python3 "$SKILL_DIR/scripts/gallery.py" "$OUT_DIR" 2>/dev/null || true

echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  ${#FAILED_STEPS[@]} step(s) failed"
else
    echo "✅ Product 3-angle complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
