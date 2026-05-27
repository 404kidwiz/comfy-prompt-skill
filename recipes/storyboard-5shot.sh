#!/usr/bin/env bash
# storyboard-5shot.sh — Generate a 5-shot cinematic storyboard with consistent style.
#
# Pipeline (est. ~$0.20 total):
#   1. EWS establishing      (flux-pro)      ~$0.04
#   2. MCU character intro   (flux-pro)      ~$0.04
#   3. ECU detail insert     (nano-banana)   ~$0.01
#   4. MS action beat        (flux-pro)      ~$0.04
#   5. WS resolution         (flux-pro)      ~$0.04
#   [optional] grid          (ImageMagick)   free
#
# Same lighting + style register applied to all five for cut continuity.
#
# Usage:
#   ./storyboard-5shot.sh "subject + scenario brief" "location" "style register"
#   ./storyboard-5shot.sh "lone bounty hunter" "rain-soaked Tokyo neon alley" "anamorphic cyberpunk Blade Runner"
#   ./storyboard-5shot.sh "subject" "location" "style" --platform wide
#   ./storyboard-5shot.sh "subject" "location" "style" --retry 2 --skip-on-fail
#
# Requires: COMFY_API_KEY. Output: ~/Comfy-Output/<YYYY-MM>/storyboard/

set -uo pipefail

# ── ARGS ──────────────────────────────────────────────────────────────────────
SUBJECT=""
LOCATION=""
STYLE=""
PLATFORM="wide"
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
            if [[ -z "$SUBJECT" ]]; then   SUBJECT="$1"
            elif [[ -z "$LOCATION" ]]; then LOCATION="$1"
            elif [[ -z "$STYLE" ]]; then    STYLE="$1"
            fi
            shift ;;
    esac
done

if [[ -z "$SUBJECT" || -z "$LOCATION" || -z "$STYLE" ]]; then
    echo "usage: $0 \"subject brief\" \"location\" \"style register\" [--quality s|a|b|c] [--budget] [--platform wide|tiktok|square]" >&2
    exit 1
fi

if [[ "$DRY_RUN" -ne 1 && -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2; exit 1
fi

# ── PLATFORM → ASPECT RATIO ───────────────────────────────────────────────────
case "$PLATFORM" in
    wide|16:9|landscape|youtube)  ASPECT="16:9" ;;
    tiktok|reel|vertical|9:16)   ASPECT="9:16" ;;
    square|1:1)                   ASPECT="1:1" ;;
    *)                            ASPECT="16:9" ;;
esac

# ── PATHS ──────────────────────────────────────────────────────────────────────
SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag storyboard | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# Tier resolver — premium first
TIER() {
    local task="$1" q="${2:-$QUALITY}"
    local b=""; [[ "$BUDGET" == "1" ]] && b="--budget"
    python3 "$SKILL_DIR/scripts/tiers.py" "$task" --quality "$q" $b 2>/dev/null
}

# All shots use premium hero model (S=gemini-3-pro via nano-banana)
HERO_MODEL="$(TIER image)"
HERO_SUB="$(python3 "$SKILL_DIR/scripts/tiers.py" image --quality "$QUALITY" $([[ "$BUDGET" == "1" ]] && echo --budget) --sub-flags 2>/dev/null)"
# Detail insert can use B tier (faster, still high quality, saves spend)
DETAIL_MODEL="$(TIER image b)"

# Shared lighting register
LIGHTING="dominant neon practicals, atmospheric haze, layered depth foreground to background, lens flares, slight chromatic aberration"

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
echo "━━━ Storyboard 5-Shot Pipeline ━━━"
echo "  Subject  : $SUBJECT"
echo "  Location : $LOCATION"
echo "  Style    : $STYLE"
echo "  Aspect   : $ASPECT ($PLATFORM)"
echo "  Output   : $OUT_DIR"
echo ""

# shellcheck disable=SC2086
run_step "Shot 1/5: EWS establishing ($HERO_MODEL)" "~\$0.15 (premium)" -- \
    comfy generate $HERO_MODEL $HERO_SUB \
        --prompt "EWS bird's eye crane up of $LOCATION, atmospheric environment establishing $SUBJECT setting, no main character visible yet, $LIGHTING, $STYLE" \
        $(AF $HERO_MODEL "$ASPECT") \
        --download "$OUT_DIR/01_establish.png"

# shellcheck disable=SC2086
run_step "Shot 2/5: MCU character intro ($HERO_MODEL)" "~\$0.15 (premium)" -- \
    comfy generate $HERO_MODEL $HERO_SUB \
        --prompt "MCU low angle of $SUBJECT, $LOCATION background visible behind out-of-focus, hero stance, looking off-camera with focused gaze, $LIGHTING, $STYLE" \
        $(AF $HERO_MODEL "$ASPECT") \
        --download "$OUT_DIR/02_intro.png"

run_step "Shot 3/5: ECU detail insert ($DETAIL_MODEL)" "~\$0.04" -- \
    comfy generate "$DETAIL_MODEL" \
        --prompt "ECU rack focus of a single specific object the character is interacting with (hand, weapon, document, locket — pick contextually relevant for $SUBJECT), $LOCATION lighting bleeds into frame, $LIGHTING, $STYLE" \
        $(AF "$DETAIL_MODEL" "$ASPECT") \
        --download "$OUT_DIR/03_detail.png"

# shellcheck disable=SC2086
run_step "Shot 4/5: MS action beat ($HERO_MODEL)" "~\$0.15 (premium)" -- \
    comfy generate $HERO_MODEL $HERO_SUB \
        --prompt "MS dutch angle of $SUBJECT mid-action — sudden movement, motion implied through pose, $LOCATION dynamic background, $LIGHTING with motion blur cue, $STYLE" \
        $(AF $HERO_MODEL "$ASPECT") \
        --download "$OUT_DIR/04_action.png"

# shellcheck disable=SC2086
run_step "Shot 5/5: WS resolution ($HERO_MODEL)" "~\$0.15 (premium)" -- \
    comfy generate $HERO_MODEL $HERO_SUB \
        --prompt "WS eye level of $SUBJECT in $LOCATION, resolution beat, character standing still or walking away, emotional register of consequence, $LIGHTING, $STYLE" \
        $(AF $HERO_MODEL "$ASPECT") \
        --download "$OUT_DIR/05_resolution.png"

# Optional grid composite
if command -v magick >/dev/null 2>&1; then
    IMAGES=()
    for img in "$OUT_DIR/01_establish.png" "$OUT_DIR/02_intro.png" "$OUT_DIR/03_detail.png" "$OUT_DIR/04_action.png" "$OUT_DIR/05_resolution.png"; do
        [[ -f "$img" ]] && IMAGES+=("$img")
    done
    if [[ ${#IMAGES[@]} -ge 2 ]]; then
        GRID="$OUT_DIR/00_storyboard.png"
        magick montage "${IMAGES[@]}" -tile 5x1 -geometry +5+5 -background black "$GRID" 2>/dev/null && \
            echo "   grid: $GRID" || true
    fi
fi

# ── SUMMARY ───────────────────────────────────────────────────────────────────
echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  Pipeline completed with ${#FAILED_STEPS[@]} failed step(s):"
    for s in "${FAILED_STEPS[@]}"; do echo "     ✗ $s"; done
    echo "   See: $FAIL_LOG"
else
    echo "✅ Storyboard complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
