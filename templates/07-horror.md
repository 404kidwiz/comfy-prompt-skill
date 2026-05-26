# Template: Horror / Dread Atmosphere

## Genre / Use case
Horror, dread, psychological unease, body horror, jump scares, supernatural,
cosmic horror, found-footage register.

## When to use
User asks for horror, scary, creepy, dread, eerie, unsettling, ghost, monster,
slasher, body horror, possession.

## Recommended models
- **Atmospheric still**: `flux-pro`, `nano-banana` (great at unsettling detail).
- **Body horror / surreal**: `stability-sd3` (wide style range), `recraft`.
- **Found-footage video**: `seedance` with handheld camera + low-light.
- **Slow dread video**: `pika-i2v` from a still keyframe.

## Example prompt — `flux-pro` (atmospheric still)

```
Model: flux-pro (cloud)
Aspect: 3:4 | Style: Psychological Horror

Medium Long Shot (MLS) Eye Level Static of a figure standing at the end of a dark hallway.
Just visible — face obscured by shadow, body still, hands at sides.
Wallpaper peeling, single bare bulb swaying overhead casting long pendulum shadows.
Floor warped, doorframe slightly askew.
Lighting: single sickly yellow practical light from the bulb. Hard chiaroscuro. Floor lost to black.
Style: 1970s grindhouse psychological horror. Heavy 16mm film grain. Crushed blacks.
Desaturated sickly palette — yellow-greens and cold browns.

Run:
comfy generate flux-pro --prompt "MLS eye level static of figure standing at end of dark hallway face obscured by shadow body still hands at sides, peeling wallpaper, single bare bulb swaying overhead casting long pendulum shadows, floor warped doorframe slightly askew, single sickly yellow practical light from bulb hard chiaroscuro floor lost to black, 1970s grindhouse psychological horror, heavy 16mm film grain, crushed blacks, desaturated sickly yellow-green and cold brown palette" --aspect_ratio 3:4 --download /tmp/horror.png
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "figure standing at end of dark hallway" | Negative space + distance = dread |
| "face obscured by shadow, body still, hands at sides" | Frozen, ambiguous posture |
| "wallpaper peeling, doorframe slightly askew" | Reality slightly wrong = uncanny register |
| "single bare bulb swaying overhead casting long pendulum shadows" | Motion implied + chiaroscuro source |
| "sickly yellow practical light. Hard chiaroscuro. Floor lost to black" | Specific horror lighting palette |
| "1970s grindhouse" | Era register + film stock cue |
| "Desaturated sickly yellow-greens and cold browns" | Disease-adjacent color palette |

## Negative constraints
Pull universal + horror-specific:
```
no overly gory imagery (unless explicitly requested), no cartoonish monsters,
no jump-scare composition (subject dead-center in frame), no over-lit faces,
no clean digital sheen
```

## Common mistakes
1. **Subject dead-center** — Horror lives in negative space + corners. Off-center, partially hidden.
2. **Over-described monster** — Implication > explicit. "Face obscured by shadow" > "monster face with claws".
3. **Bright clean lighting** — Horror = low-key, single source, hard shadows.
4. **Modern HD digital look** — Vintage film stocks (16mm, VHS, Super 8) sell horror.
5. **Generic "scary"** — Name the specific register: psychological, slasher, cosmic, body, found-footage.

## Variations

### Body horror — `stability-sd3`
```
Model: stability-sd3 (cloud)
Aspect: 1:1 | Style: Body Horror Surreal

Extreme Close-Up (ECU) Macro Rack Focus of human fingers slowly elongating,
joints rotating in impossible directions, skin stretching translucent.
Background: blurred medical-tile bathroom.
Lighting: harsh cold-white fluorescent from above, deep contact shadows.
Style: David Cronenberg body horror. Photoreal. Wet textural detail.
Muted clinical palette — pale skin, sterile white, hint of pink.
```

### Found-footage video — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 10s

Handheld POV walking down a flickering apartment hallway at 3am.
Camera: shaky handheld, slight forward push, occasional jerks.
[0-4s] Empty hallway. Light at end flickers.
[4-7s] Camera turns left into open doorway — empty bedroom, sheet on floor.
[7-10s] Camera whips back to hallway. A figure now stands where there was nothing.
Style: Found-footage. Heavy noise. Low-res digital camcorder. Timestamp overlay.
No music, only breathing audio.
```

### Cosmic horror — `nano-banana`
```
Model: nano-banana (cloud)
Aspect: 16:9 | Style: Cosmic Horror

WS Low Angle of a lighthouse on a black-rock cliff at midnight.
A sky of impossible geometry above — twisted constellations, fractal aurora, distant tentacle silhouettes against starlight.
Sea below mirror-still and obsidian black.
Lighting: green-cyan aurora glow, single warm beacon from lighthouse.
Style: Lovecraftian cosmic horror. Painted matte. Heavy atmospheric haze.
```

### Slasher — `flux-pro`
```
Model: flux-pro (cloud)
Aspect: 16:9 | Style: 1980s Slasher

LS Static of an empty suburban street at night. Yellow streetlight pools.
A figure stands in deep shadow between two pools of light, holding a long object — unclear what.
Trees rustle. One distant window glows.
Style: 1980s slasher cinematography. 35mm film grain. High contrast.
Reagan-era suburban Americana corrupted.
```

## Multi-shot horror sequence
```bash
# Beat 1: Establishing — calm before
comfy generate flux-pro --prompt "WS suburban street, golden hour, kids on bikes, normal" --download /tmp/h1_calm.png

# Beat 2: Wrong
comfy generate flux-pro --prompt "same WS suburban street, now twilight, kids gone, single shoe in road, one streetlight flickering" --download /tmp/h2_wrong.png

# Beat 3: Threat appears
comfy generate flux-pro --prompt "same WS suburban street, now full night, figure standing in deep shadow between streetlights, posture wrong" --download /tmp/h3_threat.png

# Beat 4: Reveal
comfy generate flux-pro --prompt "MCU low angle close-up matching previous figure, face still hidden by shadow but mask visible" --aspect_ratio 3:4 --download /tmp/h4_reveal.png

# Animate the threat beat
comfy generate pika-i2v --image /tmp/h3_threat.png --prompt "figure does not move, streetlight flickers, leaves drift past, camera holds locked off, slow zoom in over 5 seconds" --duration 5 --async
```
