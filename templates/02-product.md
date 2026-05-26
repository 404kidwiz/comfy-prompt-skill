# Template: Product / Commercial / UGC

## Genre / Use case
Product hero shots, e-comm photography, commercial ads, unboxing UGC, lifestyle product
shots, brand identity stills.

## When to use
User asks for product photo, hero shot, e-commerce, UGC, commercial, ad imagery,
catalog image.

## Recommended models
- **Hero still**: `flux-ultra` or `flux-pro` for max fidelity. `nano-banana` for fast iteration.
- **Background variation**: `recraft-replace-bg` after generating cutout via `recraft-rmbg`.
- **Lifestyle UGC video**: `seedance` (cloud, audio) for testimonial-style. `pika-i2v` for static-to-motion.
- **Vectorize logo**: `recraft-vectorize`.

## Example prompt — `flux-ultra` (hero still)

```
Model: flux-ultra (cloud)
Aspect: 1:1 | Style: Studio Product

MCU Static Locked-off camera. Zero movement.
A matte-black ceramic coffee mug on a polished walnut desk.
A thin ribbon of steam curls upward from the rim.
Single soft key light from upper-left, gentle fill from right.
Sunlight bleeds through unseen window onto desk surface, soft golden glow on wood grain.
Catalog photography aesthetic. Ultra-sharp focus. Color-accurate. Deep blacks.
Subtle shadow under mug, no shadows touching product surface.

Run:
comfy generate flux-ultra --prompt "static MCU of matte-black ceramic coffee mug on polished walnut desk, thin ribbon of steam curling up from rim, soft key from upper-left, gentle fill from right, sunlight bleeding through unseen window onto desk, soft golden glow on wood grain, catalog photography, ultra-sharp, color-accurate, deep blacks, subtle shadow under mug" --aspect_ratio 1:1 --download /tmp/mug_{index}.{ext}
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "matte-black ceramic" | Specific material + finish — not "dark mug" |
| "polished walnut desk" | Texture surface details the model can render distinctly |
| "thin ribbon of steam curls upward" | Atmospheric motion cue (works in video) or implied warmth (still) |
| "Static Locked-off camera. Zero movement." | Camera contract — product shots need stability |
| "Single soft key from upper-left, gentle fill from right" | Lighting setup, not "good lighting" |
| "Catalog photography aesthetic" | Specific commercial register |
| "subtle shadow under mug, no shadows touching product" | Anti-failure: prevents harsh shadow obscuring product |

## Negative constraints to append
- Environmental clutter: `no busy background, no surrounding objects competing for attention`
- Product distortion: `no warped product silhouette, no melted edges, no incorrect proportions`
- Logo / branding: if generating a real-looking product, add `text on product kept generic or blank — for branding composite in post`

## Common mistakes
1. **Too many props** — Hero shots have ONE subject. Strip secondary objects.
2. **Generic lighting** — "good lighting" or "professional lighting" ignored. Name direction + quality.
3. **Asking for logo / brand text** — Most image models butcher logos. Generate clean product, composite branding separately.
4. **Mixed registers** — "Lifestyle but also studio" = neither. Pick one.

## Variations
- **Lifestyle context**: Add environment ("on a kitchen counter at golden hour, plants soft-blurred behind"). Change camera to "soft handheld drift, shallow depth of field".
- **E-comm cutout**: Generate on white seamless background, then `recraft-rmbg` to isolate.
- **UGC selfie style**: Camera → POV / Handheld. Phone-camera aesthetic. "Iphone front camera 4K, natural daylight, slight motion blur".
- **Pack shot / multi-angle**: Generate 4 angles with same lighting, comp in grid.

## Multi-stage product pipeline
```bash
# 1. Hero still on seamless white
comfy generate flux-ultra --prompt "matte-black ceramic mug on seamless white background, soft top key, even fill, catalog photography, ultra-sharp" --aspect_ratio 1:1 --download /tmp/hero.png

# 2. Background removal
comfy generate recraft-rmbg --image /tmp/hero.png --download /tmp/cutout.png

# 3. Replace with lifestyle background
comfy generate recraft-replace-bg --image /tmp/cutout.png --prompt "sunlit Scandinavian kitchen, wood counter, soft morning light, plants soft-blurred in background" --download /tmp/lifestyle.png

# 4. Animate for social
comfy generate pika-i2v --image /tmp/lifestyle.png --prompt "subtle camera dolly in, steam rising, plants swaying gently in breeze" --duration 5 --async
```

## UGC video variant — `seedance`
```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s

A young woman holds up a matte-black coffee mug to the camera, smiling.
"I drink this every morning."
Camera: Handheld phone-style, slight drift.
Sunlit kitchen behind her, soft window light.
Style: Authentic UGC, iPhone front-camera aesthetic, natural color, slight grain.

Run:
comfy generate seedance --prompt "young woman holds up matte-black coffee mug to camera smiling, dialogue 'I drink this every morning', handheld phone-style camera slight drift, sunlit kitchen behind her, soft window light, authentic UGC iPhone front-camera aesthetic, natural color, slight grain" --duration 8 --aspect_ratio 9:16 --async
```
