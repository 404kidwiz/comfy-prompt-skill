# Comfy Model Guide — Premium-First (v3.2.0)

All cloud models via `comfy generate <model>` with `COMFY_API_KEY` set.
All local models via `comfy run --workflow <path>` after `comfy launch --background`.

**Philosophy:** premium quality is the default. Budget mode is opt-in via `--budget`.

---

## The Tier System

Every task routes through a 4-tier ladder. Pick by task, not by model name.

| Tier | Quality | When to use |
|------|---------|-------------|
| **S** | Best-in-class. No compromise. | Hero shots, client deliverables, finals, anything user will see. |
| **A** | Strong premium. ~70% S quality, ~50% S cost. | High-volume premium work (bulk of finals). |
| **B** | Solid mid. Reliable, fast, cheap. | Internal review, mood boards, drafts that survive. |
| **C** | Bargain. | Iteration, throwaway tests, experimental prompts. |

**Default tier is S.** Pass `--budget` to downshift S→B everywhere in one shot.

---

## Quick Resolution Table

What you ask for → what runs.

### Image (text-to-image)

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `nano-banana --model gemini-3-pro-image-preview` | $0.15 | Gemini 3 Pro — premium |
| A | `flux-ultra` | $0.10 | BFL Flux Pro 1.1 Ultra — top BFL |
| B | `flux-pro` | $0.04 | BFL Flux Pro 1.1 — fast cinematic |
| C | `nano-banana` (Gemini 2.5 Flash) | $0.01 | Cheapest reliable |

### Image with text (poster, sign, label)

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `ideogram` | $0.04 | Strongest text rendering in image |
| A | `nano-banana --model gemini-3-pro-image-preview` | $0.15 | Premium text |
| B | `dalle` | $0.08 | OpenAI — solid for text |
| C | `nano-banana` (Gemini 2.5 Flash) | $0.01 | Cheapest |

### Image edit

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `flux-kontext-max` | $0.12 | Max-quality edit |
| A | `flux-kontext` | $0.08 | Pro edit |
| B | `nano-banana` (Gemini 2.5 Flash) | $0.01 | Fast Gemini edit |
| C | `recraft-i2i` | $0.04 | Cheap image-to-image |

### Inpaint / Outpaint / Background

| Task | Tier S model | Notes |
|------|-------------|-------|
| Inpaint | `flux-fill` | Mask-driven edit |
| Outpaint | `flux-expand` | Extend any side |
| Background remove | `recraft-rmbg` | Best in class |
| Background replace | `recraft-replace-bg` | (S+A) — `ideogram-bg` at B |

### Illustration / vector-style

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `recraft` | $0.03 | Illustration / vector king |
| A | `ideogram` | $0.04 | Versatile |
| B | `stability-sd3` | $0.03 | Wide style range |
| C | `recraft` | $0.03 | Default |

### Video (text-to-video)

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `kling --model_name kling-v3` | $0.60 | Kling v3 (latest, top quality) |
| A | `seedance` | $0.60 | ByteDance — cinematic motion |
| B | `hailuo` | $0.30 | MiniMax — fast, solid |
| C | `pika` | $0.30 | Cheapest reliable |

### Video (image-to-video)

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `kling-i2v --model_name kling-v3` | $0.60 | Premium I2V |
| A | `runway-i2v` | $0.45 | Cinematic |
| B | `vidu-i2v` | $0.40 | Solid mid |
| C | `pika-i2v` | $0.40 | Cheapest |

### Upscale

| Tier | Model | Cost | Notes |
|------|-------|------|-------|
| **S** | `recraft-upscale-creative` | $0.15 | Creative upscale, slow |
| A | `stability-upscale-creative` | $0.15 | Stability creative |
| B | `recraft-upscale` | $0.02 | Standard |
| C | `stability-upscale-fast` | $0.05 | Fast |

---

## Using the Tier Resolver

### From shell — `cf auto`

```bash
cf auto image "cinematic hero shot of a coffee mug" --platform wide
# → routes to nano-banana --model gemini-3-pro-image-preview (S tier)

cf auto image "draft concept" --quality b
# → routes to flux-pro

cf auto image "hero shot" --budget
# → downshifts S→B → flux-pro

cf auto video-t2v "drone shot over Tokyo at night, 10 seconds"
# → kling --model_name kling-v3

cf auto video-i2v "subtle camera dolly in over 5 seconds" --image hero.png --budget
# → vidu-i2v (downshifted from kling-v3)
```

### From Python

```python
import sys
sys.path.insert(0, "scripts")
from tiers import pick

p = pick("image")                      # default S
# → Pick(model='nano-banana', sub_model='gemini-3-pro-image-preview', sub_flag='--model', quality='s', task='image')

p = pick("video-t2v", quality="a")     # tier A explicit
# → Pick(model='seedance', sub_model=None, sub_flag=None, quality='a', task='video-t2v')

p = pick("image", budget=True)         # downshift
# → Pick(model='flux-pro', sub_model=None, sub_flag=None, quality='b', task='image')
```

### From recipe script

```bash
# After sourcing/defining QUALITY and BUDGET vars
MODEL="$(TIER image)"
SUB_FLAGS="$(python3 "$SKILL_DIR/scripts/tiers.py" image --sub-flags)"

# shellcheck disable=SC2086
comfy generate $MODEL $SUB_FLAGS --prompt "..." --download out.png
```

---

## All Cloud Image Models (full inventory)

| Model | Partner | Type | Tier | Cost |
|-------|---------|------|------|------|
| `flux-2` | BFL | text-to-image | B | $0.06 |
| `flux-pro` | BFL | text-to-image | B | $0.04 |
| `flux-ultra` | BFL | text-to-image | A | $0.10 |
| `flux-kontext` | BFL | image-edit | A | $0.08 |
| `flux-kontext-max` | BFL | image-edit | S | $0.12 |
| `flux-canny` | BFL | controlnet | — | $0.06 |
| `flux-depth` | BFL | controlnet | — | $0.06 |
| `flux-fill` | BFL | inpaint | S | $0.06 |
| `flux-expand` | BFL | outpaint | S | $0.06 |
| `nano-banana` | Google | image + edit | C-S | $0.01-0.15 |
| └ `--model gemini-2.5-flash-image` | | | C | $0.01 |
| └ `--model gemini-3-pro-image-preview` | | | S | $0.15 |
| `dalle` | OpenAI | text-to-image | B | $0.08 |
| `dalle-edit` | OpenAI | image-edit | A | $0.10 |
| `ideogram` | Ideogram | text + text-in-image | S | $0.04 |
| `ideogram-edit` | Ideogram | image-edit | — | $0.05 |
| `ideogram-bg` | Ideogram | bg-replace | B | $0.04 |
| `ideogram-reframe` | Ideogram | image-edit | — | $0.04 |
| `ideogram-remix` | Ideogram | image-edit | — | $0.05 |
| `stability-sd3` | Stability | text-to-image | B | $0.03 |
| `stability-ultra` | Stability | text-to-image | A | $0.10 |
| `grok` | xAI | text-to-image | A | $0.12 |
| `grok-edit` | xAI | image-edit | — | $0.15 |
| `reve` | Reve | text-to-image | A | $0.10 |
| `reve-edit` | Reve | image-edit | — | $0.12 |
| `recraft` | Recraft | text-to-image | S (illust.) | $0.03 |
| `recraft-i2i` | Recraft | image-to-image | C | $0.04 |
| `recraft-inpaint` | Recraft | inpaint | B | $0.07 |
| `recraft-rmbg` | Recraft | bg-remove | S | $0.02 |
| `recraft-replace-bg` | Recraft | bg-replace | S | $0.07 |
| `recraft-vectorize` | Recraft | vectorize | S | $0.03 |
| `recraft-upscale` | Recraft | upscale | B | $0.02 |
| `recraft-upscale-creative` | Recraft | upscale | S | $0.15 |
| `stability-upscale` | Stability | upscale | B | $0.08 |
| `stability-upscale-fast` | Stability | upscale | C | $0.05 |
| `stability-upscale-creative` | Stability | upscale | A | $0.15 |

## All Cloud Video Models

| Model | Partner | Type | Tier | Cost |
|-------|---------|------|------|------|
| `kling` | Kling | text-to-video | S/B | $0.20-0.60 |
| └ `--model_name kling-v3` | | | S | $0.60 |
| └ `--model_name kling-v2-6` | | | A | $0.55 |
| └ `--model_name kling-v1-6` | | | B | $0.30 |
| └ `--model_name kling-v1` | | | C | $0.20 |
| `kling-i2v` | Kling | image-to-video | S/B | $0.20-0.60 |
| `kling-lipsync` | Kling | lipsync | — | $0.50 |
| `kling-extend` | Kling | video-extend | — | $0.30 |
| `seedance` | ByteDance | t2v + i2v | A | $0.60 |
| `pika` | Pika | text-to-video | C | $0.30 |
| `pika-i2v` | Pika | image-to-video | C | $0.40 |
| `runway` | Runway | text-to-image | — | $0.35 |
| `runway-i2v` | Runway | image-to-video | A | $0.45 |
| `hailuo` | MiniMax | text-to-video | B | $0.30 |
| `luma` | Luma | text-to-video | A | $0.40 |
| `luma-i2v` | Luma | image-to-video | A | $0.45 |
| `vidu` | Vidu | text-to-video | B | $0.30 |
| `vidu-i2v` | Vidu | image-to-video | B | $0.40 |
| `vidu-extend` | Vidu | video-extend | — | $0.25 |
| `moonvalley-t2v` | MoonValley | text-to-video | A | $0.40 |
| `moonvalley-i2v` | MoonValley | image-to-video | A | $0.40 |
| `grok-video` | xAI | text-to-video | A | $0.50 |

---

## Local Image Blueprints

Path prefix: `/Users/dawizkidmal/ComfyUI/blueprints/`

| Blueprint | Type | Use |
|-----------|------|-----|
| `Text to Image (Flux.1 Dev).json` | T2I | Standard Flux 1 |
| `Text to Image (Flux.2 Dev).json` | T2I | Latest Flux 2 local |
| `Text to Image (Flux.1 Krea Dev).json` | T2I | Flux Krea variant |
| `Text to Image (Qwen-Image).json` | T2I | Qwen-Image |
| `Text to Image (Qwen-Image 2512).json` | T2I | Qwen 2512 |
| `Text to Image (Z-Image-Turbo).json` | T2I | Z-Image fast |
| `Text to Image (Z-Image-Base).json` | T2I | Z-Image base |
| `Text to Image (Ernie Image).json` | T2I | Baidu Ernie |
| `Text to Image (Ernie Image Turbo).json` | T2I | Ernie fast |
| `Text to Image (NetaYume Lumina).json` | T2I | NetaYume Lumina |
| `Image Edit (Flux.2 Dev).json` | edit | Flux 2 edit |
| `Image Edit (Flux.2 Klein 4B).json` | edit | Flux 2 Klein 4B edit |
| `Image Edit (Qwen 2509).json` | edit | Qwen 2509 edit |
| `Image Edit (Qwen 2511).json` | edit | Qwen 2511 edit |
| `Image Edit (LongCat Image Edit).json` | edit | LongCat edit |
| `Image Edit (FireRed Image Edit 1.1).json` | edit | FireRed edit |
| `Image Inpainting (Flux.1 Fill Dev).json` | inpaint | Flux inpaint |
| `Image Inpainting (Qwen-image).json` | inpaint | Qwen inpaint |
| `Image Outpainting (Qwen-Image).json` | outpaint | Qwen outpaint |
| `Image Upscale(Z-image-Turbo).json` | upscale | Z-Image upscale |
| `Image to Layers(Qwen-Image-Layered).json` | layered | Decompose to layers |
| `Image to Depth Map (Lotus).json` | depth | Lotus depth est. |
| `Image Captioning (gemini).json` | caption | Gemini caption |
| `Image Segmentation (SAM3).json` | segment | SAM3 segmentation |
| `Image to Model (Hunyuan3d 2.1).json` | 3D | Image-to-3D |
| `Remove Background (BiRefNet).json` | rmbg | BG remove |
| `Pose to Image (Z-Image-Turbo).json` | pose | Pose-conditioned |
| `Canny to Image (Z-Image-Turbo).json` | canny | Edge-conditioned |
| `Depth to Image (Z-Image-Turbo).json` | depth | Depth-conditioned |
| `ControlNet (Z-Image-Turbo).json` | controlnet | Generic ControlNet |

## Local Video Blueprints

| Blueprint | Type | Use |
|-----------|------|-----|
| `Text to Video (Wan 2.2).json` | T2V | Wan 2.2 — best local T2V |
| `Text to Video (LTX-2.3).json` | T2V | LTX fast T2V |
| `Image to Video (Wan 2.2).json` | I2V | Wan 2.2 I2V |
| `Image to Video (LTX-2.3).json` | I2V | LTX I2V |
| `First-Last-Frame to Video (LTX-2.3).json` | F-L-V | Start + end frame |
| `Canny to Video (LTX 2.0).json` | controlnet-v | Edge to video |
| `Depth to Video (ltx 2.0).json` | controlnet-v | Depth to video |
| `Pose to Video (LTX 2.0).json` | controlnet-v | Pose to video |
| `Video Inpaint(Wan2.1 VACE).json` | inpaint-v | Video inpaint |
| `Video Upscale(GAN x4).json` | upscale-v | 4x GAN upscale |
| `Frame Interpolation.json` | interp | Frame interpolation |
| `Video Captioning (Gemini).json` | caption-v | Gemini video caption |
| `Video Segmentation (SAM3).json` | segment-v | SAM3 video |
| `Video Stitch.json` | stitch | Stitch clips |
| `Get Any Video Frame.json` | frame | Extract frame |

## Local Audio Blueprint

| Blueprint | Type | Use |
|-----------|------|-----|
| `Text to Audio (ACE-Step 1.5).json` | T2A | ACE-Step audio gen |

---

## Aspect Ratios — what each model accepts

Most cloud models accept: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `4:5`, `5:4`.

Anamorphic (2.35:1, 2.39:1) is NOT an output ratio for most cloud models — it's a
**Look line style register**. Use 16:9 output + "anamorphic widescreen, letterboxed
black bars" in the Look line.

Local blueprints take pixel dimensions directly via empty-latent nodes — edit the
workflow JSON to set width/height.

---

## Cost / mode notes

| Mode | What it means |
|------|---------------|
| `sync` | Blocks until done. Use for image gen <30s. |
| `async` | Returns job_id immediately. Use `--async` then `comfy generate resume <model> <job_id>`. Required for video. |

`--timeout <sec>` on sync calls (default 300s). Set higher for slow models.

---

## Cost-saving tactics

- **Premium-first defaults** — but pass `--budget` on any recipe / `cf auto` for B-tier downshift in one shot.
- Use S tier for finals only. Use B/C for iteration drafts.
- Test prompt variations locally (free) before committing to cloud video.
- Always pre-flight with `cf preflight <model>` before async video calls.
- Track spending: `cf jobs budget` and Comfy Cloud dashboard at platform.comfy.org.
- Content-hash dedup is on by default — identical re-runs return existing output free.

---

## Async vs sync — execution patterns

**Sync flow:**
```bash
cf auto image "cinematic hero shot" --platform wide
# Blocks ~5-30s, downloads when done
```

**Async flow (required for video):**
```bash
# 1. Submit
cf auto video-t2v "drone shot over Tokyo at night" --platform wide
# → returns job_id, auto-logged

# 2. Poll later
cf jobs pending

# 3. Auto-poll background daemon
cf watch --loop
```

---

## Verified working examples (2026-05-26)

```bash
export COMFY_API_KEY=comfyui-...

# Premium image (auto-routed to Gemini 3 Pro)
cf auto image "matte black coffee mug on wooden counter, golden hour"

# Premium video (auto-routed to kling-v3)
cf auto video-t2v "drone shot over Tokyo at night, neon reflections"

# Budget mode (downshift everything to B tier)
cf auto image "draft concept exploration" --budget

# Override tier explicitly
cf auto image "..." --quality a   # Force tier A (flux-ultra)

# Preview what would route
cf tiers image           # → nano-banana
cf tiers image --budget  # → flux-pro
cf tiers video-t2v       # → kling --model_name kling-v3

# Browse all available cloud models
cf models

# Schema for a specific model
comfy generate schema flux-pro
```
