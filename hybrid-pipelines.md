# Hybrid Cloud + Local Pipelines

When to stack Comfy Cloud and Local for best results.

The default heuristic: **cloud for hero / fast / max-quality stills; local for batch /
animation / privacy / no-cost iteration.** Real wins come from combining them.

---

## Pattern 1: Cloud hero still → Local Wan 2.2 animation

**When to use:** You need premium hero-frame quality for a video, but cloud video
models are expensive or rate-limited.

```bash
# Cloud: high-quality hero still
comfy generate flux-ultra \
    --prompt "<full MCSLA prompt>" \
    --aspect_ratio 16:9 \
    --download /tmp/hero.png

# Local: animate from hero (no per-call cost, full control over duration)
comfy launch --background

python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Image to Video (Wan 2.2).json" \
    --prompt "subtle camera dolly in, hair drifts in breeze, eyes blink once at 2s, no extreme motion" \
    --out /tmp/run.json

comfy run --workflow /tmp/run.json --wait --timeout 600 --verbose
```

**Why:** Cloud Flux Ultra gives world-class hero image fidelity. Wan 2.2 locally gives
you unlimited iteration on the animation timing without burning credits.

---

## Pattern 2: Cloud seedance video → Local frame interpolation

**When to use:** Cloud video gen at 24fps but you need 60fps for smooth playback.

```bash
# Cloud: generate 24fps clip
comfy generate seedance \
    --prompt "<motion prompt>" \
    --duration 5 \
    --aspect_ratio 16:9 \
    --async

# (wait for job, resume + download)
comfy generate resume seedance <job_id> --download /tmp/raw.mp4

# Local: interpolate to 60fps
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Frame Interpolation.json" \
    --out /tmp/interp.json
# (Note: workflow may need manual input video path swap — see blueprint)

comfy run --workflow /tmp/interp.json --wait --timeout 600
```

**Why:** Seedance handles motion physics, local frame interpolation gives smooth
60fps without paying extra cloud credits.

---

## Pattern 3: Cloud nano-banana style transfer → Local Wan 2.2 video

**When to use:** Need a specific visual style applied to a reference image, then
animated.

```bash
# Cloud: style-transfer the reference photo to target aesthetic
comfy generate nano-banana \
    --image ./photo.jpg \
    --prompt "transform to Studio Ghibli painted matte aesthetic, soft watercolor brushwork, warm desaturated palette" \
    --download /tmp/styled.png

# Local: animate styled keyframe
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Image to Video (Wan 2.2).json" \
    --prompt "gentle ambient motion — leaves rustle, hair drifts, ambient particles, no character motion" \
    --out /tmp/animate.json

comfy run --workflow /tmp/animate.json --wait --timeout 600
```

---

## Pattern 4: Cloud upscale chain (large output)

**When to use:** Need a final 4K+ image. Cloud upscale is faster than local 4x GAN.

```bash
# 1. Cloud base generation (1024x1024)
comfy generate flux-pro --prompt "<...>" --download /tmp/base.png

# 2. Cloud first upscale (1024 → 2048)
comfy generate stability-upscale-fast --image /tmp/base.png --download /tmp/2k.png

# 3. Cloud creative upscale (2048 → 4096, slower)
comfy generate stability-upscale-creative --image /tmp/2k.png --download /tmp/4k.png

# OR Local 4x GAN as final step (free, slightly slower)
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Image Upscale(Z-image-Turbo).json" \
    --out /tmp/upscale.json
comfy run --workflow /tmp/upscale.json --wait --timeout 300
```

---

## Pattern 5: Local batch (100 variations) → Cloud final hero

**When to use:** Concept exploration phase — want 100 cheap variations, pick best,
then finalize with cloud.

```bash
# Local batch — vary seeds, no cloud cost
for seed in $(seq 1 100); do
    python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
        "/Users/dawizkidmal/ComfyUI/blueprints/Text to Image (Flux.1 Dev).json" \
        --prompt "<exploration prompt>" \
        --seed "$seed" \
        --out "/tmp/var_${seed}.json"
    comfy run --workflow "/tmp/var_${seed}.json" --wait --timeout 120 --no-verbose
done

# Sweep all outputs into organized folder
python3 ~/.claude/skills/comfy-prompt/scripts/organize.py sweep \
    --tag exploration --model wan-flux1-dev --since-hours 1

# Pick the best, then finalize at hero quality
comfy generate flux-ultra \
    --prompt "<refined version of best variant>" \
    --aspect_ratio 16:9 \
    --download /tmp/hero_final.png
```

---

## Pattern 6: Cloud edit → Local inpaint

**When to use:** Need a precise edit that needs masking. Cloud `flux-fill` doesn't
always nail mask precision; local inpainting with manual mask is more controllable.

```bash
# 1. Cloud: generate base image
comfy generate flux-pro --prompt "<...>" --download /tmp/base.png

# 2. Create mask in your image editor (white = edit area, black = preserve)
# Save as /tmp/mask.png

# 3. Local inpaint with precise mask
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Image Inpainting (Flux.1 Fill Dev).json" \
    --prompt "<what to fill the masked area with>" \
    --out /tmp/inpaint.json
# (Note: image + mask paths must be edited into workflow JSON manually for inpaint nodes)
comfy run --workflow /tmp/inpaint.json --wait --timeout 300
```

---

## Decision matrix: when cloud vs local

| Need | Choose |
|------|--------|
| Premium hero still, max fidelity | Cloud `flux-ultra` |
| 100+ variations to explore | Local Wan/Flux blueprints |
| Specific partner model (Seedance, Pika, Grok) | Cloud (only path) |
| Long video (10s+) | Cloud `seedance` or local Wan 2.2 |
| Frame interpolation | Local (no cloud equivalent) |
| Background removal | Cloud `recraft-rmbg` (fast) |
| Precise inpaint with manual mask | Local |
| Style transfer from reference | Cloud `nano-banana` or `flux-kontext` |
| Privacy-sensitive content | Local (data never leaves machine) |
| Batch processing 50+ images | Local (no per-call cost) |
| Maximum text fidelity | Cloud `ideogram` |
| 3D model from image | Local `Image to Model (Hunyuan3d 2.1).json` |
| Vectorize to SVG | Cloud `recraft-vectorize` (no local equivalent) |

---

## Tracking hybrid pipelines

Use `jobs.py` for async cloud calls + `organize.py sweep` for local outputs:

```bash
# After running a hybrid pipeline:
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py pending     # check async cloud jobs
python3 ~/.claude/skills/comfy-prompt/scripts/organize.py sweep --tag <pipeline-name>
```
