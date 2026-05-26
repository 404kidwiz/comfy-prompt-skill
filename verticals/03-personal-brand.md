# Vertical: Personal Brand — Founder Authority Content

Adapted from Roman Knox `seedance-personal-brand` skill for Comfy.

## When to use
Personal brand, founder story, day-in-the-life, authority content, thought leadership,
creator content, lifestyle videos, behind-the-scenes, executive presence.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Authority hero video (10s, audio, founder face) | `seedance` | Cloud, async |
| Quick founder clip (5s, image-to-video) | `pika-i2v`, `runway-i2v` | Cloud, async |
| Founder portrait still | `flux-pro`, `flux-ultra` | Cloud, sync |
| Same-identity variation across shots | `flux-kontext` with `--image` | Cloud, sync |

---

## The Personal Brand Problem

Generic personal brand content fails by either:
1. **Talking-head boredom** — straight-to-camera with no production value
2. **Lifestyle fake** — staged "casual" moments that read as performance

Authority content lands when it shows the work + the person + the environment in a
register that feels earned, not staged.

---

## Hook Patterns for Authority

### Eye Contact Lock
```
ECU of eyes in shadow. At 0.6s, eyes snap open and lock into camera. Pupil dilates.
Subtle head tilt forward — predatory, intense. Single rim light catches iris detail.
No blinking for 2s. Sound: heartbeat, low frequency.
```

### Workspace Reveal
```
Open on ECU of a single object on desk (vintage pen, coffee cup, mechanical keyboard).
Camera pulls back over 2s to reveal workspace — screens, equipment, achievements.
Person enters frame at 2s, sits, looks at camera. Establishes authority through context.
```

### Speed-of-Thought
```
Quick cuts (0.3s each) showing rapid sequence: hand writing, screen with code/data,
finger on phone, eye looking through telescope/microscope/lens. 6 cuts in 2s.
At 2s, hard cut to person centered, calm, focused. Speed→stillness = mastery.
```

---

## Lighting for Authority

### Founder Studio (preferred)
```
Three-point: warm key 45° from camera-left, minimal soft fill from right, strong
brand-color or warm rim light from behind separating subject from environment.
Environment props (screens, books, instruments of trade) lit subtly with practicals.
Background falls 1-2 stops below subject — clear depth, hero subject, authority.
```

### Documentary Real
```
Single large softbox window-left (natural daylight register). No fill. Subject lit
naturally with one side in shadow. Environment visible in soft natural light.
Reads as authentic captured moment, not staged shoot.
```

### Power Silhouette
```
Backlit silhouette at golden hour or against bright window. Subject reads as shape
only. Rim light separates from background. Used for closing beat or hero opening
when face reveal is downstream.
```

---

## Camera Language for Personal Brand

| Move | Use |
|------|-----|
| Slow Push-In | Emotional intensification on founder face. 10% scale change over 5s. |
| Slow Orbit | 90° around workspace. Reveals depth of environment. Authority through context. |
| Static Locked-Off MCU | Conversation/interview register. No movement. Subject does the work. |
| Walk-and-Talk Steadicam | Following founder through environment. Documentary feel. |
| Workspace Reveal Pull-Back | ECU on hands working → pull back to reveal full workspace. |

---

## Worked Example — Founder Authority Hero (10s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s | Style: Documentary-Cinematic

HOOK [0-1.5s]:
ECU of eyes in low-key lighting. Single rim light from right catches iris detail.
Eyes focused, intense, looking slightly off-camera. Shallow DOF — only eyes sharp.
Static shot. No blinking. Minimal ambient — room tone only. Camera micro-pushes
(barely perceptible forward movement). Tension through stillness.

LOCK [1.5-2s]:
Eyes shift to lock directly into camera. Subtle head tilt forward. Direct gaze =
the hook — primal social brain activation. Sound: single low-frequency pulse
synced to eye contact moment.

REVEAL [2-4s]:
Camera pulls back to MS revealing person in workspace/studio. Three-point lighting:
warm key, minimal fill, strong backlight separating from dark environment.
Environment communicates authority — screens, equipment, clean desk. Person's
posture confident, centered in frame.

ENVIRONMENT [4-7s]:
Camera slow orbit 90° around subject. Environment details reveal — achievements,
tools of trade, brand elements. Lighting shifts as camera moves, revealing new
depth layers. Ambient electronic music enters, minimal and modern.

LANDING [7-10s]:
Camera settles at 3/4 angle. Subject in power position frame-left, environment
frame-right. DOF racks from subject to background detail and back. Music reaches
steady state. Composition suggests story continuing beyond clip.

Sound: 0-1.5s silence. 1.5s low pulse. 2-10s ambient electronic, bass-forward,
no vocals. Clean, modern, authoritative.

Material references: --image $FOUNDER_PORTRAIT (founder face/person), --image $WORKSPACE
(workspace environment for visual coherence).

Run:
PORTRAIT=/path/to/founder.jpg
comfy generate seedance \
  --prompt "<...>" \
  --image "$PORTRAIT" \
  --aspect_ratio 9:16 --duration 10 --async
```

---

## Worked Example — Day-in-the-Life Vignette (8s, Multi-shot)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Documentary-Cinematic

[0-2s] HOOK — Speed-of-Thought:
Quick cuts (0.3s each, 6 shots): hand writing in notebook, fingers on phone, coffee
pour close-up, screen with data/code, eyes scanning, pen tapping. Each cut synced
to single percussive sound. Cinematic Steadicam handheld register.

[2-5s] SLOW:
Hard cut to MCU founder at desk, looking down at work. Slight micro-push camera.
Single window-light from left. Subject does not look at camera. The work IS the
subject.

[5-8s] LOOK UP:
Founder looks up — slow, deliberate. Eye contact lock with camera over 1s.
Composition: founder frame-left, environment frame-right, brand-color rim light.
Music resolves. Final frame holds.

Sound: 0-2s percussive cuts + ambient. 2-5s near-silence (room tone). 5-8s warm
ambient pad enters, resolves on final eye contact.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Identity locks for personal brand
- Founder face NEVER staged-smiling at camera. Eye contact = pause, not pose.
- Environment = authority. Lighting reveals depth.
- Slow camera, not flashy. Authority is calm.
- Real work visible. No stock-photo gestures.
- Single founder, no extras (or extras out of focus background only).
- 2-second silence beats are common — premium pacing.
