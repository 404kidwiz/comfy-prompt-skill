# Vertical: Before-After — Transformation Reveals

Adapted from Roman Knox `seedance-before-after` skill for Comfy.

## When to use
Transformation reveals, glow-ups, makeovers, renovation reveals, fitness transformations,
design before-after, business growth, results videos, progress visuals.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Video transformation (8s, audio) | `seedance` | Cloud, async |
| Static before/after pair (then composite) | `flux-pro` × 2 | Cloud, sync |
| Image-to-image transformation | `flux-kontext`, `nano-banana` | Cloud, sync |
| Local image edit batch | `Image Edit (Flux.2 Klein 4B).json` | Local |

---

## The Contrast Arc

Before-after content wins on the DELTA. The transformation must be:

| Axis | Before | After |
|------|--------|-------|
| Lighting | Flat, harsh, fluorescent | Warm, soft, directional |
| Color | Desaturated, gray | Saturated, warm |
| Composition | Chaotic, cluttered | Clean, ordered |
| Energy | Static or jittery | Smooth, deliberate |
| Sound | Discordant ambient | Clean musical resolution |

The bigger the contrast, the higher the retention. Pick at least 3 of the 5 axes
to flip dramatically.

---

## Hook Structures

### Split-Screen Wipe
```
Frame divided vertically. Left shows "before" state for 0.8s. Hard vertical wipe
sweeps left-to-right. Right reveals "after." Whoosh + impact sound on wipe.
Contrast must be dramatic — ugly→beautiful, chaos→order, empty→full.
```

### Sequential Cut
```
Before state holds 2-3s with discordant ambient. Hard cut to after state with
music drop + bass hit synced. Same camera angle in both shots — only the content
changes. Audience reads the difference immediately.
```

### Time-Lapse Flow
```
Single sustained shot showing the transformation in accelerated time. Lighting
shifts, elements move, color saturates. Camera locked off. Sound: time-passing
ambient (clock ticks, music swelling, environmental cues).
```

### Match-Cut Transform
```
Last frame of "before" shot composition-matched to first frame of "after." Same
object position, same framing, same camera angle — but content transformed. Cut is
seamless, the change reveals itself. Sound: single bass swell across the cut.
```

---

## Transition Techniques

| Transition | Use |
|-----------|-----|
| Hard vertical wipe | Maximum contrast, social-media-native |
| Cross-fade | Soft / dreamy transformation |
| Match-cut | Cinematic, premium |
| Whip-pan transition | Energetic, kinetic, fitness/lifestyle |
| Black-frame blink | Dramatic / shock reveal |
| Light-flash transition | Bright burst between shots, then reveal |

---

## Visual Contrast Strategies

### Cold → Warm
Before: cool fluorescent, blue-green tint, harsh top-down light. After: warm window
light, golden-hour amber, soft directional.

### Cluttered → Clean
Before: handheld jittery camera, things in foreground/midground/background, chaos.
After: locked off, single subject, vast negative space.

### Dim → Bright
Before: under-exposed, shadows dominate. After: properly lit, hero subject in light.

### Desaturated → Saturated
Before: muted gray-green palette. After: rich color reveal, brand colors present.

### Documentary → Cinematic
Before: handheld micro-jitter, flat lighting. After: Steadicam smooth, dramatic
lighting, shallow DOF.

---

## Camera Techniques for Reveals

| Move | Use |
|------|-----|
| Locked Off Both | Camera identical in before and after. Content does the work. |
| Pull-Back Reveal | Tight detail → wide context. After shot expands to show transformation scale. |
| Slow Push-In | Camera pushes through the wipe, intimacy with transformed state. |
| Match-Angle | Same exact camera angle in both shots. Reveals contrast cleanly. |

---

## Sound Design: Contrast Audio

Most important rule: AUDIO TRANSFORMATION mirrors VISUAL TRANSFORMATION.

| Before audio | After audio |
|--------------|-------------|
| Discordant ambient (buzzing fluorescent, keyboard chaos) | Clean music, soft beat |
| Silence / room tone | Music drop with bass hit |
| Fast / cluttered sounds | Sustained, breathing |

```
Sound: 0-1.5s chaotic ambient — buzzing fluorescent, keyboard clacking, phone
notification chaos. 1.5-2s whoosh + deep impact hit. 2-6s clean minimal beat,
satisfying, resolution-feeling. Low BPM, warm tones. The audio transformation
IS the message.
```

---

## Worked Example — Workspace Transformation (6s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 6s | Style: Cold→Warm Workspace

BEFORE [0-1.5s]:
Split composition — frame divided vertically. Left side shows chaotic, messy, ugly
state: cluttered desk, tangled wires, dim fluorescent lighting, gray color palette.
Right side is black/hidden.

Camera slowly reveals left-side chaos. Handheld micro-jitter for documentary
realism. Flat, unflattering lighting. Sound: discordant ambient — buzzing
fluorescent, keyboard clacking, phone notification chaos.

WIPE [1.5-2s]:
Hard vertical wipe transition sweeps left-to-right across frame. Sound: dramatic
whoosh + deep impact hit. Screen shake on impact.

AFTER [2-4s]:
Right side reveals the transformation — same space but organized, minimal,
beautiful. Warm golden-hour lighting from window. Clean surfaces, cable-managed
desk, plant accents. Color palette shifts to warm amber and cream. Camera movement
becomes smooth Steadicam — contrasting earlier handheld jitter.

PAYOFF [4-6s]:
Camera pushes in to hero detail — the centerpiece of transformed space. Single
object in perfect light. Shallow DOF, bokeh background. Sound transitions to clean
ambient: soft music, no clutter. Audio transformation mirrors visual.

Sound: 0-1.5s chaotic ambient. 1.5-2s whoosh + impact. 2-6s clean minimal beat,
satisfying, resolution-feeling. Low BPM, warm tones.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 6 --async
```

---

## Worked Example — Photo Before-After (Static Pair → Composite)

```bash
# Generate matched before-after using flux-kontext for identity locking

# 1. Generate BEFORE state
comfy generate flux-pro \
  --prompt "MS of cluttered home office, dim fluorescent overhead light, papers everywhere on desk, tangled cables, dirty coffee cup, gray walls, documentary handheld feel, flat unflattering light" \
  --aspect_ratio 1:1 \
  --download /tmp/before.png

# 2. Transform same space using kontext (identity-locked)
comfy generate flux-kontext \
  --image /tmp/before.png \
  --prompt "transform this exact same space: now organized minimal aesthetic, warm golden-hour window light from camera-left, clean desk with single laptop and plant, cable-managed, warm amber and cream palette, polished hardwood floor, shallow depth of field background bokeh, cinematic" \
  --download /tmp/after.png

# 3. Composite into split-screen via ImageMagick (or video editor)
magick montage /tmp/before.png /tmp/after.png -tile 2x1 -geometry +0+0 /tmp/split.png
```

---

## Worked Example — Renovation Reveal (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Architectural Reveal

[0-2s] BEFORE:
WS of empty derelict room. Walls peeling, harsh single bare bulb light, exposed
wires, dust suspended in air. Camera slow handheld drift. Sound: dripping water,
distant traffic, eerie ambient hum.

[2-2.5s] TRANSITION:
Light-flash transition — bright white burst for 0.3s. Sound: hard whoosh + impact +
crystal chime layer.

[2.5-6s] AFTER:
Same WS angle but room fully renovated — warm wood floors, hanging pendant lights,
modern furniture, large windows with natural daylight. Camera Steadicam smooth
push-in. Color grade: warm amber + soft cream. Sound: clean ambient pad with
soft music entering.

[6-8s] PAYOFF:
Camera pushes through window to view outside the building — establishing exterior.
Music resolves. Final frame holds 1s. Sound: music plateau then resolution chord.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Identity locks for before-after
- DELTA must be dramatic. Pick 3+ axes to flip (lighting, color, composition, energy, sound).
- Audio transformation mirrors visual. Sound matters as much as image.
- Same camera angle when possible — content does the work, not camera tricks.
- The TRANSITION is the moment of impact. Don't bury it in 5s of buildup.
- After state should feel like answered tension, not just "different."
- Last frame holds 1+ seconds — let the new state land.
