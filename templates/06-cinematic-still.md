# Template: Cinematic Still Image (Shot Framing Formula)

## Genre / Use case
Premium cinematic still images using the exact shot-framing formula. Hero frames for
posters, key art, magazine covers, film-look stills, narrative keyframes.

## When to use
User wants a "cinematic still", "film still", "hero frame", "key art", or describes
shot framing language (close-up, medium, wide, angle, lens).

## The Formula

```
[Shot size] + [Angle] + [Movement keyword if applicable] of [character/subject].
[Pose / micro-action]. [Environment]. [Lighting]. [Style register].
```

## Recommended models
- **Photoreal cinematic**: `flux-pro`, `flux-ultra`.
- **Concept art / illustration**: `stability-sd3`, `stability-ultra`, `recraft`.
- **Versatile / fast**: `nano-banana`.
- **Text-in-frame (posters)**: `ideogram`, `dalle`.

## Example prompts — formula applied

### Sci-Fi Character Tension — `flux-pro`
```
Model: flux-pro (cloud)
Aspect: 16:9 | Style: Cinematic

Medium Close-Up (MCU) Low Angle Dolly Zoom of a weathered space pilot in a cracked visor.
Staring intensely off-camera, jaw clenched.
The sparking, smoke-filled cockpit of a crashing starfighter.
Flashing red emergency lights, hard side-key illumination.
Photorealistic sci-fi cinematic. Ultra-sharp detail. Anamorphic widescreen.

Run:
comfy generate flux-pro --prompt "MCU low angle dolly zoom of weathered space pilot in cracked visor, staring intensely off-camera jaw clenched, sparking smoke-filled cockpit of crashing starfighter, flashing red emergency lights, hard side-key illumination, photoreal sci-fi cinematic, ultra-sharp detail, anamorphic widescreen letterboxed" --aspect_ratio 16:9 --download /tmp/pilot.png
```

### Epic Fantasy Scale — `stability-ultra`
```
Model: stability-ultra (cloud)
Aspect: 16:9 | Style: Concept Art

Extreme Wide Shot (EWS) Overhead Crane Up of a lone knight in blackened armor.
Kneeling in snow with a glowing broadsword planted in the ground.
A vast frozen lake surrounded by jagged obsidian mountains.
Cold blue hour. Soft diffused moonlight piercing heavy clouds.
Dark fantasy concept art. High contrast. 4K.

Run:
comfy generate stability-ultra --prompt "EWS overhead crane up of lone knight in blackened armor kneeling in snow with glowing broadsword planted in ground, vast frozen lake surrounded by jagged obsidian mountains, cold blue hour soft diffused moonlight piercing heavy clouds, dark fantasy concept art, high contrast, 4K" --aspect_ratio 16:9 --download /tmp/knight.png
```

### Psychological Thriller Detail — `nano-banana`
```
Model: nano-banana (cloud)
Aspect: 3:4 | Style: 1970s Thriller

Extreme Close-Up (ECU) Dutch Angle Rack Focus of a trembling hand clutching an ornate silver key.
Knuckles white from gripping too hard, skin textured and cold.
Dimly lit vintage hallway with peeling floral wallpaper, blurred background.
Sickly yellow-green practical light. Crushed shadows.
1970s psychological thriller. Heavy film grain. Muted palette.

Run:
comfy generate nano-banana --prompt "ECU dutch angle rack focus of trembling hand clutching ornate silver key, knuckles white skin textured and cold, dimly lit vintage hallway with peeling floral wallpaper blurred behind, sickly yellow-green practical light, crushed shadows, 1970s psychological thriller, heavy film grain, muted palette" --download /tmp/thriller.png
```

## Annotation — why the formula works

| Element | What it does |
|---------|--------------|
| **Shot size** (ECU/CU/MCU/MS/MLS/LS/WS/EWS) | Anchors composition. Model knows distance + frame ratio. |
| **Angle** (Low/High/Eye Level/Bird's Eye/Worm's Eye/Dutch) | Sets viewer's vertical relationship to subject. Power dynamics. |
| **Movement keyword** (Dolly Zoom, Crane Up, Rack Focus, etc.) | Even on a still, this informs composition energy and apparent depth. |
| **Character + clothing + state** | Identity grounded. "Weathered", "cracked visor", "blackened armor" = texture words model can render. |
| **Pose / micro-action** | "Jaw clenched", "kneeling", "trembling" — performance direction. |
| **Environment** | Specific location + atmosphere ("sparking smoke-filled cockpit", "vast frozen lake"). |
| **Lighting** | Direction + quality + color. "Hard side-key", "blue hour soft diffused". |
| **Style register** | Specific aesthetic — "photoreal sci-fi cinematic" beats "high quality". |

## Building your own — fill-in-blank

```
Model: <flux-pro / flux-ultra / nano-banana / stability-ultra>
Aspect: <16:9 / 3:4 / 1:1 / 9:16> | Style: <Cinematic / Concept Art / Editorial>

<Shot size> <Angle> <Movement keyword> of <character / subject>.
<Pose / micro-action>.
<Environment>.
<Lighting: direction + quality + color>.
<Style register>. <Texture/grain notes>. <Color grade>.
```

## Negative constraints to append

Universal artifact prevention (see `shared/negative-constraints.md` § Universal):
```
no warped hands, no extra fingers, no morphed faces, no plastic skin,
no overexposed highlights, no banding artifacts, no chromatic fringing,
no watermark, no logo overlay, no caption text
```

## Common mistakes

1. **Skip shot size** — Without ECU/CU/MS the model defaults to medium-wide. Always specify.
2. **Skip lighting** — Default lighting is flat. Always name direction + quality + color.
3. **Vague style** — "Cinematic" alone is weak. Pair with "anamorphic", "35mm grain", specific era ("1970s thriller").
4. **Over-described pose** — "Standing with one foot forward, head tilted at 22 degrees" = brittle. Use "kneeling", "jaw clenched", "hand outstretched".
5. **Mixing registers** — "Photoreal cinematic but also painted illustration" = neither. Pick one.

## Shot size + angle quick combos

| Goal | Shot + Angle |
|------|--------------|
| Hero introduction | MCU Low Angle |
| Vulnerability / threat | High Angle Wide or Worm's Eye Low |
| Intimate emotion | ECU Eye Level Rack Focus |
| Scale / awe | EWS Bird's Eye or Crane Up |
| Disorientation / tension | Dutch Angle MCU |
| Action energy | LS Low Angle (running figure) |
| Sci-fi grandeur | WS Worm's Eye |
| Romantic / soft | MCU Eye Level with shallow depth of field |
| Horror / unease | High Angle or Dutch with low-key lighting |
| Documentary realism | MS Eye Level Handheld |

## Multi-frame storyboard pattern

For a 5-shot sequence telling a micro-story:

```bash
# Shot 1: Establishing
comfy generate flux-pro --prompt "EWS bird's eye of <location>, <lighting>, anamorphic cinematic" --aspect_ratio 16:9 --download /tmp/01_establish.png

# Shot 2: Character intro
comfy generate flux-pro --prompt "MCU low angle of <character>, <pose>, <same lighting register>, anamorphic cinematic" --aspect_ratio 16:9 --download /tmp/02_intro.png

# Shot 3: Detail insert
comfy generate nano-banana --prompt "ECU rack focus of <object the character holds/looks at>, <same color grade>, anamorphic cinematic" --aspect_ratio 16:9 --download /tmp/03_detail.png

# Shot 4: Action
comfy generate flux-pro --prompt "MS dutch angle of <character mid-action>, <motion blur cue>, <same lighting>, anamorphic cinematic" --aspect_ratio 16:9 --download /tmp/04_action.png

# Shot 5: Resolution / final beat
comfy generate flux-pro --prompt "WS eye level of <character + environment>, <emotional register>, anamorphic cinematic" --aspect_ratio 16:9 --download /tmp/05_resolution.png
```
