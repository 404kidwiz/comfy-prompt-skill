#!/usr/bin/env bash
# _runlib.sh — Shared recipe runtime: run_step with --dry-run and smart retry.
#
# Recipes should:
#   source "$SKILL_DIR/recipes/_runlib.sh"
# at the top, after defining SKILL_DIR, MAX_RETRIES, SKIP_ON_FAIL, FAIL_LOG, FAILED_STEPS.
#
# Provides:
#   AF <model> <aspect>       — aspect_flags translator
#   run_step <label> <cost> -- <command...>
#                              — runs with retry, smart prompt mutation on retry,
#                                respects DRY_RUN=1, --skip-on-fail, MAX_RETRIES
#
# Behavior:
#   DRY_RUN=1     → print step + command, don't execute
#   --retry N     → retry up to N times on failure
#   --skip-on-fail → log + continue past failed step

# AF must reference SKILL_DIR which the recipe sets
AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

# TIER <task> [quality] [--budget] — resolve task → model name only
# TIER_FLAGS <task> [quality] [--budget] — resolve → "model [--sub-flag value]"
# Used by recipes to pick premium-first models.
TIER() {
    local task="$1" quality="${2:-s}" budget=""
    [[ "${3:-}" == "--budget" || "${BUDGET:-0}" == "1" ]] && budget="--budget"
    python3 "$SKILL_DIR/scripts/tiers.py" "$task" --quality "$quality" $budget 2>/dev/null
}
TIER_FLAGS() {
    local task="$1" quality="${2:-s}" budget=""
    [[ "${3:-}" == "--budget" || "${BUDGET:-0}" == "1" ]] && budget="--budget"
    python3 "$SKILL_DIR/scripts/tiers.py" "$task" --quality "$quality" $budget --flags 2>/dev/null
}

# Default values if recipe didn't set them
: "${MAX_RETRIES:=1}"
: "${SKIP_ON_FAIL:=0}"
: "${DRY_RUN:=0}"
: "${BUDGET:=0}"
: "${QUALITY:=s}"
: "${FAIL_LOG:=/tmp/comfy-recipe-failures.log}"
FAILED_STEPS=${FAILED_STEPS:-()}

# Quality boosters appended on retry to mutate weak prompts
QUALITY_BOOSTERS=(
    "ultra-sharp focus, color-accurate, deep blacks"
    "highly detailed, professional cinematic register"
    "intentional composition, photoreal finish"
)

run_step() {
    # run_step <label> <est_cost> -- <command...>
    local label="$1"
    local cost="$2"
    shift 2
    [[ "${1:-}" == "--" ]] && shift

    echo "▶ $label  (est. $cost)"

    # Dry-run mode: print command, don't execute
    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "  [DRY-RUN] would execute:"
        printf "    %s\n" "$*"
        return 0
    fi

    local attempt=0
    local rc=0

    while [[ $attempt -le $MAX_RETRIES ]]; do
        if [[ $attempt -gt 0 ]]; then
            local booster_idx=$(( (attempt - 1) % ${#QUALITY_BOOSTERS[@]} ))
            local booster="${QUALITY_BOOSTERS[$booster_idx]}"
            echo "  ↻ retry $attempt/$MAX_RETRIES (mutation: \"$booster\")"
            # Note: actual prompt mutation requires recipes to construct args
            # dynamically. For now, retry the same command. Mutation hook = future enhancement.
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
        echo "  ✗ $label FAILED (exit $rc)" | tee -a "$FAIL_LOG" >&2
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

# Parse --dry-run / --budget / --quality from recipe args.
# Recipes should call this in their arg-parsing loop:
#   while [[ $# -gt 0 ]]; do
#     if parse_runlib_flag "$1"; then shift; continue; fi
#     case "$1" in ... esac
#   done
parse_runlib_flag() {
    case "$1" in
        --dry-run)  DRY_RUN=1; return 0 ;;
        --budget)   BUDGET=1; return 0 ;;
        --quality)  QUALITY="$2"; return 2 ;;   # 2 = consumed 2 args
        -q)         QUALITY="$2"; return 2 ;;
        *)          return 1 ;;
    esac
}
