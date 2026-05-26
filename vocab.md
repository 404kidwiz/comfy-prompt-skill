# Comfy Prompt Vocabulary

Cinematic vocabulary for Comfy prompts. Adapted from filmmaking + cinematography.
Use these EXACT terms — generic phrasing ("camera moves dramatically") gets ignored
by every model.

---

## Camera Movement

### Linear movement
- **Dolly In / Out** — smooth track toward/away from subject
- **Dolly Left / Right** — smooth lateral track
- **Dolly Zoom (Vertigo)** — simultaneous dolly + counter-zoom
- **Super Dolly In / Out** — exaggerated fast version
- **Truck** — lateral dolly synonym
- **Push-In** — slow dolly in, emotional intensification
- **Pull-Back** — slow dolly out, scale reveal

### Vertical
- **Crane Up / Down** — vertical rise or descent
- **Crane Over** — directly overhead
- **Levitation** — dreamlike float upward
- **Tilt Up / Down** — rotate on horizontal axis (no physical movement)
- **Pedestal Up / Down** — physical vertical move with locked tilt

### Orbit / Arc
- **360 Orbit** — complete circle around subject
- **Arc** — semi-circular sweep
- **Lazy Susan** — slow turntable rotation
- **Robo Arm** — precision mechanical arc path
- **Half-Orbit** — 180° sweep

### Zoom
- **Crash Zoom In / Out** — rapid sudden zoom (handheld feel)
- **Rack Focus** — refocus between near and far
- **Slow Zoom** — gradual focal-length change
- **Whip Zoom** — instant snap zoom

### Follow / Immersive
- **Action Run** — low follow behind running subject
- **FPV Drone** — fast agile aerial weaving
- **Handheld** — organic shaky realistic
- **Steadicam** — smooth flowing follow
- **Snorricam** — mounted on actor, background sways
- **Head Tracking** — locked to character's head
- **POV / First Person** — camera IS the character's eyes

### Cinematic techniques
- **Bullet Time** — slow-motion sweep around frozen subject
- **Dutch Angle / Canted** — tilted diagonal composition
- **Fisheye** — wide distortion lens
- **Whip Pan** — fast blur pan
- **Overhead / Bird's Eye** — direct top-down
- **Worm's Eye** — extreme low looking up
- **Flying** — free-floating aerial glide
- **Hyperlapse** — moving camera + time-lapse

### Time-based
- **Timelapse** — fixed camera, fast-forward time
- **Slow Motion** — sub-real-time playback
- **Speed Ramp** — variable speed across single shot
- **Freeze Frame** — single-frame hold

---

## Camera Angles

- **Low Angle** — camera looks up (power, dominance)
- **High Angle** — camera looks down (vulnerability)
- **Eye Level** — neutral, conversational
- **Bird's-Eye View** — directly overhead
- **Worm's-Eye View** — extreme low looking straight up
- **Ground Level** — camera on ground surface
- **Canted Angle / Dutch Tilt** — tilted horizon for unease
- **Over-the-Shoulder (OTS)** — shot-reverse-shot framing
- **POV / First Person** — character's eyes
- **Hip Level** — between ground and eye, neutral handheld
- **Static Oblique** — off-axis angled perspective

---

## Shot Sizes

- **ECU (Extreme Close-Up)** — fragment of face / object detail
- **CU (Close-Up)** — full face, shoulders to top of head
- **MCU (Medium Close-Up)** — chest up
- **MS (Medium Shot)** — waist up
- **MLS (Medium Long Shot)** — knees up (American shot)
- **LS (Long Shot)** — full body, some environment
- **WS (Wide Shot)** — character + significant environment
- **EWS (Extreme Wide Shot)** — character tiny in vast environment
- **Two-Shot** — two characters framed together
- **Insert** — sub-second cut to detail (always name the subject)

---

## Lens / Optical Vocabulary

- **Anamorphic** — 2.39:1 widescreen, horizontal flares, oval bokeh
- **Wide Lens (14-24mm)** — exaggerated depth, distortion at edges
- **Standard (35-50mm)** — close to human eye
- **Telephoto (85-200mm)** — compressed depth, shallow focus
- **Macro** — extreme close-focus detail
- **Tilt-Shift** — miniature effect, selective focus plane
- **Bokeh** — out-of-focus background blur
- **Lens Flare** — light bleeding through lens
- **Chromatic Aberration** — color fringing at edges
- **Shallow Depth of Field** — narrow plane of focus
- **Deep Focus** — everything sharp

---

## Lighting

### Direction
- **Key Light** — primary directional light
- **Fill Light** — softens shadows from key
- **Rim Light / Back Light** — separates subject from background
- **Side Key** — dramatic single-side illumination
- **Top Light** — overhead, eye sockets shadowed
- **Under Light** — from below, horror register
- **Practical Light** — visible source in frame (lamp, neon, candle)

### Quality
- **Hard Light** — sharp shadows, high contrast
- **Soft Light** — diffused, no harsh shadows
- **Diffused** — softened through scrim/cloud
- **Specular** — glossy reflective highlights

### Time-of-day
- **Golden Hour** — warm sunset/sunrise, low angle
- **Blue Hour** — twilight, cool ambient
- **Magic Hour** — narrow window post-sunset
- **Midday** — harsh overhead
- **Overcast** — soft natural diffusion
- **Night** — practical sources dominant

### Mood
- **Chiaroscuro** — extreme light/dark contrast
- **Noir** — single key, deep shadows
- **High Key** — bright even, minimal shadows
- **Low Key** — predominantly dark, single sources
- **Volumetric** — light shafts through atmosphere

---

## Color / Grade

- **Cinematic Color Grade** — teal-and-orange or muted naturalistic
- **Warm Palette** — amber, gold, red
- **Cool Palette** — blue, cyan, green
- **Desaturated** — muted color, near-monochrome
- **Saturated** — vivid, pushed colors
- **Cross-Processed** — vintage color shift
- **Bleach Bypass** — high contrast, low saturation
- **Crushed Blacks** — deep no-detail shadows
- **Lifted Blacks** — gray-shifted shadows (faded film)
- **Split Tone** — warm highlights + cool shadows

---

## Motion Physics Anchors

Anchor speed to physical analogy:

- `like dust suspended in honey` — extremely slow, viscous
- `like embers floating in still air` — slow, weightless
- `like smoke through a cathedral at dawn` — slow, layered
- `like a lake disturbed by a single drop` — slow ripple
- `like a flag in a steady cross-breeze` — moderate, periodic
- `like a slammed door rebounding` — fast, decaying
- `at the pace of a clock's hour hand` — barely perceptible
- `at the speed of light bending through water` — fluid, refractive

---

## 4-Layer Motion Hierarchy

Every video prompt specifies each layer separately:

1. **Subject motion** — what the character/object does
2. **Internal motion** — micro-motion within the subject (breath, hair, fabric, eye)
3. **Camera motion** — what the camera does
4. **Environmental motion** — what the world does (rain, leaves, light shifting)

Specifying each prevents the multi-motion-overload failure.

---

## Camera Contract

State camera behavior as an explicit rule BEFORE describing subject. Examples:

- `Static locked-off camera. Zero movement. No pan, no zoom, no dolly, no shake.`
  → atmospheric / observational / product reveals
- `Slow push-in only — 10% scale change over the full duration.`
  → quiet emotional intensification
- `Single handheld drift, slight organic sway, no cuts.`
  → documentary register, intimate scenes

Pair every camera contract with **negative reinforcement** — name the excluded
moves in the negative prompt.

---

## Composition

- **Rule of Thirds** — subject on 1/3 line intersection
- **Center Framing** — subject dead-center (formal, symmetric)
- **Negative Space** — empty area around subject
- **Leading Lines** — diagonals/curves drawing eye to subject
- **Symmetry** — mirrored composition
- **Foreground / Mid / Background** — explicit three-plane separation
- **Frame Within Frame** — doorway/window/arch around subject
- **Headroom** — space above subject's head
- **Lookroom / Noseroom** — space in direction subject faces
- **Depth Cue** — overlapping objects implying 3D space

---

## Texture / Surface

- **Photoreal** — modern digital cinema look
- **Film Grain** — analog grain texture
- **35mm / 16mm Film** — specific grain register
- **Super 8** — heavy grain, low resolution, color shift
- **VHS** — interlaced, color bleed, tracking artifacts
- **Polaroid** — vintage instant film look
- **Wet Plate** — Civil War-era photo register
- **Etching / Engraving** — line-art texture
- **Watercolor / Gouache** — painterly soft edges
- **Concept Art** — illustrative, painterly digital
- **3D Rendered** — CGI/Pixar look
- **Anime / Manga** — 2D animation register
- **Photoreal Sci-Fi** — physically grounded futuristic
- **Cinematic Realism** — film-quality real

---

## Aspect ratio (output spec) vs. style register

`16:9`, `9:16`, `1:1`, `4:5`, `3:4` → output aspect ratio (model parameter)
`Anamorphic`, `2.35:1`, `2.39:1`, `Cinemascope`, `Letterboxed` → style register
(use in Look line; render at 16:9 with letterboxing implied)

Do NOT pass `2.35:1` as a model parameter — most Comfy Cloud models don't accept it.
