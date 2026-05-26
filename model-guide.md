# Comfy Model Guide — Cloud + Local

All cloud models accessed via `comfy generate <model>` with `COMFY_API_KEY` set.
All local models accessed via `comfy run --workflow <path>` after `comfy launch --background`.

---

## Cloud Image Models — Head to Head

| Model | Partner | Quality | Faces | Style range | Text | Speed | Best for |
|-------|---------|---------|-------|-------------|------|-------|----------|
| `flux-2` | BFL | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | Latest Flux, max fidelity |
| `flux-pro` | BFL | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | Cinematic, photoreal |
| `flux-ultra` | BFL | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | Ultra-HD, hero shots |
| `nano-banana` | Google | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | Versatile, text rendering, fast |
| `dalle` | OpenAI | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | Text-in-image, instruction following |
| `stability-sd3` | Stability | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | SD3.5 — wide style range |
| `stability-ultra` | Stability | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | Stable Image Ultra |
| `ideogram` | Ideogram | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | Strongest text rendering |
| `grok` | xAI | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Grok Imagine — versatile |
| `recraft` | Recraft | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | Illustration, vector-style |
| `reve` | Reve | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | General purpose |
| `runway` | Runway | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Quick concept |

## Cloud Image-Edit Models

| Model | Purpose | Input | Speed |
|-------|---------|-------|-------|
| `flux-kontext` | High-quality edit | image + prompt | ★★★☆☆ |
| `flux-kontext-max` | Max-quality edit (slower) | image + prompt | ★★☆☆☆ |
| `flux-canny` | ControlNet from edge | canny edge image | ★★★☆☆ |
| `flux-depth` | ControlNet from depth | depth image | ★★★☆☆ |
| `flux-fill` | Inpaint | image + mask | ★★★☆☆ |
| `flux-expand` | Outpaint | image | ★★★☆☆ |
| `dalle-edit` | OpenAI image edit | image + prompt | ★★★★☆ |
| `ideogram-edit` | Ideogram edit | image + prompt | ★★★★☆ |
| `grok-edit` | Grok image edit | image + prompt | ★★★★☆ |
| `nano-banana` | Gemini Flash Image edit | image + prompt | ★★★★★ |
| `recraft-i2i` | Image-to-image | image + prompt | ★★★★☆ |
| `recraft-inpaint` | Recraft inpaint | image + mask | ★★★★☆ |
| `reve-edit` | Reve edit | image + prompt | ★★★★☆ |

## Cloud Specialty Models

| Model | Purpose |
|-------|---------|
| `recraft-rmbg` | Background remove |
| `recraft-replace-bg` | Replace background |
| `recraft-vectorize` | Vectorize to SVG |
| `recraft-upscale` | Standard upscale |
| `recraft-upscale-creative` | Creative upscale |
| `stability-upscale` | Conservative upscale |
| `stability-upscale-creative` | Creative upscale (async) |
| `stability-upscale-fast` | Fast upscale |

## Cloud Video Models

| Model | Partner | Motion | Realism | Duration | Audio | Mode | Best for |
|-------|---------|--------|---------|----------|-------|------|----------|
| `seedance` | ByteDance | ★★★★★ | ★★★★☆ | 3-12s | ✅ | async | T2V + I2V, complex motion |
| `pika` | Pika | ★★★★☆ | ★★★☆☆ | 5s | — | async | T2V, clean motion |
| `pika-i2v` | Pika | ★★★★☆ | ★★★☆☆ | 5s | — | async | I2V, social clips |
| `runway` | Runway | ★★★☆☆ | ★★★☆☆ | — | — | sync | Quick concept |
| `runway-i2v` | Runway | ★★★★☆ | ★★★★☆ | — | — | async | I2V, hero shots |
| `vidu` | Vidu | ★★★★☆ | ★★★☆☆ | — | — | async | T2V general |
| `vidu-i2v` | Vidu | ★★★★☆ | ★★★☆☆ | — | — | async | I2V general |
| `vidu-extend` | Vidu | ★★★★☆ | ★★★☆☆ | — | — | async | Extend existing video |
| `grok-video` | xAI | ★★★★☆ | ★★★★☆ | — | — | async | T2V via Grok Imagine |

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
| `First-Last-Frame to Video.json` | F-L-V | Generic F-L-V |
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

## Decision Flowchart

```
Is this IMAGE or VIDEO?

├── IMAGE
│   ├── Need text in image (poster, sign, label)?
│   │   ├── Strongest text → ideogram (cloud) or dalle (cloud)
│   │   └── Fast text → nano-banana (cloud)
│   ├── Portrait / face-focused?
│   │   ├── Cloud max quality → flux-pro / nano-banana
│   │   └── Local → Text to Image (Flux.2 Dev).json
│   ├── Cinematic still / hero shot?
│   │   ├── Cloud → flux-pro, flux-ultra, stability-ultra
│   │   └── Local → Text to Image (Flux.2 Dev).json
│   ├── Wide style range / illustration?
│   │   ├── Cloud → stability-sd3, recraft, reve
│   │   └── Local → Text to Image (NetaYume Lumina).json
│   ├── Edit existing image?
│   │   ├── Versatile cloud → nano-banana, flux-kontext, recraft-i2i
│   │   ├── Max quality → flux-kontext-max
│   │   └── Local → Image Edit (Flux.2 Dev).json or (Qwen 2511).json
│   ├── Inpaint? → flux-fill (cloud) or Image Inpainting (Flux.1 Fill Dev).json (local)
│   ├── Outpaint? → flux-expand (cloud) or Image Outpainting (Qwen-Image).json (local)
│   ├── Remove background? → recraft-rmbg (cloud) or Remove Background (BiRefNet).json
│   ├── Upscale? → stability-upscale-fast (cloud) or Image Upscale(Z-image-Turbo).json
│   ├── Vectorize? → recraft-vectorize (cloud, no local)
│   └── ControlNet (pose/canny/depth)? → flux-canny/flux-depth (cloud) or *.Z-Image-Turbo.json (local)
│
└── VIDEO
    ├── Text-to-video (motion-heavy)?
    │   ├── Cloud → seedance (3-12s, audio), grok-video
    │   └── Local → Text to Video (Wan 2.2).json
    ├── Text-to-video (clean / quick)?
    │   └── Cloud → pika, vidu, runway
    ├── Image-to-video?
    │   ├── Cloud → seedance, pika-i2v, runway-i2v, vidu-i2v
    │   └── Local → Image to Video (Wan 2.2).json or LTX-2.3
    ├── First+last frame? → First-Last-Frame to Video (LTX-2.3).json (local)
    ├── Extend existing video? → vidu-extend (cloud)
    ├── ControlNet video (canny/depth/pose)? → local LTX 2.0 blueprints
    ├── Video inpaint? → Video Inpaint(Wan2.1 VACE).json (local)
    ├── Video upscale? → Video Upscale(GAN x4).json (local)
    └── Frame interpolation? → Frame Interpolation.json (local)
```

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

## Approximate credit cost (verify against platform.comfy.org for actuals)

These are rough partner-cost estimates. ALWAYS check current pricing at
[platform.comfy.org](https://platform.comfy.org) — partner rates change.

| Tier | Models | Approx. cost per call |
|------|--------|------------------------|
| Low | `nano-banana`, `recraft`, `recraft-i2i`, `recraft-rmbg`, `recraft-vectorize`, `reve` | $0.01-0.03 |
| Low-Medium | `dalle`, `ideogram`, `stability-sd3`, `stability-upscale-fast`, `grok` | $0.03-0.06 |
| Medium | `flux-pro`, `flux-kontext`, `stability-ultra`, `runway`, `vidu` | $0.05-0.10 |
| Medium-High | `flux-2`, `flux-ultra`, `flux-kontext-max`, `dalle-edit` | $0.08-0.15 |
| High (video) | `seedance` (3-5s), `pika`, `pika-i2v`, `runway-i2v`, `vidu-i2v`, `vidu-extend` | $0.15-0.40 |
| Very High (video) | `seedance` (10-12s), `grok-video` | $0.40-1.00+ |

**Cost-saving tactics:**
- Use `nano-banana` for exploration drafts, `flux-ultra` for finals only
- Test prompt variations locally (free) before committing to cloud video
- Use `stability-upscale-fast` over `stability-upscale-creative` for routine upscales
- Always pre-flight with `scripts/preflight.py` to avoid wasted calls on bad inputs
- Track spending via Comfy Cloud dashboard at platform.comfy.org

## Async vs sync — execution patterns

**Sync flow:**
```bash
comfy generate flux-pro --prompt "..." --download out.png
# Blocks ~5-30s, downloads when done
```

**Async flow (required for video):**
```bash
# 1. Submit (returns immediately with job_id)
RESPONSE=$(comfy generate seedance --prompt "..." --duration 10 --async --json)
JOB_ID=$(parse-job-id-from-response)

# 2. Log it
python3 scripts/jobs.py log seedance "$JOB_ID" --prompt "..."

# 3. Poll later
python3 scripts/jobs.py pending

# 4. When ready, resume + download
comfy generate resume seedance "$JOB_ID" --download out.mp4
python3 scripts/jobs.py complete "$JOB_ID" --output out.mp4
```

---

## Verified working examples (2026-05-26)

```bash
export COMFY_API_KEY=comfyui-...

# Text-to-image, sync, fast
comfy generate nano-banana --prompt "..." --download /tmp/{index}.{ext}
# → 1024×1024 PNG in ~10s

# Browse all available
comfy generate list

# Schema for a specific model
comfy generate schema flux-pro
```
