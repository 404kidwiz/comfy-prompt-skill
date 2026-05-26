#!/usr/bin/env bash
# style-variants.sh — Generate same poster in 4 style registers via nano-banana.
#
# Demonstrates the skill's range. ~$0.04 total. ~30s.

set -uo pipefail

[[ -z "${COMFY_API_KEY:-}" ]] && { echo "error: COMFY_API_KEY not set" >&2; exit 1; }

SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
OUT_DIR="$(python3 "$SKILL_DIR/scripts/organize.py" path --tag style-variants | xargs dirname)"
mkdir -p "$OUT_DIR"

declare -A VARIANTS=(
  [ghibli]="square poster, bold hand-lettered display text 'comfy-prompt' in cream ivory upper third with soft painterly edges, subtitle 'every style, every model, one workflow' in clay-amber monospace, 2x2 bento of hand-painted Ghibli countryside, seaside town, forest path, lantern square — soft watercolor brushwork, earth tones, dusty pinks, faded blues, dreamy Studio Ghibli aesthetic, no terminals"
  [noir]="square poster, bold display serif text 'comfy-prompt' in pure white upper third with hard chiaroscuro shadow diagonal beneath, subtitle 'every style, every model, one workflow' in bone gray monospace, 2x2 bento of classic film noir — trenchcoat detective under streetlamp, smoky jazz piano, venetian blind alley figure, fog-soaked stairs silhouette — pure B&W high contrast, chiaroscuro lighting, 1940s noir, no terminals"
  [cyberpunk]="square poster, bold sans-serif text 'comfy-prompt' as glowing neon hologram cyan-magenta gradient upper third with chromatic aberration edges, subtitle 'every style, every model, one workflow' in amber holographic monospace, 2x2 bento of photoreal cyberpunk Blade Runner — rain-soaked neon Tokyo alley, holographic megastructure billboards, trenchcoat figure with neon umbrella, flying vehicle at smog sunset — dominant neon practicals, atmospheric haze, wet reflective surfaces, no terminals"
  [pixar]="square poster, bold rounded sans-serif text 'comfy-prompt' in cream with soft 3D extrusion upper third, subtitle 'every style, every model, one workflow' in coral monospace, 2x2 bento of Pixar 3D scenes — adorable rounded character with expressive eyes, vibrant treehouse village, cozy animated kitchen with steaming pot, magical floating island with rainbow waterfall — soft rounded geometry, warm cinematic grading, optimistic register, no terminals"
)

for name in "${!VARIANTS[@]}"; do
    prompt="${VARIANTS[$name]}"
    out="$OUT_DIR/poster-$name.png"
    echo "▶ $name (~\$0.01)..."
    comfy generate nano-banana --prompt "$prompt" --download "$out" 2>&1 | grep -E "Saved|error" | head -2
    python3 "$SKILL_DIR/scripts/embed.py" "$out" --prompt "$prompt" --model nano-banana --cost 0.01 2>/dev/null || true
done

python3 "$SKILL_DIR/scripts/gallery.py" "$OUT_DIR" 2>/dev/null && echo "gallery: $OUT_DIR/index.html"
echo "━━━ Variant pack: $OUT_DIR ━━━"
ls -lh "$OUT_DIR" | grep poster-
