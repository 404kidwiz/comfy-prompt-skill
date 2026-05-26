# Comfy Recipes

Multi-step pipelines combining cloud + local Comfy operations.
Each recipe is a self-contained `.sh` script — runnable from anywhere.

## Available recipes

| Recipe | What it does | Time | Cost |
|--------|--------------|------|------|
| `instagram-ad.sh` | Product → cutout → lifestyle BG → 4K upscale → 5s animation | ~3-5 min | medium-high (5 cloud calls) |
| `character-sheet.sh` | Hero portrait → 3 angle variations with identity locked | ~1-2 min | low-medium (4 cloud calls) |
| `storyboard-5shot.sh` | 5-shot cinematic sequence with consistent style register | ~1-2 min | low-medium (5 cloud calls) |
| `product-lifestyle.sh` | Product hero → 4 lifestyle scene composites | ~2-3 min | medium (6 cloud calls) |

## Prerequisites

```bash
export COMFY_API_KEY=comfyui-...
```

Optional: install ImageMagick for automatic grid composites:
```bash
brew install imagemagick    # macOS
```

## Usage

```bash
# Instagram product ad
./instagram-ad.sh "matte black coffee mug" "sunlit Scandinavian kitchen, plants, wood counter"

# Character sheet
./character-sheet.sh "weathered space pilot, late 30s, cracked visor, worn leather jacket"

# Storyboard
./storyboard-5shot.sh "lone bounty hunter tracking a target" "rain-soaked Tokyo neon alley at 2am" "anamorphic cyberpunk Blade Runner"

# Product lifestyle A/B
./product-lifestyle.sh "matte black coffee mug"
```

## Output

All recipes write to `~/Comfy-Output/<YYYY-MM>/<recipe-tag>/`.

Async jobs are logged via `scripts/jobs.py` so you can poll status later:
```bash
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py pending
```

## Writing your own recipe

Pattern:
1. Check `COMFY_API_KEY`
2. Resolve output dir via `organize.py path`
3. Generate hero / base via cloud sync model
4. Chain transformations (rmbg, replace-bg, upscale, edit)
5. Final step: async video gen + log to `jobs.py`
6. Optional grid composite with ImageMagick

Use existing recipes as templates.
