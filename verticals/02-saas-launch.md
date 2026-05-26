# Vertical: SaaS Launch — Software Demos That Look Like Apple Keynotes

Adapted from Roman Knox `seedance-saas-launch` skill for Comfy.

## When to use
SaaS, app, software, product launch, demo, feature showcase, startup, tech reveal,
UI/dashboard/landing page video.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Hero product launch (10-12s, audio, UI cinematography) | `seedance` | Cloud, async |
| UI feature demo (5-8s, image-to-video) | `pika-i2v`, `runway-i2v` | Cloud, async |
| Hero UI screenshot (still) | `flux-ultra`, `flux-pro`, `dalle` | Cloud, sync |
| Dashboard mockup with text | `ideogram` (text fidelity), `dalle` | Cloud, sync |
| Local iteration | `Image to Video (Wan 2.2).json` | Local |

## The SaaS Video Problem

Most SaaS videos look like one of two failures:
1. **Boring screen recording** — UI walkthrough with cursor, zero cinema
2. **Generic mocks** — stock office b-roll, person typing on laptop, no product visible

The fix: treat the UI as a HERO subject. Lights, camera, cinematography — applied to
software the same way an Apple ad treats hardware.

---

## UI Cinematography Vocabulary

| Technique | Phrasing |
|-----------|----------|
| Pixel-perfect macro | "ECU of UI element with f/1.4 equivalent shallow DOF. Micro-shadow under button, glass-morphism reflection. Subpixel anti-aliasing visible." |
| Glass-morphism reveal | "UI element materializes from frosted glass blur — sharpens over 1s as camera pushes in. Glow behind element, subtle inner shadow." |
| Data cascade | "Charts animate upward, numbers count up, status indicators turn green one by one. Each element timed to subtle UI sound." |
| Cursor as character | "Cursor moves with intention — slows before clicks, hovers with hesitation, accelerates between targets. Treat it as actor." |
| Through-screen transition | "Camera pushes through monitor surface — UI fills frame, then emerges inside the product environment. Glassy bend distortion at transition." |
| Device hero | "Laptop / phone floats in 3-point lit workspace. Screen content alive. Surface props (plant, coffee, notebook) in shallow bokeh." |

---

## Lighting for Software

| Setup | Use case |
|-------|---------|
| **Studio Hero** | Three-point on device: warm key 45° left, soft fill right, brand-color rim behind. Workspace warm ambient. |
| **Dark Mode Glow** | Black/deep gray environment. Single brand-color glow behind device. Screen content provides the key light. |
| **Editorial White** | Pure white seamless background. Even softbox overhead. Device floats with subtle contact shadow only. |
| **Dual Glow** | Two opposing brand colors as rim lights — cool blue from one side, warm orange other. Screen white catches both. |

---

## Sound Design for SaaS

Layer the SaaS stack:

1. **UI sound layer** — click, hover, confirmation, notification synced to visual beats
2. **Music layer** — minimal electronic, 100-110 BPM, bass-forward, confident
3. **Whoosh/transition layer** — synced to camera moves and feature reveals
4. **Voiceover (optional)** — confident founder voice for hero shots only

Avoid: corporate stock music, generic upbeat ukulele, anything trendy-acoustic.

---

## Worked Example — Product Launch Hero Video (12s)

```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 12s | Style: Apple-Keynote Cinematic

HOOK [0-2s]:
Black screen. Single cursor blink in center — small, white, rhythmic, minimal.
Cursor blinks 3 times in darkness. Each blink with soft digital pulse sound.
Camera static. Tension through simplicity.
On third blink, cursor transforms into product logo, scaling small→medium.

ENTER [2-4s]:
Logo settles center-frame. Camera begins slow push-in. Dark gradient background
with subtle brand-color glow behind logo. Logo catches light — metallic/glass
material, not flat. Ambient synth note enters, sustained. Logo rotates slightly
on Y-axis revealing 3D depth.

THROUGH-SCREEN [4-7s]:
Camera pushes through logo — transition effect. Emerges inside product UI.
Full-screen dashboard view. Data populating: charts animate upward, numbers count
up, status indicators turn green one by one. Camera slow pan across features.
Each element animates as camera passes — cards flip in, lists populate,
notifications slide in.

Sound: data cascade sounds synced to each element. Soft clicks, whooshes,
confirmation tones. Music introduces light beat — minimal electronic 100 BPM.
Bass foundation.

DEVICE HERO [7-10s]:
Camera pulls back from UI to reveal device (laptop) in premium workspace.
Product on screen, glowing. Warm ambient. Three-point: warm key, soft fill,
brand-color rim. Shallow DOF — workspace props (plant, coffee, notebook) in soft
bokeh.

CTA [10-12s]:
Final frame: device with product centered. Tagline below — clean typography,
fade-in animation. Logo in corner. Music reaches satisfying resolution.
Sustained final chord.

Material references: --image $LOGO_PNG (logo asset).

Run:
LOGO=/path/to/logo.png
comfy generate seedance \
  --prompt "<paste prompt body>" \
  --image "$LOGO" \
  --aspect_ratio 16:9 --duration 12 --async
```

---

## Worked Example — Feature Demo Speed Run (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Kinetic Demo

HOOK [0-1.5s]:
Tight close-up of UI element — single button labeled with product action. Premium
rendering: micro-shadow, hover state glow, glass-morphism. Dark mode interface
surrounding it.
Cursor approaches button slow motion. Button reacts — hover state activates, glow
intensifies. Sound: subtle UI hover. Camera push to button at 40% frame.
Anticipation.

CLICK [1.5-2s]:
Click. Ripple animation expands from button. Screen shake (micro — 2 pixels).
Sound: satisfying deep click + bass pulse. Hard cut.

MONTAGE [2-4s]:
Rapid montage of features activating. 4 shots, 0.5s each. Each shot different
camera angle. Quick cuts synced to drum hits. Speed ramp: start 1.5x, accelerate
to 3x by end.

PAYOFF [4-6s]:
Camera pulls back to reveal all features working together on full dashboard.
Everything alive, animated, processing. Data flows between sections via animated
connection lines or particle streams. Sound: full music, building energy.
Multiple UI sounds layered.

CTA [6-8s]:
Product zooms out to device level. Device floats with reflection. Performance
metric appears: "10x faster" or "Zero manual steps" in bold typography. Text
animations: scale-up with overshoot bounce. Sound: final resolution chord.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Multi-stage SaaS launch pipeline

```bash
# 1. Hero UI screenshot (still) — for thumbnail + first frame
comfy generate flux-ultra \
  --prompt "premium SaaS dashboard, dark mode, brand-color accent, glass-morphism cards, data visualizations, clean typography, three-point studio lighting, photoreal UI render" \
  --aspect_ratio 16:9 \
  --download /tmp/ui_hero.png

# 2. Animate hero into 8s reveal
comfy generate pika-i2v --image /tmp/ui_hero.png \
  --prompt "camera slow push-in to UI, data populates with cascade animation, feature cards flip in one by one, brand-color glow intensifies" \
  --duration 8 --async

# 3. Full launch video (high-quality, audio)
comfy generate seedance \
  --prompt "<full hero launch prompt>" \
  --aspect_ratio 16:9 --duration 12 --async
```

---

## Identity locks for SaaS
- UI is the hero. Treat it like hardware in an Apple ad.
- Never use stock office b-roll. Never include "person typing"  unless founder-led.
- Brand colors mentioned in lighting (rim light = brand color).
- 100-110 BPM minimal electronic. No corporate stock music.
- Cursor moves with intention, not random.
- Through-screen transitions for product reveals.
