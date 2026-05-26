# Template: Cinematic Action / Chase

## Genre / Use case
High-energy pursuit, foot chases, vehicle chases, rooftop escapes, parkour. Primary
energy: someone moving fast through a space with stakes.

## When to use
User asks for chase, pursuit, escape, running, parkour, action scene.

## Recommended models
- **Video**: `seedance` (cloud, audio-capable, 10s) for character chases. `grok-video`
  for stylized action. Local: `Text to Video (Wan 2.2).json` for full control.
- **Still keyframe**: `flux-pro` for hero frame, `nano-banana` for fast iteration.

## Example prompt — `seedance`

```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls and startled vendors. Steam rises from food carts.
Neon signs fracture in every puddle.
Camera: Action Run — low behind her, matching pace.
A metal gate drops ahead. She slides under it without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast. 16:9.

Run:
comfy generate seedance --prompt "woman in tactical jacket sprints through rain-soaked night market, weaving between stalls and startled vendors, steam rising from food carts, neon signs fracturing in every puddle, action run camera low behind her matching pace, metal gate drops ahead she slides under it without breaking stride, cinematic cold blue shadows warm amber market light high contrast" --duration 10 --aspect_ratio 16:9 --async
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "tactical jacket" | Specific clothing grounds character — not "a woman running" |
| "rain-soaked night market" | Wet surfaces + neon = visual complexity model renders well |
| "weaving between stalls and startled vendors" | Active verbs give motion direction |
| "Steam rises from food carts" | Atmospheric motion fills dead space |
| "Neon signs fracture in every puddle" | Reflection cue — models respond to it |
| "Camera: Action Run" | Named preset from `vocab.md` |
| "low behind her, matching pace" | Clarifies camera-subject spatial relationship |
| "A metal gate drops. She slides under it" | One obstacle + one response = clean beat |
| "Cold blue shadows, warm amber market light" | Dual-color grade beats generic "cinematic" |

## Negative constraints to append
- Motion overload: limit to 1 primary action + 1 secondary. Don't chain chase + fight + explosion in one clip.
- Camera switches: ONE camera per clip. Don't combine Action Run + Bullet Time in a single gen.
- Identity drift: video models can morph faces over 10s clips. Add: `keep face consistent across the clip`.

## Common mistakes
1. **Too many camera switches** — "Action Run then Whip Pan then Bullet Time" = visual soup. One camera per clip.
2. **Generic language** — "camera follows dramatically" does nothing. Name exact preset.
3. **Vague subject** — "a person running" → fix with clothing, gear, demeanor.

## Variations
- **Handheld grittier**: Camera → Handheld. Add "shaky documentary urgency" to Look.
- **Vehicle chase**: Use `seedance` or `grok-video`. Describe vehicles + road specifics.
- **Vertical / social format**: Aspect 9:16. Camera → Action Run, note "close framing, face visible".
- **Sci-fi corridor chase**: Add zero-gravity or corridor environment. Camera → FPV Drone.

## Multi-shot chain (image → video)
```bash
# 1. Hero keyframe
comfy generate flux-pro --prompt "woman in tactical jacket mid-stride, rain-soaked market" --aspect_ratio 16:9 --download /tmp/hero.png

# 2. Animate from keyframe
comfy generate seedance --image /tmp/hero.png --prompt "she continues sprinting, slides under closing metal gate, camera tracks low behind" --duration 8 --async
```
