#!/usr/bin/env bash
# demo-video.sh — Generate the demo video for launching comfy-prompt.
#
# Creates a 10-second cinematic video that demonstrates the workflow visually.
# Uses seedance (async, audio-aware) — ~$0.60, ~2min from submit to ready.
#
# The video shows: terminal generating prompts → outputs appearing on screen →
# brand assets organizing themselves — a literal animation of the workflow.

set -euo pipefail

if [[ -z "${COMFY_API_KEY:-}" ]]; then
    echo "error: COMFY_API_KEY not set" >&2
    exit 1
fi

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"

PROMPT="cinematic wide shot of a developer workstation at night, three ultrawide monitors arranged in arc, screens slowly light up one by one with cascading terminal output and image generation thumbnails appearing in grid layout, hand of a developer typing rhythmically at backlit cyan mechanical keyboard, slow Steadicam push-in over 10 seconds toward the central monitor, condensed steam drifting from coffee mug across the lens, soft amber bias light pulses subtly with each new image render, deep navy and charcoal color palette with amber accent, anamorphic 35mm letterbox, crushed blacks, photoreal cinematic register, no text visible on screens just abstract code and image grids, hero composition with negative space top-right for title overlay"

OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag launch-kit | xargs dirname)"
mkdir -p "$OUT_DIR"

echo "━━━ Demo Video Generation ━━━"
echo "  Model: seedance (async, audio-capable)"
echo "  Aspect: 16:9"
echo "  Duration: 10s"
echo "  Estimated cost: ~\$0.60"
echo "  Estimated wait: ~2 minutes async"
echo ""

# Pre-spend lint
python3 "$SKILL_DIR/scripts/lint.py" "$PROMPT" --model seedance --type video --aspect 16:9 --quiet || true

AF() { python3 "$SKILL_DIR/scripts/aspect_flags.py" "$@" 2>/dev/null; }

echo "▶ Submitting async generation..."
RESPONSE=$(comfy generate seedance \
    --prompt "$PROMPT" \
    $(AF seedance 16:9) \
    --duration 10 \
    --async --json 2>&1)

echo "$RESPONSE"

JOB_ID=$(echo "$RESPONSE" | python3 -c "
import sys, re
data = sys.stdin.read()
m = re.search(r'\"id\"\\s*:\\s*\"([^\"]+)\"', data) or re.search(r'job[_-]?id[\"\\s:=]+([a-zA-Z0-9_-]+)', data)
print(m.group(1) if m else '')
" 2>/dev/null || echo "")

if [[ -z "$JOB_ID" ]]; then
    echo "⚠  Could not extract job_id — check response above" >&2
    exit 1
fi

# Log job
python3 "$SKILL_DIR/scripts/jobs.py" log seedance "$JOB_ID" \
    --prompt "$PROMPT" \
    --note "launch-kit hero demo video" \
    --cost 0.60

OUTPUT_PATH="$OUT_DIR/demo-video.mp4"

echo ""
echo "✅ Async job submitted: $JOB_ID"
echo ""
echo "Next steps:"
echo "  1. Wait ~2 minutes for seedance to finish"
echo "  2. Check status:    cf jobs pending"
echo "  3. Resume + download when ready:"
echo "       comfy generate resume seedance $JOB_ID --download $OUTPUT_PATH"
echo "       python3 $SKILL_DIR/scripts/jobs.py complete $JOB_ID --output $OUTPUT_PATH"
echo ""
echo "  OR start the auto-watch daemon to handle it for you:"
echo "       python3 $SKILL_DIR/scripts/watch.py --loop"
echo ""
echo "Output will land at: $OUTPUT_PATH"
echo "Use on X thread tweet #7 or as LinkedIn post slide 2."
