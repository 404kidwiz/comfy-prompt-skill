# Template: Sci-Fi / VFX / Cyberpunk

## Genre / Use case
Sci-fi imagery — cyberpunk, space, futurism, VFX-heavy concepts, mecha, post-apocalyptic,
holographic interfaces, transformation effects.

## When to use
User asks for sci-fi, cyberpunk, space, futuristic, VFX, mecha, holograms, dystopian,
robot, AI character, neon-noir.

## Recommended models
- **Photoreal sci-fi still**: `flux-pro`, `flux-ultra`, `stability-ultra`.
- **Concept / painterly**: `stability-sd3`, `recraft`.
- **VFX-heavy video**: `seedance` (motion physics), `grok-video`, local `Text to Video (Wan 2.2).json`.
- **Image-to-video transformation**: `pika-i2v` for animation, `seedance` for complex motion.

## Example prompt — `flux-pro` (cyberpunk still)

```
Model: flux-pro (cloud)
Aspect: 21:9 | Style: Photoreal Cyberpunk

Wide Shot Low Angle of a rain-soaked Tokyo back alley at 2am.
A figure in a translucent rain poncho stands beneath a flickering neon sign reading "電気".
Their face half-lit by holographic ad displays cycling overhead — pink, cyan, violet.
Background: layered fire escapes, hanging laundry, distant skyscraper silhouettes.
Foreground: rain-slick pavement reflecting neon, steam rising from sewer grates.
Lighting: dominant neon practicals — cyan rim from rear sign, magenta key from above hologram.
Style: Anamorphic widescreen 2.39:1. Photoreal cyberpunk. Blade Runner influence.
Heavy atmospheric haze. Crushed blacks. Lens flares from neon. Slight chromatic aberration.

Run:
comfy generate flux-pro --prompt "wide shot low angle of rain-soaked Tokyo back alley at 2am, figure in translucent rain poncho beneath flickering neon sign reading '電気', face half-lit by holographic ads cycling pink cyan violet overhead, layered fire escapes and hanging laundry behind, distant skyscraper silhouettes, rain-slick pavement reflecting neon, steam rising from sewer grates, dominant neon practicals cyan rim from rear sign magenta key from above hologram, anamorphic widescreen photoreal cyberpunk Blade Runner influence, heavy atmospheric haze, crushed blacks, lens flares from neon, slight chromatic aberration" --aspect_ratio 21:9 --download /tmp/cyber_{index}.{ext}
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "rain-soaked Tokyo back alley at 2am" | Geography + time anchor for cyberpunk register |
| "translucent rain poncho" | Specific material that interacts with light |
| "neon sign reading '電気'" | Real text glyph (use ideogram for cleaner text) |
| "holographic ad displays cycling overhead — pink, cyan, violet" | Specific color cycle + visible light source |
| "layered fire escapes, hanging laundry" | Vertical depth detail |
| "rain-slick pavement reflecting neon, steam rising from sewer grates" | Reflection + atmospheric motion |
| "dominant neon practicals — cyan rim from rear, magenta key from above" | Specific lighting from named source positions |
| "Blade Runner influence" | Reference shorthand for visual register |
| "Slight chromatic aberration" | Lens artifact register cue |

## Negative constraints
Pull universal + specific:
```
no plastic CGI sheen, no over-rendered hard surfaces, no Pixar-style smoothness,
no incoherent perspective, no impossible scale on background objects,
no warped reflections
```

For human/character in scene: pull `Face / Identity` constraints.

## Common mistakes
1. **Too many futuristic elements** — Hologram + robot + neon + flying car + cyberpunk graffiti = visual overload. Pick 2-3 anchors.
2. **Generic neon** — "Neon city" is meaningless. Name colors, name sign content, name light direction.
3. **No human anchor** — Pure environment shots feel empty. Add a figure for scale + emotional register.
4. **VFX described abstractly** — "Energy blast" or "magical effect" → fix with "blue-white arc lightning crackling between fingers, sparks dripping downward".

## Variations

### Mecha / robot — `stability-ultra`
```
Model: stability-ultra (cloud)
Aspect: 16:9 | Style: Photoreal Sci-Fi

Medium Wide of a 12-meter humanoid mecha standing in scorched desert.
Plating: brushed titanium with weathered black panels, exposed hydraulic joints, glowing cyan visor.
Mid-stride, dust kicked up around feet, smoke trailing from rear thrusters.
Background: distant ruined city silhouette, dawn sky.
Lighting: hard side-key from rising sun, deep contact shadows.
Style: Photoreal sci-fi. Industrial weight. Photographic realism — not anime.
```

### Hologram interface — `nano-banana`
```
Model: nano-banana (cloud)
Aspect: 16:9 | Style: Cyberpunk Tech

Over-the-shoulder of a hacker in a dark room facing translucent holographic UI panels.
Panels: cyan and amber data streams, 3D city map rotating, biometric scan readout.
Light from holograms reflects off her face and onto desk surface.
Style: Photoreal cyberpunk. Practical hologram light dominant. Cool color grade.
```

### Transformation video — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 8s

A man stands in a sterile white lab. Blue energy begins crackling around his hands.
[0-2s] Static MCU. He raises his palms, looking down at them. Energy intensifies.
[2-5s] Camera slow dolly in. Blue arc lightning visible between fingers, body outlined in faint glow.
[5-8s] Sudden flash. Camera holds. He stands transformed — armor plating, glowing chest core.
Style: Photoreal VFX. Cinema-grade lighting. Sharp transformation moment.
```

### Image-to-video sci-fi sequence
```bash
# 1. Cyberpunk hero still
comfy generate flux-ultra --prompt "<cyberpunk alley description>" --aspect_ratio 21:9 --download /tmp/cyber.png

# 2. Animate atmosphere
comfy generate pika-i2v --image /tmp/cyber.png --prompt "rain falls steadily, neon signs flicker, steam rises continuously, figure remains still, camera holds locked off" --duration 5 --async

# 3. Resume and download
comfy generate resume pika-i2v <job_id> --download /tmp/cyber.mp4
```
