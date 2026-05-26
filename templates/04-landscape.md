# Template: Landscape / Establishing Shot

## Genre / Use case
Wide environment shots, nature photography, establishing shots for film/narrative,
cityscapes, atmospheric environments, geographic hero shots.

## When to use
User asks for landscape, environment, establishing shot, nature, cityscape, vista,
geographic shot, "wide" or "scenic" anything.

## Recommended models
- **Photoreal landscape**: `flux-ultra`, `flux-pro` for max fidelity.
- **Painterly / concept**: `stability-sd3`, `stability-ultra`, `recraft`.
- **Cinematic establishing**: `flux-pro` with anamorphic style register.
- **Video timelapse**: `seedance` or local `Text to Video (Wan 2.2).json`.

## Example prompt — `flux-ultra` (epic landscape)

```
Model: flux-ultra (cloud)
Aspect: 16:9 | Style: Cinematic Photoreal

Extreme Wide Shot (EWS) Bird's Eye Crane Up of a vast frozen lake.
Surrounded by jagged obsidian mountains piercing low clouds.
Single hairline crack across the ice surface, snow scattered in patches.
A lone figure stands at lake center, tiny against scale — tactical jacket, head tilted up.
Lighting: Blue Hour. Soft diffused moonlight piercing heavy gray clouds.
Color: cold blue-gray dominant, single warm amber pinpoint from distant cabin window on shore.
Style: Anamorphic widescreen 2.39:1 letterboxed. Photoreal cinematic.
Heavy atmospheric haze. Crushed blacks. 4K resolution.

Run:
comfy generate flux-ultra --prompt "EWS bird's eye crane up of vast frozen lake surrounded by jagged obsidian mountains piercing low clouds, single hairline crack across ice surface with snow scattered in patches, lone figure stands at lake center tiny against scale wearing tactical jacket with head tilted up, blue hour soft diffused moonlight piercing heavy gray clouds, cold blue-gray dominant with single warm amber pinpoint from distant cabin window on shore, anamorphic widescreen letterboxed photoreal cinematic, heavy atmospheric haze, crushed blacks, 4K" --aspect_ratio 16:9 --download /tmp/landscape_{index}.{ext}
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "EWS Bird's Eye Crane Up" | Shot size + angle + camera move all named |
| "vast frozen lake surrounded by jagged obsidian mountains" | Subject + environment with material specificity |
| "piercing low clouds" | Active verb gives depth |
| "Single hairline crack across the ice" | One micro-detail anchors scale |
| "A lone figure stands at lake center, tiny against scale" | Human anchor for scale (powerful in EWS) |
| "Blue Hour" | Named lighting condition |
| "Soft diffused moonlight piercing heavy gray clouds" | Specific quality + direction |
| "cold blue-gray dominant, single warm amber pinpoint" | Dual-color grade beats "moody" |
| "Anamorphic widescreen 2.39:1 letterboxed" | Style register in Look line (not as aspect param) |
| "Heavy atmospheric haze" | Atmospheric layer cue |

## Negative constraints
- Composition: `no centered horizon line, no flat dead-zone foreground, no missing depth cue`
- Detail: `no over-rendered foliage, no painterly texture (unless illustration register requested)`
- Scale: `no missing scale reference if scale is the subject`

## Common mistakes
1. **No depth cue** — Foreground + midground + background should each have a distinct visual layer.
2. **Centered horizon** — Boring composition. Use rule-of-thirds (horizon at upper-third or lower-third).
3. **"Beautiful landscape"** — Style slop. Name geography, light, atmosphere.
4. **Missing human scale** — If grandeur is the point, add a tiny figure or known-scale object (lighthouse, cabin).

## Variations

### Painterly concept art — `stability-sd3`
```
Model: stability-sd3 (cloud)
Aspect: 16:9 | Style: Painted Concept Art

Vast windswept plain stretching to ochre mountains.
A caravan of robed travelers winds along a dirt road, leaving long shadows in late afternoon sun.
Sky dominates upper two-thirds — orange-to-violet gradient, scattered cumulus.
Style: Studio Ghibli painted matte, soft brushwork, slight grain.
Warm desaturated palette.
```

### Cityscape establishing — `flux-pro`
```
Model: flux-pro (cloud)
Aspect: 21:9 | Style: Cinematic Photoreal

Aerial wide of a coastal city at twilight.
Rows of skyscrapers descending toward an active harbor.
Container ships moored in foreground, distant bridges spanning bay.
Lighting: dusk magic hour. Sky deep blue-violet, city windows glowing amber.
Sparse atmospheric haze. Lens flares from sun-glints on water.
Style: Anamorphic widescreen letterboxed. Photoreal cinematic. 4K.
```

### Nature timelapse video — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 10s

A mountain valley at dawn, captured as accelerated time-lapse.
Mist flows through valley like a slow river, dissipating with rising sun.
Cloud shadows race across mountainsides.
Camera: locked off wide, no pan.
[0-3s] Pre-dawn blue.
[3-7s] Sun crests ridge — light spreads across valley floor.
[7-10s] Mist burns off, full daylight, sharp shadows.
Style: Photoreal nature documentary. Smooth time-acceleration. 4K.
```

### Multi-shot landscape pipeline
```bash
# 1. Establish wide
comfy generate flux-ultra --prompt "<EWS landscape>" --aspect_ratio 16:9 --download /tmp/wide.png

# 2. Push to specific feature
comfy generate flux-pro --prompt "same valley, now medium shot focused on lone cabin at edge of frozen lake, smoke from chimney, same blue hour lighting" --aspect_ratio 16:9 --download /tmp/medium.png

# 3. Animate establishing shot
comfy generate pika-i2v --image /tmp/wide.png --prompt "slow crane up over the landscape, mist drifting through valley, clouds moving slowly across sky" --duration 5 --async
```
