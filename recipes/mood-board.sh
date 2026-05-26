#!/usr/bin/env bash
# mood-board.sh — Generate a 9-tile visual mood reference for a creative brief.
#
# Pipeline (est. ~$0.36):
#   9 nano-banana tiles (~$0.01 each)  ~$0.09
#   OR
#   9 flux-pro tiles (~$0.04 each)     ~$0.36 (higher quality, --hq flag)
#
# Each tile explores a different facet of the brief: color, texture, light,
# subject, environment, composition, mood, scale, motion.
#
# Usage:
#   ./mood-board.sh "cyberpunk neon detective in rain"
#   ./mood-board.sh "brief" --hq                # use flux-pro instead of nano-banana
#   ./mood-board.sh "brief" --retry 2

set -uo pipefail

BRIEF=""
MODEL="nano-banana"
COST="\$0.01"
MAX_RETRIES=1
SKIP_ON_FAIL=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --hq)           MODEL="flux-pro"; COST="\$0.04"; shift ;;
        --retry)        MAX_RETRIES="$2"; shift 2 ;;
        --skip-on-fail) SKIP_ON_FAIL=1; shift ;;
        -*)             echo "unknown flag: $1" >&2; exit 1 ;;
        *)              BRIEF="$1"; shift ;;
    esac
done

if [[ -z "$BRIEF" ]]; then
    echo "usage: $0 \"creative brief\" [--hq] [--retry N] [--skip-on-fail]" >&2
    exit 1
fi
if [[ -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2; exit 1
fi

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag mood-board | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# 9 mood-board axes
declare -a AXES=(
    "COLOR — color palette study, abstract gradient inspired by"
    "TEXTURE — macro texture detail study, materials and surfaces evoking"
    "LIGHT — pure lighting study, no subject, just light quality of"
    "SUBJECT — character/object study, hero focal point evoking"
    "ENVIRONMENT — wide environmental establishing shot of the world of"
    "COMPOSITION — graphic composition study, abstracted geometry of"
    "MOOD — emotional atmosphere capture, tonal essence of"
    "SCALE — sense of scale and proportion study evoking"
    "MOTION — implied motion / energy study of"
)
declare -a TAGS=("color" "texture" "light" "subject" "environment" "composition" "mood" "scale" "motion")

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

echo "━━━ Mood Board Pipeline (9 tiles) ━━━"
echo "  Brief: $BRIEF"
echo "  Model: $MODEL (est. $COST × 9 = ~\$$(python3 -c "print(${COST#\$} * 9)"))"
echo "  Output: $OUT_DIR"
echo ""

for i in "${!AXES[@]}"; do
    n=$((i+1))
    axis="${AXES[$i]}"
    tag="${TAGS[$i]}"
    run_step "Tile $n/9: $tag" "~$COST" -- \
        comfy generate "$MODEL" \
            --prompt "$axis $BRIEF, mood-board reference tile, no text overlay, cinematic register, intentional composition" \
            $(AF "$MODEL" 1:1) \
            --download "$OUT_DIR/0${n}_${tag}.png" || true
done

# 3×3 grid
if command -v magick >/dev/null 2>&1; then
    IMAGES=()
    for tag in "${TAGS[@]}"; do
        for i in $(seq 1 9); do
            img="$OUT_DIR/0${i}_${tag}.png"
            [[ -f "$img" ]] && IMAGES+=("$img") && break
        done
    done
    if [[ ${#IMAGES[@]} -ge 2 ]]; then
        magick montage "${IMAGES[@]}" -tile 3x3 -geometry +5+5 -background black "$OUT_DIR/00_board.png" && \
            echo "   grid: $OUT_DIR/00_board.png"
    fi
fi

python3 "$SKILL_DIR/scripts/gallery.py" "$OUT_DIR" 2>/dev/null || true

echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  ${#FAILED_STEPS[@]} step(s) failed"
else
    echo "✅ Mood board complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
