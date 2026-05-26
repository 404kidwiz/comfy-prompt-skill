# Template: Portrait / Character Intro

## Genre / Use case
Portrait photography, character introductions, close-ups, identity-anchored shots.
Hero face shots for cinema, editorial covers, character keyframes for video pipelines.

## When to use
User asks for portrait, character shot, close-up, headshot, identity reference,
keyframe for video, profile image.

## Recommended models
- **Best face fidelity**: `flux-pro`, `flux-ultra`, `nano-banana`.
- **Cinematic register**: `flux-pro` with explicit film vocabulary.
- **Editorial / fashion**: `stability-sd3`, `recraft` (illustration).
- **Video character intro**: `seedance` from keyframe, or `pika-i2v`.
- **Local**: `Text to Image (Flux.2 Dev).json`.

## Example prompt — `flux-pro` (cinematic portrait)

```
Model: flux-pro (cloud)
Aspect: 3:4 | Style: Cinematic Portrait

Medium Close-Up (MCU) Eye Level of a man in his late 30s with weathered features,
short dark hair flecked with gray, three-day stubble.
Looking just past camera, half-shadowed expression — neither smiling nor sad.
Worn leather jacket over a faded gray t-shirt.
Background: out-of-focus warehouse interior, distant industrial lights bokeh.
Lighting: single hard side-key from camera-right, deep chiaroscuro shadow on left half of face.
Cool blue ambient fill from above.
Style: Anamorphic widescreen letterboxed. Heavy 35mm film grain. Crushed blacks.
Bleach-bypass color, muted saturation. Photoreal cinematic.

Run:
comfy generate flux-pro --prompt "MCU eye level of man in late 30s with weathered features, short dark hair flecked with gray, three-day stubble, looking just past camera with half-shadowed expression, worn leather jacket over faded gray t-shirt, out-of-focus warehouse interior background with distant industrial light bokeh, single hard side-key from camera-right with deep chiaroscuro shadow on left half of face, cool blue ambient fill from above, anamorphic widescreen letterboxed, heavy 35mm film grain, crushed blacks, bleach-bypass color, muted saturation, photoreal cinematic" --aspect_ratio 3:4 --download /tmp/portrait_{index}.{ext}
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "late 30s with weathered features" | Specific age + texture cue, not "a man" |
| "short dark hair flecked with gray, three-day stubble" | Hair details + facial hair = identity grounding |
| "looking just past camera, half-shadowed expression" | Pose + emotional register specific |
| "worn leather jacket over faded gray t-shirt" | Wardrobe with texture words ("worn", "faded") |
| "out-of-focus warehouse interior, distant industrial lights bokeh" | Background shape + bokeh keyword |
| "single hard side-key from camera-right, deep chiaroscuro shadow on left half" | Lighting specifics named |
| "Anamorphic widescreen letterboxed" | Style register in Look line (not aspect ratio param) |
| "Heavy 35mm film grain. Crushed blacks. Bleach-bypass" | Specific film stock + grade language |

## Negative constraints to append
Pull from `shared/negative-constraints.md` § Face / Identity:
```
no asymmetric eyes, no merged irises, no missing eyelashes,
no plasticky skin texture, no waxen sheen, no melted features
```

## Common mistakes
1. **"Beautiful" / "elegant" / "stunning"** — Style slop. Model can't act on these. Describe specific features.
2. **No lighting specified** — Default lighting is flat. Always name key direction + quality.
3. **No emotional register** — "Smiling" or "neutral" lacks specificity. Use "half-shadowed expression, neither smiling nor sad" or "intense stare, jaw clenched".
4. **No depth-of-field cue** — Add "shallow depth of field" or "out-of-focus background" for cinematic register.

## Variations

### Editorial fashion — `stability-sd3`
```
Model: stability-sd3 (cloud)
Aspect: 3:4 | Style: Editorial Fashion

Full-body portrait of a woman in flowing silver couture gown.
Standing motionless against blank concrete wall.
Camera: eye level, 85mm lens, perfect symmetry.
Lighting: single overhead diffused softbox, no fill.
Style: Vogue editorial. High-contrast monochrome with single silver accent.
Magazine cover composition.
```

### Character intro video — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 5s

[0-2s] Static MCU of the same man (description from still),
slowly turning his head from profile toward camera.
[2-5s] He locks eyes with the camera. Slight squint, jaw tightens.
Camera: locked off, no movement.
Internal motion: cigarette smoke drifting past his face, hair barely moving.
Style: Anamorphic cinematic, side-key lighting, heavy grain.
```

### Identity-anchored sequence
For multi-shot work with same character:
1. Generate hero portrait with `flux-pro`.
2. Use that image as reference (`--image hero.png`) in subsequent gens.
3. Add `keep same facial features, same hair, same wardrobe` to each prompt.
4. Model: `nano-banana` or `flux-kontext` for variations.

```bash
# Hero
comfy generate flux-pro --prompt "<full description>" --download /tmp/hero.png

# Variation: different angle, same identity
comfy generate flux-kontext --image /tmp/hero.png --prompt "same character, now in profile facing left, same wardrobe, same lighting register" --download /tmp/profile.png

# Variation: different location, same identity
comfy generate nano-banana --image /tmp/hero.png --prompt "same character now standing in dimly lit alley at night, neon signs in background, same wardrobe, same age and features, anamorphic widescreen" --download /tmp/alley.png
```
