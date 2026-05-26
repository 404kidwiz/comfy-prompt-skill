# Comfy Prompt Examples

Examples per model + before-after improvements. All original, no IP / real names.

---

## Cinematic Still Images

### Sci-Fi Character Tension — `flux-pro`
```
Model: flux-pro (cloud)
Aspect: 16:9 | Style: Cinematic

Medium Close-Up (MCU) Low Angle Dolly Zoom of a weathered space pilot in a cracked visor.
Staring intensely off-camera, jaw clenched.
The sparking, smoke-filled cockpit of a crashing starfighter.
Flashing red emergency lights, hard side-key illumination.
Photorealistic sci-fi cinematic, ultra-sharp detail, anamorphic widescreen.

Run:
comfy generate flux-pro --prompt "MCU low angle of weathered space pilot in cracked visor, jaw clenched, intense stare off-camera, sparking smoke-filled cockpit of crashing starfighter, flashing red emergency lights, hard side-key illumination, photorealistic sci-fi cinematic, ultra-sharp detail, anamorphic widescreen letterboxed" --aspect_ratio 16:9 --download /tmp/{request_id}.{ext}
```

### Epic Fantasy Scale — `stability-ultra`
```
Model: stability-ultra (cloud)
Aspect: 16:9 | Style: Concept Art

Extreme Wide Shot (EWS) Bird's Eye Crane Up of a lone knight in blackened armor.
Kneeling in snow with a glowing broadsword planted in the ground.
A vast frozen lake surrounded by jagged obsidian mountains.
Cold blue hour, soft diffused moonlight piercing heavy clouds.
Dark fantasy concept art, high contrast, 4K.

Run:
comfy generate stability-ultra --prompt "EWS bird's eye of lone knight in blackened armor kneeling in snow with glowing broadsword planted in ground, vast frozen lake surrounded by jagged obsidian mountains, cold blue hour, diffused moonlight piercing heavy clouds, dark fantasy concept art, high contrast, 4K" --aspect_ratio 16:9 --download /tmp/{request_id}.{ext}
```

### Psychological Thriller Detail — `nano-banana`
```
Model: nano-banana (cloud)
Aspect: 3:4 | Style: 1970s Thriller

Extreme Close-Up (ECU) Dutch Angle Rack Focus of a trembling hand clutching an ornate silver key.
Knuckles white from gripping too hard, skin textured and cold.
A dimly lit vintage hallway with peeling floral wallpaper, blurred background.
Sickly yellow-green practical light, deep crushed shadows.
1970s psychological thriller, heavy film grain, muted palette.

Run:
comfy generate nano-banana --prompt "ECU dutch angle of trembling hand clutching ornate silver key, knuckles white, skin textured and cold, dimly lit vintage hallway with peeling floral wallpaper blurred behind, sickly yellow-green practical light, crushed shadows, 1970s psychological thriller, heavy film grain, muted palette" --download /tmp/thriller_{index}.{ext}
```

### Product Hero — `flux-ultra`
```
Model: flux-ultra (cloud)
Aspect: 1:1 | Style: Studio Product

MCU Static Locked-off camera. Zero movement.
A matte-black coffee mug on polished walnut desk.
Steam curls upward in a thin ribbon.
Single soft key from upper-left, gentle fill, no shadows on product.
Sunlight bleeds through unseen window onto desk surface.
Catalog photography aesthetic, ultra-sharp, color-accurate, deep blacks.

Run:
comfy generate flux-ultra --prompt "static MCU of matte-black coffee mug on polished walnut desk, thin ribbon of steam curling up, soft key from upper-left, sunlight bleeding through unseen window onto desk surface, catalog photography, ultra-sharp, color-accurate, deep blacks" --aspect_ratio 1:1 --download /tmp/mug_{index}.{ext}
```

### Text-in-Image Poster — `ideogram`
```
Model: ideogram (cloud)
Aspect: 9:16 | Style: Vintage Poster

Vintage travel poster of a coastal lighthouse at golden hour.
Lighthouse top-third of frame, ocean spanning lower two-thirds.
Bold typography centered top: "CAPE ATLAS — EST. 1887" in art-deco serif, ivory on deep teal.
Smaller subtitle bottom: "VISIT THE NORTHERN COAST" in thinner sans-serif.
Painted illustration aesthetic, screen-printed look, muted ochre and teal palette.

Run:
comfy generate ideogram --prompt "vintage travel poster of coastal lighthouse at golden hour, lighthouse top-third of frame, ocean spanning lower two-thirds, bold art-deco serif text 'CAPE ATLAS — EST. 1887' ivory on deep teal, subtitle 'VISIT THE NORTHERN COAST' in thinner sans-serif, painted illustration, screen-printed, muted ochre and teal palette" --aspect_ratio 9:16 --download /tmp/poster.png
```

---

## Image Edit Examples

### Style Transfer — `flux-kontext`
```
Model: flux-kontext (cloud)
Input: ./portrait.jpg
Edit: Transform to 1970s Polaroid look, warm color shift, soft focus, faded edges, slight motion blur.

Run:
comfy generate flux-kontext --image ./portrait.jpg --prompt "transform to 1970s Polaroid look, warm color shift, soft focus, faded edges, slight motion blur, vintage instant photo aesthetic" --download /tmp/polaroid.png
```

### Background Replace — `nano-banana`
```
Model: nano-banana (cloud)
Input: ./product.jpg
Edit: Replace background with a sun-lit Mediterranean balcony, terracotta tile floor, white-washed walls, blue ocean visible at horizon. Keep product lighting consistent with new environment.

Run:
comfy generate nano-banana --image ./product.jpg --prompt "replace background with sun-lit Mediterranean balcony, terracotta tile floor, white-washed walls, blue ocean visible at horizon, keep product lighting consistent with new environment" --download /tmp/replaced.png
```

### Outpaint — `flux-expand`
```
Model: flux-expand (cloud)
Input: ./close-up-portrait.jpg
Edit: Extend canvas outward — full body visible, urban rooftop environment, dusk sky, city lights below.

Run:
comfy generate flux-expand --image ./close-up-portrait.jpg --prompt "extend frame to show full body, urban rooftop environment, dusk sky, city lights below, cinematic lighting" --download /tmp/expanded.png
```

---

## Video Examples

### Action — `seedance` (audio-capable)
```
Model: seedance (cloud, async)
Duration: 10s | Aspect: 16:9 | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls. Steam rises from food carts.
Neon signs fracture in every puddle.
Camera: Action Run — low behind her, matching pace.
A metal gate drops ahead. She slides under it without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast.

Run:
comfy generate seedance --prompt "woman in tactical jacket sprints through rain-soaked night market, weaving between stalls, steam rising from food carts, neon fracturing in puddles, action run camera low behind her matching pace, metal gate drops ahead she slides under it without breaking stride, cinematic, cold blue shadows, warm amber market light, high contrast" --duration 10 --aspect_ratio 16:9 --async
# Returns job_id — then:
comfy generate resume seedance <job_id> --download /tmp/chase.mp4
```

### Image-to-Video — `pika-i2v`
```
Model: pika-i2v (cloud, async)
Input: ./portrait.jpg
Duration: 5s | Aspect: 9:16

Starting from the provided image as the first frame.
Her hair lifts gently in the evening breeze. She turns her head slowly to the right,
eyes narrowing as if recognizing someone below.
Camera: slow Dolly In toward her profile.
Wind catches the dress fabric. Distant city lights begin flickering on.
Style: Cinematic, warm golden hour, shallow depth of field.

Run:
comfy generate pika-i2v --image ./portrait.jpg --prompt "hair lifts gently in evening breeze, head turns slowly to the right, eyes narrowing as if recognizing someone below, slow dolly in toward her profile, wind catches dress fabric, distant city lights flickering on, cinematic warm golden hour shallow depth of field" --duration 5 --aspect_ratio 9:16 --async
```

### Local — Wan 2.2 Text-to-Video
```
Workflow: /Users/dawizkidmal/ComfyUI/blueprints/Text to Video (Wan 2.2).json

# Edit the prompt node in the JSON to:
"A lone astronaut walks across a vast red dune at sunset, helmet glinting,
camera handheld behind, dust devils swirling at horizon, golden hour, photorealistic"

Run:
comfy launch --background
comfy run --workflow "/Users/dawizkidmal/ComfyUI/blueprints/Text to Video (Wan 2.2).json" --wait --timeout 600 --verbose
# Output in /Users/dawizkidmal/ComfyUI/output/
```

---

## Before → After — Prompt Improvement Examples

### Example 1: Vague → Specific (Action Video)

**Before (weak):**
```
A cool action scene in a city at night with a woman running and cameras moving dramatically.
```

Problems: No named camera, "cool" unmeasurable, "cameras moving dramatically" generic.

**After (strong):**
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 10s

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls. Steam rises from food carts. Neon fractures in puddles.
Camera: Action Run — low behind her, matching pace.
A metal gate drops ahead. She slides under it without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast. 16:9.
```

What changed: Named camera preset (Action Run), specific environment details, active
verbs (sprints, slides, weaving), explicit color grade, concrete style.

---

### Example 2: Over-described I2V → Motion-first

**Before (weak):**
```
A beautiful woman with long dark hair and brown eyes wearing a red silk dress
is standing on a balcony with a city behind her at sunset. The sky is orange
and pink with some clouds. There are tall buildings in the background. She looks elegant.
```

Problems: Re-describes everything already in the input image. No motion cues. "Beautiful"
and "elegant" are style slop the model can't act on.

**After (strong):**
```
Model: pika-i2v
Starting from the provided image as the first frame.
Her hair lifts gently in the evening breeze. She turns her head slowly to the right,
eyes narrowing slightly as if recognizing someone below.
Camera: slow Dolly In toward her profile.
Wind catches the dress fabric. City lights begin flickering on in the distance.
Style: Cinematic, warm golden hour, shallow depth of field.
```

---

### Example 3: Generic style → concrete look

**Before (weak):**
```
Make it look cinematic and moody.
```

Problems: "Cinematic" and "moody" can mean ten different things.

**After (strong):**
```
Look: Anamorphic widescreen 2.39:1 letterboxed. Cold blue ambient + warm amber practicals.
Film grain heavy. Crushed blacks. Bleach-bypass color, low saturation.
Single side-key light, deep chiaroscuro shadows.
```

---

### Example 4: Wrong model for task

**Before:**
```
"Generate a poster with the text 'GRAND OPENING TONIGHT' in flux-pro"
```

Problem: `flux-pro` is great at images but weak at text rendering.

**After (route to right model):**
```
Use `ideogram` or `dalle` for text-in-image. Flux for the visuals, comp the text in
post if needed.

comfy generate ideogram --prompt "vintage poster with text 'GRAND OPENING TONIGHT' in bold art-deco serif, ivory on deep red, gold accents, painted illustration aesthetic" --aspect_ratio 9:16
```

---

## Model Pairings — Multi-stage Workflows

### Image → Upscale
```bash
# 1. Generate base
comfy generate flux-pro --prompt "..." --download /tmp/base.png

# 2. Upscale to 4K
comfy generate stability-upscale-fast --image /tmp/base.png --download /tmp/4k.png
```

### Image → Video
```bash
# 1. Hero image
comfy generate flux-ultra --prompt "..." --download /tmp/hero.png

# 2. Animate
comfy generate pika-i2v --image /tmp/hero.png --prompt "subtle motion, hair drift, slow dolly in" --duration 5 --async
```

### Image → Edit → Vectorize
```bash
# 1. Generate
comfy generate flux-pro --prompt "..." --download /tmp/img.png

# 2. Remove background
comfy generate recraft-rmbg --image /tmp/img.png --download /tmp/cutout.png

# 3. Vectorize
comfy generate recraft-vectorize --image /tmp/cutout.png --download /tmp/logo.svg
```
