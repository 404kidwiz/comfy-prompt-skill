#!/usr/bin/env bash
# instagram-ad.sh — End-to-end Instagram product ad pipeline.
#
# Pipeline:
#   1. Hero still on white seamless          (flux-ultra)      ~$0.10
#   2. Background removal                    (recraft-rmbg)    ~$0.02
#   3. Background replacement (lifestyle)    (recraft-replace-bg) ~$0.07
#   4. Upscale to 4K                         (stability-upscale-fast) ~$0.05
#   5. Animate to vertical clip              (pika-i2v, async) ~$0.40
#
# Usage:
#   ./instagram-ad.sh "matte black coffee mug" "sunlit Scandinavian kitchen, wood counter, plants"
#   ./instagram-ad.sh "product" "background" --platform reel   # explicit platform
#   ./instagram-ad.sh "product" "background" --retry 2         # 2 retries per step
#   ./instagram-ad.sh "product" "background" --skip-on-fail    # continue on step failure
#
# Requires: COMFY_API_KEY. Output: ~/Comfy-Output/<YYYY-MM>/instagram-ad/
# Total est. cost: ~$0.64 per full run

set -uo pipefail

# ── ARGS ──────────────────────────────────────────────────────────────────────
PRODUCT=""
LIFESTYLE=""
PLATFORM="reel"   # default: 9:16
MAX_RETRIES=1
SKIP_ON_FAIL=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --platform) PLATFORM="$2"; shift 2 ;;
        --retry)    MAX_RETRIES="$2"; shift 2 ;;
        --skip-on-fail) SKIP_ON_FAIL=1; shift ;;
        -*)         echo "unknown flag: $1" >&2; exit 1 ;;
        *)
            if [[ -z "$PRODUCT" ]]; then   PRODUCT="$1"
            elif [[ -z "$LIFESTYLE" ]]; then LIFESTYLE="$1"
            fi
            shift ;;
    esac
done

if [[ -z "$PRODUCT" || -z "$LIFESTYLE" ]]; then
    echo "usage: $0 \"product description\" \"lifestyle background\" [--platform reel|tiktok|square] [--retry N] [--skip-on-fail]" >&2
    exit 1
fi

if [[ -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2
    exit 1
fi

# ── PLATFORM → ASPECT RATIO ────────────────────────────────────────────────
case "$PLATFORM" in
    tiktok|reel|vertical|9:16) ASPECT="9:16" ;;
    square|1:1|instagram)      ASPECT="1:1" ;;
    wide|16:9|youtube)         ASPECT="16:9" ;;
    *)                         ASPECT="9:16" ;;
esac

# ── PATHS ────────────────────────────────────────────────────────────────────
SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag instagram-ad | xargs dirname)"
mkdir -p "$OUT_DIR"
FAIL_LOG="$OUT_DIR/_failures.log"

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# ── HELPERS ──────────────────────────────────────────────────────────────────
FAILED_STEPS=()

run_step() {
    # run_step <step_label> <est_cost> -- <comfy command...>
    local label="$1"
    local cost="$2"
    shift 2
    # consume the '--' separator if present
    [[ "${1:-}" == "--" ]] && shift

    local attempt=0
    local rc=0

    echo "▶ $label  (est. $cost)"
    while [[ $attempt -le $MAX_RETRIES ]]; do
        if [[ $attempt -gt 0 ]]; then
            echo "  ↻ retry $attempt/$MAX_RETRIES ..."
        fi
        if "$@"; then
            rc=0
            break
        else
            rc=$?
            attempt=$((attempt + 1))
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
echo "━━━ Instagram Ad Pipeline ━━━"
echo "  Product  : $PRODUCT"
echo "  Lifestyle: $LIFESTYLE"
echo "  Platform : $PLATFORM ($ASPECT)"
echo "  Output   : $OUT_DIR"
echo ""

HERO="$OUT_DIR/01_hero.png"
run_step "Step 1/5: Hero on white seamless (flux-ultra)" "~\$0.10" -- \
    comfy generate flux-ultra \
        --prompt "$PRODUCT on seamless white background, MCU static locked-off camera, soft overhead key with even fill, catalog photography, ultra-sharp, color-accurate, deep blacks, no environmental clutter, photoreal" \
        $(AF flux-ultra 1:1) \
        --download "$HERO" || { HERO=""; }

CUTOUT="$OUT_DIR/02_cutout.png"
if [[ -n "${HERO:-}" && -f "$HERO" ]]; then
    run_step "Step 2/5: Background remove (recraft-rmbg)" "~\$0.02" -- \
        comfy generate recraft-rmbg --image "$HERO" --download "$CUTOUT" || { CUTOUT=""; }
else
    echo "  ⏭  Step 2 skipped — hero not available"
    CUTOUT=""
fi

LIFESTYLE_IMG="$OUT_DIR/03_lifestyle.png"
if [[ -n "${CUTOUT:-}" && -f "$CUTOUT" ]]; then
    run_step "Step 3/5: Lifestyle background (recraft-replace-bg)" "~\$0.07" -- \
        comfy generate recraft-replace-bg \
            --image "$CUTOUT" \
            --prompt "$LIFESTYLE, soft natural light, keep product lighting consistent with new environment" \
            --download "$LIFESTYLE_IMG" || { LIFESTYLE_IMG=""; }
else
    echo "  ⏭  Step 3 skipped — cutout not available"
    LIFESTYLE_IMG=""
fi

UPSCALED="$OUT_DIR/04_4k.png"
INPUT_FOR_UPSCALE="${LIFESTYLE_IMG:-${HERO:-}}"
if [[ -n "${INPUT_FOR_UPSCALE:-}" && -f "$INPUT_FOR_UPSCALE" ]]; then
    run_step "Step 4/5: Upscale to 4K (stability-upscale-fast)" "~\$0.05" -- \
        comfy generate stability-upscale-fast --image "$INPUT_FOR_UPSCALE" --download "$UPSCALED" || { UPSCALED=""; }
else
    echo "  ⏭  Step 4 skipped — no input image available"
    UPSCALED=""
fi

INPUT_FOR_ANIM="${UPSCALED:-${LIFESTYLE_IMG:-${HERO:-}}}"
if [[ -n "${INPUT_FOR_ANIM:-}" && -f "$INPUT_FOR_ANIM" ]]; then
    # Async submission — no retry (would duplicate jobs); just log and continue
    echo "▶ Step 5/5: Animate vertical clip (pika-i2v, async)  (est. ~\$0.40)"
    # pika-i2v has no aspect flag — inherits from source image
    ANIMATE_JSON=$(comfy generate pika-i2v \
        --image "$INPUT_FOR_ANIM" \
        --prompt "subtle camera dolly in over 5 seconds, steam rising from product, background elements drifting gently in soft breeze, hero product stays still and sharp" \
        --duration 5 \
        --resolution 1080p \
        --async --json 2>&1) || true

    JOB_ID=$(echo "$ANIMATE_JSON" | python3 -c "
import sys, re
data = sys.stdin.read()
m = re.search(r'\"id\"\s*:\s*\"([^\"]+)\"', data) or re.search(r'job[_-]?id[\"\\s:=]+([a-zA-Z0-9_-]+)', data)
print(m.group(1) if m else '')
" 2>/dev/null || echo "")

    if [[ -n "${JOB_ID:-}" ]]; then
        python3 "$SKILL_DIR/scripts/jobs.py" log pika-i2v "$JOB_ID" \
            --prompt "$PRODUCT lifestyle ad animation" --note "instagram-ad recipe"
        echo "  ✓ async job logged: $JOB_ID"
        echo "  resume: comfy generate resume pika-i2v $JOB_ID --download $OUT_DIR/05_animated.mp4"
    else
        echo "  ⚠  Step 5/5 — could not parse job_id, check pika-i2v output above manually" >&2
        FAILED_STEPS+=("Step 5/5: job_id not captured")
    fi
else
    echo "  ⏭  Step 5 skipped — no input image available"
fi

# ── SUMMARY ───────────────────────────────────────────────────────────────────
echo ""
if [[ ${#FAILED_STEPS[@]} -gt 0 ]]; then
    echo "⚠  Pipeline completed with ${#FAILED_STEPS[@]} failed step(s):"
    for s in "${FAILED_STEPS[@]}"; do echo "     ✗ $s"; done
    echo "   See: $FAIL_LOG"
else
    echo "✅ Pipeline complete."
fi
echo "   Output: $OUT_DIR"
ls -lh "$OUT_DIR" 2>/dev/null || true
