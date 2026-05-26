# Vertical: Viral Hook — Scroll-Stopping Short-Form

Adapted from Roman Knox `seedance-viral-hook` skill for Comfy Cloud / local models.

## When to use
User asks for viral, hook, scroll-stop, retention, views, TikTok, Reels, Shorts,
attention-grabbing video, pattern interrupt.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Hero hook (8-10s, audio, vertical) | `seedance` | Cloud, async |
| Quick hook (5s clean motion) | `pika` | Cloud, async |
| Image-to-video hook from static keyframe | `pika-i2v`, `runway-i2v` | Cloud, async |
| Repeat-iteration / batch (no cost) | `Image to Video (Wan 2.2).json` | Local |

## Hook patterns
Pull from `verticals/shared/hooks.md` — 12 universal patterns. Pick ONE per gen.

## Sound design
Pull from `verticals/shared/sound-design.md`. Bass Drop and Voice Hook hit hardest
for viral. For non-audio models, describe sound to lock motion timing then add in DAW.

## Platform tuning
Pull from `verticals/shared/platform-optimization.md`.

---

## Camera Movement Library — Fast Hooks

| Move | Speed | Purpose | Phrasing |
|------|-------|---------|----------|
| Snap Zoom | 0.3s | Instant focus, shock | "Snap zoom from wide to tight close-up in 0.3s. No easing — hard mechanical zoom. Subject centered." |
| Whip Pan | 0.5s | Energy, transition | "Whip pan left-to-right in 0.5s. Motion blur trails. Camera settles with slight overshoot and bounce-back." |
| Drop Shot | 0.4s | Falling sensation | "Camera drops vertically 6 feet in 0.4s. Stomach-drop sensation. Subject stays centered. Frame shakes on landing." |
| Dutch Snap | 0.3s | Unease, style | "Camera rotates 30 degrees clockwise in 0.3s. Horizon tilts. Hold the tilted frame — don't correct it." |

## Camera Movement Library — Reveal Hooks

| Move | Speed | Purpose | Phrasing |
|------|-------|---------|----------|
| Pull-Back Reveal | 2s | Context expansion | "Tight close-up on detail. Camera pulls back steadily over 2s, revealing full scene. Context changes meaning of what was shown." |
| Orbit Reveal | 3s | 360 discovery | "Camera orbits 180° around subject over 3s. Each 45° reveals new environmental element. Constant distance from subject." |
| Rise Reveal | 2s | Scale, majesty | "Camera rises vertically 20 feet over 2s. Ground-level detail gives way to aerial perspective. Reveals scale of scene." |

---

## High-Engagement Lighting

### Neon Contrast
```
Dual-color neon: pink/cyan or orange/blue from opposing sides. Hard shadows where
colors meet. Subject's face split between warm and cool. Background dark, no fill.
Rim light separates from black background. Colors at 80% saturation. Scroll-stopping.
```

### Silhouette Pop
```
Complete backlight silhouette. Strong source directly behind subject (window, LED
panel, sunset). No fill light — pure black outline. Shape tells the story. Viewer
can't identify subject = curiosity. Edge light catches hair/shoulder outline.
Background blown out to white/gold.
```

### Flash Strobe
```
Strobe lighting at 4Hz — rapid on-off creating freeze-frame effect. Subject in motion
captured in staccato bursts. Dark between flashes. Nightclub intensity. Sound synced
to strobe rate. Background pure black between flashes.
```

---

## Worked Example — Product Reveal Hook (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Cinematic ASMR

HOOK [0-2s] — Obscured Subject:
ECU of fingers slowly peeling back matte black packaging material. Macro lens,
shallow DOF (f/1.4 equivalent). Warm side-light from left, long shadows across
textured surface.
Only fingers and packaging visible. Material peels with satisfying slow motion
at 0.5x speed.
Sound: ASMR-quality crisp paper/foil texture amplified. No music. Camera slowly
pushes in.

ESCALATE [2-4s] — Product edge becomes visible. Metallic, catching light. Camera
pull-back begins. Single lens flare as product surface catches key light. Soft
synth note enters audio.

PAYOFF [4-6s] — Full product revealed in hero position. Camera orbits 90° at
constant distance. Three-point lighting: warm key 45° left, soft fill right, cyan
rim behind. Background transitions from black to gradient.

LOOP / CONTINUITY [6-8s] — Product floats/rotates center frame. Logo catches
light. Music builds with bass + synth layers. Camera slowly pushes in to final
close-up of key feature detail.

Sound: 0-2s ASMR texture only. 2-4s single sustained synth note. 4-8s minimal
electronic, bass-forward, modern. No voiceover.

Mood: Premium, satisfying, curiosity-driven. The unboxing IS the hook.

Run:
comfy generate seedance \
  --prompt "<paste prompt body above as single string>" \
  --aspect_ratio 9:16 --duration 8 --async

# Log job
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py log seedance <job_id> --prompt "viral hook product reveal"
```

---

## Worked Example — Mystery / Curiosity Loop (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Cinematic Mystery

HOOK [0-1s] — Subliminal Flashes:
Black screen 0.5s. Then rapid flash of image for exactly 3 frames (0.12s) — too
fast to consciously process but brain registers. Black 0.3s. Repeat 3 times with
different angles of the subject. Each flash with sharp digital click sound.

REVEAL [1-2s] — Image holds 1s but heavily blurred (gaussian max). Shape + color
visible, no detail. Camera slow push-in. Rising frequency tone building tension.

CLEAR [2-4s] — Blur clears over 2s. Rack focus from completely soft to tack sharp.
Brain gets more info each frame. Camera continues steady push-in. Tension tone
resolves into clean musical note as image sharpens.

PAYOFF [4-6s] — Subject fully revealed in sharp focus. Camera begins slow orbit.
Dramatic lighting — strong key 60° above, minimal fill, subject sculptural. Music
enters, confident, modern.

LANDING [6-8s] — Camera completes 180° orbit. Each angle reveals new detail/
context. Lighting shifts dynamically. Final frame settles on most dramatic angle.
Music plateau, bass anchors visual.

Sound: 0-1s digital clicks. 1-2s rising tension. 2-4s resolution tone. 4-8s full
electronic track, mid-tempo, bass-driven.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Identity locks for this vertical
- Cinematic finish — never YouTube-tutorial flat
- Per-second beat structure mandatory
- One hook pattern per gen — don't combine
- Sound stack named even on silent models (locks motion timing)
- Last 0.5s frames loop back to first frame (TikTok algorithm preference)
