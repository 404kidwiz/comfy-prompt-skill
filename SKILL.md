---
name: comfy-prompt
description: |
  Write production-grade prompts for ComfyUI Cloud (cloud.comfy.org) and local
  ComfyUI blueprints. Provides MCSLA prompt structure (Model · Camera · Subject ·
  Look · Action), cinematic vocabulary, model routing across BFL Flux, OpenAI DALL-E,
  Stability SD3, Ideogram, xAI Grok, ByteDance Seedance, Pika, Runway, Vidu, Recraft,
  Reve, Google nano-banana, plus the 60+ local blueprints in ~/ComfyUI/blueprints/.

  Use this skill when the user asks to:
  - Write or refine an image/video prompt for Comfy
  - Pick the right model for a generation
  - Get a cinematic prompt with proper camera/motion vocabulary
  - Match a genre (action, product, horror, portrait, landscape, sci-fi, etc.)
  - Improve a weak prompt
  - Generate a still image, video, edit, or upscale via Comfy

  Pairs with `comfyui-cli` skill — this writes the prompt, comfyui-cli executes it.
version: 1.0.0
license: MIT
platforms: [macos, linux]
metadata:
  tags: [comfy, comfyui, prompt, cinematic, video, image, MCSLA]
  pairs_with: comfyui-cli
  cloud_models: ["flux-2","flux-pro","flux-ultra","flux-kontext","flux-kontext-max","flux-canny","flux-depth","flux-fill","flux-expand","nano-banana","dalle","dalle-edit","stability-sd3","stability-ultra","ideogram","ideogram-edit","grok","grok-edit","grok-video","recraft","recraft-i2i","recraft-inpaint","seedance","pika","pika-i2v","runway","runway-i2v","vidu","vidu-i2v","vidu-extend","reve","reve-edit"]
---

# Comfy Prompt Skill

Sister skill to `comfyui-cli`. This writes the prompt. `comfyui-cli` runs it.

**Language rule:** Reply in whatever language the user writes in.

---

## HARD RULES — pre-delivery checklist

Run this checklist BEFORE sending any prompt response. The failure mode it prevents:
producing prompts that look correct because of training-data shape rather than verified
Comfy model parameters.

**Confirm in order:**

1. **Routing line first.** First line names model + path (cloud/local) + workflow.
   Example: `Routing: cloud → flux-pro (text-to-image, sync, 1024×1024)`.
   Missing routing line = response incomplete.

2. **Model exists and is verified.** Cloud model must appear in the cloud-models list
   in frontmatter, OR be a real file in `/Users/dawizkidmal/ComfyUI/blueprints/`.
   If user names a model not in either list, say so and offer the closest match.
   NEVER invent model names. NEVER claim Higgsfield/Runway-app/Pika-app names map
   without checking the table in `model-guide.md`.

3. **MCSLA structure intact on video prompts.** Model · Camera · Subject · Look · Action.
   Five layers, every video prompt, unless user explicitly opts out.

4. **Camera/motion vocabulary verified.** Camera preset names come from `vocab.md`.
   If user names one not in the file, say so and ask for clarification.

5. **Negative constraints appended.** Pull from `shared/negative-constraints.md`.
   Do not paraphrase — use file phrasing.

6. **Aspect ratio uses correct flag per model family.** Comfy Cloud models have
   different parameter conventions for dimensions:
   - BFL Flux (`flux-pro`, `flux-ultra`, `flux-2`): `--width INT --height INT`
   - Stability / Ideogram / Reve / Vidu / Grok: `--aspect_ratio STRING`
   - Seedance: `--ratio ENUM --resolution ENUM`
   - Runway: `--ratio ENUM`
   - DALL-E / Recraft: `--size "WxH"`
   - Pika (t2v): `--aspectRatio FLOAT` (camelCase!)
   - kontext / fill / expand / rmbg / nano-banana: no dimension flag (uses source)

   **Use the translator script** to avoid schema errors:
   ```bash
   $(python3 ~/.claude/skills/comfy-prompt/scripts/aspect_flags.py <model> <aspect>)
   ```

   Or via `cf` wrapper: `--platform tiktok|reel|wide|square` auto-translates.
   Never hand-write `--aspect_ratio` — it only works for some models.
   Anamorphic / 2.35:1 / 2.39:1 are style register (Look line), not output ratios.

7. **Prompt under 200 words.** Going over = padding. Tighten.

8. **Execution command appended.** End with the exact `comfy generate ...` or
   `comfy run --workflow ...` command the user can paste.

If items 1–8 incomplete, the response is incomplete. Fix before sending.

---

## Two execution paths

| Path | When | Skill that runs it |
|------|------|----|
| **Cloud** (`comfy generate <model>`) | Need access to BFL Flux, DALL-E, Seedance, Grok, etc. Fast, no local setup. Requires `COMFY_API_KEY`. | `comfyui-cli` § Comfy Cloud |
| **Local** (`comfy run --workflow`) | Have models downloaded, want full workflow control, no per-call cost. Need `comfy launch --background` first. | `comfyui-cli` § Local |

Default: cloud for fast prototyping, local for repeat / batch / privacy.

---

## Workflow

### Fast Path — Simple Creative Requests

User gives clear creative intent, no specific constraints ("write me a prompt for a car
chase at night"). Generate immediately with **premium-first defaults**:

| Parameter | Default |
|-----------|---------|
| Aspect ratio | 16:9 |
| Quality tier | **S (premium)** — pass `--budget` to downshift to B |
| Image model (S) | `nano-banana --model gemini-3-pro-image-preview` (Gemini 3 Pro) |
| Image model (B fallback) | `flux-pro` |
| Image-text (poster, sign) | `ideogram` (S — strongest text rendering) |
| Image edit (S) | `flux-kontext-max` |
| Video model (S) | `kling --model_name kling-v3` (latest, top quality) |
| Video model (A) | `seedance` (cinematic motion) |
| Video model (B fallback) | `hailuo` |
| Image-to-video (S) | `kling-i2v --model_name kling-v3` |
| Local image | `Text to Image (Flux.2 Dev).json` |
| Local video | `Text to Video (Wan 2.2).json` |
| Style | Cinematic |
| Duration (video) | 5s (cloud sync limits), 10s local |

Resolve via `cf auto <task> "<prompt>"` — auto-picks tier-correct model.

Do not ask clarifying questions on Fast Path. Deliver ready-to-paste prompt + command.

### Full Path — Production Requests

User signals production intent (multi-shot, specific model, budget concern, client work).
Confirm in one message:

**Required:**
- Generation type: Image / Video / Edit / Upscale
- Aspect ratio: 16:9 / 9:16 / 1:1 / 4:5 / 3:4
- Path: Cloud or Local
- Model preference (or ask me to recommend — see `model-guide.md`)

**Optional (skip if user provided):**
- Visual style
- Reference image path (for image-to-image / image-to-video)
- Duration (video)
- Negative constraints

Ask everything in ONE message — do not split rounds.

---

## Route to the right model — tier system

Full mapping → `model-guide.md`. **Premium-first tier table** (S default):

| Task | S (premium default) | A | B | C (budget) |
|------|--------------------|---|---|------------|
| `image` | `nano-banana --model gemini-3-pro-image-preview` | `flux-ultra` | `flux-pro` | `nano-banana` (Gemini 2.5 Flash) |
| `image-edit` | `flux-kontext-max` | `flux-kontext` | `nano-banana` | `recraft-i2i` |
| `image-text` (poster, sign) | `ideogram` | `nano-banana` (Gemini 3 Pro) | `dalle` | `nano-banana` (Gemini 2.5 Flash) |
| `illustration` | `recraft` | `ideogram` | `stability-sd3` | `recraft` |
| `inpaint` | `flux-fill` | `flux-fill` | `recraft-inpaint` | `recraft-inpaint` |
| `outpaint` | `flux-expand` | — | — | — |
| `bg-remove` | `recraft-rmbg` | — | — | — |
| `bg-replace` | `recraft-replace-bg` | `recraft-replace-bg` | `ideogram-bg` | — |
| `vectorize` | `recraft-vectorize` | — | — | — |
| `upscale` | `recraft-upscale-creative` | `stability-upscale-creative` | `recraft-upscale` | `stability-upscale-fast` |
| `video-t2v` | `kling --model_name kling-v3` | `seedance` | `hailuo` | `pika` |
| `video-i2v` | `kling-i2v --model_name kling-v3` | `runway-i2v` | `vidu-i2v` | `pika-i2v` |

**Local fallback** (for privacy, no-cost iteration, ControlNet):
- T2I: `Text to Image (Flux.2 Dev).json`
- I2I edit: `Image Edit (Flux.2 Klein 4B).json`
- T2V: `Text to Video (Wan 2.2).json`
- Upscale: `Image Upscale(Z-image-Turbo).json`
- Inpaint: `Image Inpainting (Flux.1 Fill Dev).json`

**Resolution shortcut:** `cf auto <task> "<prompt>" [--quality s|a|b|c] [--budget]` routes automatically.

---

## Check templates for genre match

Before writing from scratch, check `templates/`:

| User request matches | Template |
|----------------------|----------|
| Chase, pursuit, action, parkour | `templates/01-action.md` |
| Product, commercial, ad, UGC | `templates/02-product.md` |
| Portrait, character intro, close-up | `templates/03-portrait.md` |
| Landscape, nature, establishing shot | `templates/04-landscape.md` |
| Sci-fi, cyberpunk, VFX, space | `templates/05-scifi.md` |
| Cinematic still image with shot framing | `templates/06-cinematic-still.md` |

Adapt the template — don't paste verbatim.

---

## MCSLA Formula

Five layers, every prompt:

| M | C | S | L | A |
|---|---|---|---|---|
| Model | Camera | Subject | Look | Action |

**Core rules:**
- Name specific camera presets from `vocab.md`
- Describe VFX concretely (not "magical effects")
- Subject → Action → Camera → Style is the most reliable order
- Keep prompts under 200 words

### Output format

**Single prompt:**
```
**Model**: <model name> (<cloud/local>)
**Aspect ratio**: <ratio>  **Duration**: <Xs>  **Style**: <style>

<Prompt body — MCSLA composed>

**Camera**: <camera preset name from vocab.md>
**Negative**: <pulled from shared/negative-constraints.md>

**Run**:
```bash
<exact comfy generate or comfy run command>
```
```

**Two versions (when style varies):**
```
### Version 1 — <Style Name>
<Prompt>
**Run**: `<command>`

---
### Version 2 — <Style Name>
<Prompt>
**Run**: `<command>`
```

---

## @ Reference Rules

- User uploads image → `--image <path>` flag (cloud) or wire into workflow input (local)
- For image-to-video → `comfy generate <i2v_model> --image <path> --prompt "..."`
- For style transfer → describe target style in Look line, reference in `--image`
- For edits → use `flux-kontext`, `nano-banana`, or `recraft-i2i` with `--image`

---

## Shared resources

| Resource | What it contains |
|----------|------------------|
| `model-guide.md` | Full cloud + local model table, capabilities, costs, aspect ratios |
| `vocab.md` | Camera presets, angles, motion physics, lens behavior, composition |
| `prompt-examples.md` | Worked examples per model + before/after improvements |
| `templates/` | 10 genre templates: action, product, portrait, landscape, scifi, cinematic-still, horror, fashion, comedy, music-performance |
| `verticals/` | 10 business-channel templates (adapted from Roman Knox AI Video Generator): viral-hook, saas-launch, personal-brand, course-promo, faceless-channel, luxury-aesthetic, before-after, testimonial-story, ai-avatar, podcast-visual |
| `verticals/shared/` | hooks.md (12 universal patterns) · sound-design.md (4-layer stack) · platform-optimization.md (TikTok/Reels/Shorts/LinkedIn) |
| `styles/` | 7 reusable Look-line style snippets (anamorphic-1970s, studio-ghibli, cyberpunk-blade-runner, film-noir, pixar-3d, editorial-vogue, concept-art-painted) |
| `recipes/` | 4 multi-step shell pipelines (instagram-ad, character-sheet, storyboard-5shot, product-lifestyle) |
| `scripts/` | 5 Python helpers: parameterize.py, jobs.py, preflight.py, organize.py, schema_cache.py |
| `hybrid-pipelines.md` | Cloud + local stacking patterns |
| `shared/negative-constraints.md` | Negative-prompt phrases for common artifacts |

## When to use templates vs verticals

- **Templates** (`templates/`) — pick by SHAPE / STYLE / GENRE. "Action chase scene", "fashion editorial portrait", "cyberpunk still".
- **Verticals** (`verticals/`) — pick by BUSINESS USE-CASE / CHANNEL. "TikTok hook", "SaaS launch", "course promo", "testimonial reel".

Combine them: vertical for the business context + template for the visual specificity.
Example: viral-hook vertical + product template + cyberpunk style = TikTok hook for a tech product launch with neon register.

## Tooling — `scripts/` helpers

| Script | What it does |
|--------|--------------|
| `parameterize.py` | Swap prompt/seed/dims in a local blueprint JSON. `python3 .../parameterize.py <blueprint> --prompt "..." --out /tmp/run.json` |
| `jobs.py` | Track async cloud jobs + cost accounting. `jobs.py log <model> <id>`, `jobs.py pending`, `jobs.py budget`, `jobs.py complete <id>` |
| `preflight.py` | Validate API key, model, paths BEFORE spending credits. `preflight.py <model> [--image PATH] [--download PATH]` |
| `organize.py` | Build dated output paths, move/sweep files. Respects `COMFY_AUTO_OPEN=1`. `organize.py path --tag X --model flux-pro` |
| `schema_cache.py` | 24h cache for `comfy generate schema`. `schema_cache.py <model>` |
| `compare.py` | A/B test same prompt on 2–4 models in parallel. `compare.py "prompt" --models flux-pro flux-ultra nano-banana` |

**Use them.** Don't hand-paste `--download /tmp/out.png` when `organize.py path` exists.
Don't lose async job_ids — log them with `jobs.py`.

## Brand config (`brand.yaml`)

When generating assets for a specific project, client, or product line:

1. Copy `brand.yaml` to the project dir (or edit the global one in skill root).
2. Fill in: `name`, `palette`, `mood`, `lighting`, `camera`, `look_keywords`, `negatives`, `output_tag`, `preferred_image_model`.
3. Tell Claude: *"use brand config"* — the Look line and negative constraints will be injected automatically.

```bash
# Quick check what brand config says
cat ~/.claude/skills/comfy-prompt/brand.yaml | grep -v '^#' | grep -v '^$'
```

Brand config fields map to MCSLA layers:
- `palette` + `mood` + `look_keywords` → **Look** line
- `negatives` → appended to **Negative** constraints
- `lighting` → **Look** sub-line
- `camera` → **Camera** preset guidance
- `preferred_image_model` / `preferred_video_model` → **Model** selection
- `output_tag` → `--tag` arg for `organize.py`

## A/B Comparison (`scripts/compare.py`)

Same prompt across multiple models simultaneously:

```bash
# Compare 3 image models in parallel
python3 ~/.claude/skills/comfy-prompt/scripts/compare.py \
    "cinematic portrait of a detective in rain-soaked alley, cyberpunk neon register" \
    --models flux-pro flux-ultra nano-banana \
    --aspect_ratio 16:9 \
    --tag portrait-ab

# Compare i2i models with a reference image
python3 ~/.claude/skills/comfy-prompt/scripts/compare.py \
    "same character, profile view, identity locked" \
    --models flux-kontext flux-kontext-max \
    --image /tmp/hero.png \
    --seq   # sequential if you want to avoid parallel API rate limits

# Results land in:
# ~/Comfy-Output/<YYYY-MM>/compare/compare_<HH:MM:SS>/
# summary table printed to stdout
```

Or via the `cf` wrapper:
```bash
# cf doesn't have a built-in compare command — call compare.py directly
COMFY_AUTO_OPEN=1 python3 ~/.claude/skills/comfy-prompt/scripts/compare.py \
    "prompt" --models flux-pro seedance --aspect_ratio 9:16
```

## Style snippets (`styles/`)

Append a style snippet to your Look line by reference. Each file has a `Quick paste`
block at the bottom — drop that into the prompt.

```
Style: $(cat ~/.claude/skills/comfy-prompt/styles/anamorphic-1970s.md | sed -n '/Quick paste/,/```$/p' | sed -n '3p')
```

Or just include the file's `Style:` line verbatim.

## Recipes (`recipes/`)

Pre-built multi-step pipelines with failure recovery, retry, and `--platform` shortcuts.

```bash
# Basic usage
~/.claude/skills/comfy-prompt/recipes/instagram-ad.sh "matte black mug" "sunlit kitchen, plants"
~/.claude/skills/comfy-prompt/recipes/character-sheet.sh "weathered space pilot, late 30s, worn jacket"
~/.claude/skills/comfy-prompt/recipes/storyboard-5shot.sh "lone hunter tracking target" "rain-soaked Tokyo alley" "cyberpunk Blade Runner"
~/.claude/skills/comfy-prompt/recipes/product-lifestyle.sh "matte black coffee mug"

# With platform shortcut (sets aspect ratio automatically)
~/.claude/skills/comfy-prompt/recipes/instagram-ad.sh "mug" "kitchen" --platform reel      # 9:16
~/.claude/skills/comfy-prompt/recipes/storyboard-5shot.sh "subject" "loc" "style" --platform wide  # 16:9

# With failure recovery flags
~/.claude/skills/comfy-prompt/recipes/instagram-ad.sh "mug" "kitchen" --retry 2            # 2 retries per step
~/.claude/skills/comfy-prompt/recipes/product-lifestyle.sh "product" --skip-on-fail        # continue past failures
```

Platform shortcuts: `tiktok|reel|vertical → 9:16` · `wide|youtube → 16:9` · `square|instagram → 1:1`
Failure modes: `--retry N` retries failed steps N times; `--skip-on-fail` logs failures and continues.
Cost estimates printed per step. All outputs land in `~/Comfy-Output/<YYYY-MM>/<recipe-tag>/`.

---

## Pairs with comfyui-cli

This skill writes prompts. `comfyui-cli` executes them. Always end with the runnable command.

**Cloud (full discipline):**
```bash
export COMFY_API_KEY=comfyui-...

# 1. Pre-flight check (catches errors before spending credits)
python3 ~/.claude/skills/comfy-prompt/scripts/preflight.py flux-pro --download /tmp/out.png

# 2. Build organized output path
OUT=$(python3 ~/.claude/skills/comfy-prompt/scripts/organize.py path --model flux-pro --tag client-x)

# 3. Generate
comfy generate flux-pro --prompt "..." --download "$OUT"
```

**Cloud async (with job tracking):**
```bash
# Generate async, capture job_id, log it
RESPONSE=$(comfy generate seedance --prompt "..." --duration 10 --async --json)
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys, json, re; print(re.search(r'\"id\"\\s*:\\s*\"([^\"]+)\"', sys.stdin.read()).group(1))")
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py log seedance "$JOB_ID" --prompt "..."

# Later: check status
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py pending

# When done: resume + complete
comfy generate resume seedance "$JOB_ID" --download /tmp/out.mp4
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py complete "$JOB_ID" --output /tmp/out.mp4
```

**Local (with parameterize helper):**
```bash
comfy launch --background

# Swap prompt/seed/dims into blueprint
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Text to Image (Flux.1 Dev).json" \
    --prompt "..." --seed 42 --width 1024 --height 1024 \
    --out /tmp/run.json

# Execute
comfy run --workflow /tmp/run.json --wait --timeout 120

# Sweep outputs into organized tree
python3 ~/.claude/skills/comfy-prompt/scripts/organize.py sweep --tag local --model flux1-dev
```

Output dir: `~/Comfy-Output/<YYYY-MM>/<tag>/` (organized) or `~/ComfyUI/output/` (raw local).
