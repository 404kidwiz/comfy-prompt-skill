#!/usr/bin/env bash
# character-sheet.sh — Generate a 4-angle character sheet with identity locked.
#
# Pipeline (est. ~$0.28 total):
#   1. Hero front 3/4               (flux-pro)     ~$0.04
#   2. Profile left                 (flux-kontext) ~$0.08
#   3. Profile right                (flux-kontext) ~$0.08
#   4. Three-quarter back           (flux-kontext) ~$0.08
#   [optional] ImageMagick grid     (free)
#
# Usage:
#   ./character-sheet.sh "weathered space pilot in his late 30s, short dark hair"
#   ./character-sheet.sh "character desc" --retry 2
#   ./character-sheet.sh "character desc" --skip-on-fail
#
# Requires: COMFY_API_KEY. Output: ~/Comfy-Output/<YYYY-MM>/character-sheet/

set -uo pipefail

# ── ARGS ──────────────────────────────────────────────────────────────────────
DESC=""
MAX_RETRIES=1
SKIP_ON_FAIL=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)      DRY_RUN=1; shift ;;
        --retry)        MAX_RETRIES="$2"; shift 2 ;;
        --skip-on-fail) SKIP_ON_FAIL=1; shift ;;
        -*)             echo "unknown flag: $1" >&2; exit 1 ;;
        *)              DESC="$1"; shift ;;
    esac
done

if [[ -z "$DESC" ]]; then
    echo "usage: $0 \"character description\" [--retry N] [--skip-on-fail]" >&2
    exit 1
fi

if [[ "$DRY_RUN" -ne 1 && -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2
    exit 1
fi

# ── PATHS ─────────────────────────────────────────────────────────────────────
SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag character-sheet | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

# Helper: translate (model, aspect) → correct CLI flags for that model
AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# Shared lighting + style register — applied to all four angles for consistency
LIGHTING="single hard side-key from camera-right with deep chiaroscuro shadow on opposite half of face, cool blue ambient fill from above, photoreal skin texture"
STYLE="anamorphic widescreen letterboxed, heavy 35mm film grain, crushed blacks, bleach-bypass color, muted saturation, photoreal cinematic"

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
echo "━━━ Character Sheet Pipeline ━━━"
echo "  Character: $DESC"
echo "  Output   : $OUT_DIR"
echo ""

HERO="$OUT_DIR/01_front.png"
run_step "1/4: Hero front 3/4 (flux-pro)" "~\$0.04" -- \
    comfy generate flux-pro \
        --prompt "MCU eye level front three-quarter angle of $DESC, looking just past camera, $LIGHTING, $STYLE" \
        $(AF flux-pro 3:4) \
        --download "$HERO" || { HERO=""; }

LEFT="$OUT_DIR/02_left.png"
if [[ -n "${HERO:-}" && -f "$HERO" ]]; then
    run_step "2/4: Profile left (flux-kontext)" "~\$0.08" -- \
        comfy generate flux-kontext \
            --image "$HERO" \
            --prompt "same character, same wardrobe, same hair, same age and features, now in pure profile facing camera-left, same $LIGHTING, same $STYLE, identity locked" \
            --download "$LEFT" || { LEFT=""; }
else
    echo "  ⏭  Step 2 skipped — hero not available"; LEFT=""
fi

RIGHT="$OUT_DIR/03_right.png"
if [[ -n "${HERO:-}" && -f "$HERO" ]]; then
    run_step "3/4: Profile right (flux-kontext)" "~\$0.08" -- \
        comfy generate flux-kontext \
            --image "$HERO" \
            --prompt "same character, same wardrobe, same hair, same age and features, now in pure profile facing camera-right, same $LIGHTING, same $STYLE, identity locked" \
            --download "$RIGHT" || { RIGHT=""; }
else
    echo "  ⏭  Step 3 skipped — hero not available"; RIGHT=""
fi

BACK="$OUT_DIR/04_back.png"
if [[ -n "${HERO:-}" && -f "$HERO" ]]; then
    run_step "4/4: Three-quarter back (flux-kontext)" "~\$0.08" -- \
        comfy generate flux-kontext \
            --image "$HERO" \
            --prompt "same character, same wardrobe, same hair, same age and features, now in three-quarter back view facing away from camera at slight angle so jaw is just visible, same $LIGHTING, same $STYLE, identity locked" \
            --download "$BACK" || { BACK=""; }
else
    echo "  ⏭  Step 4 skipped — hero not available"; BACK=""
fi

# Optional ImageMagick grid
if command -v magick >/dev/null 2>&1; then
    # Only composite images that actually exist
    IMAGES=()
    for img in "${HERO:-}" "${LEFT:-}" "${RIGHT:-}" "${BACK:-}"; do
        [[ -n "$img" && -f "$img" ]] && IMAGES+=("$img")
    done
    if [[ ${#IMAGES[@]} -ge 2 ]]; then
        GRID="$OUT_DIR/00_sheet.png"
        magick montage "${IMAGES[@]}" -tile 2x2 -geometry +10+10 -background black "$GRID" && \
            echo "   grid: $GRID"
    fi
fi

# ── SUMMARY ───────────────────────────────────────────────────────────────────
echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  Pipeline completed with ${#FAILED_STEPS[@]} failed step(s):"
    for s in "${FAILED_STEPS[@]}"; do echo "     ✗ $s"; done
    echo "   See: $FAIL_LOG"
else
    echo "✅ Character sheet complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
