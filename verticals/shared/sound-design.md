# Sound Design — 4-Layer Stack

Adapted from Roman Knox / @roman.knox skill set.
Apply to audio-capable Comfy models: `seedance` (cloud), local `Text to Audio (ACE-Step).json`.

For non-audio models (`pika`, `runway-i2v`, `vidu`), describe intended sound in the prompt
even though the model won't render it — this guides motion timing and post-production audio sync.

---

## The Stack

Layer these elements for maximum impact:

1. **Base Layer** — Ambient bed (room tone, wind, hum) or silence
2. **Impact Layer** — Bass hits, whooshes, clicks synced to visual beats
3. **Music Layer** — Trending audio or custom beat (enter after 1-2s)
4. **Voice Layer** — Voiceover hook or text-to-speech (optional)

---

## Sound Templates by Hook Type

### The Bass Drop
Silence → explosion.

```
Audio: 1.5s of near-silence (faint ambient). At 1.5s marker: deep 808 bass hit
synced to visual cut. Sub-bass vibration. Music enters on beat 2.
```

### The Glitch
Digital disruption.

```
Audio: clean ambient interrupted by digital glitch sounds — bit-crush, stutter,
frequency sweep. 0.3s glitch at 0.8s mark. Creates "something wrong" feeling.
Synced to visual glitch effect.
```

### ASMR Crunch
Tactile satisfaction.

```
Audio: hyper-close microphone capturing texture sounds — crunch, crack, pour, slice.
No music. Pure sound design. Binaural feel. Viewer's brain triggers tactile response.
```

### Voice Hook
Words that stop scroll.

```
Audio: confident voice says [provocative 3-5 word statement] in first 1.5s. No intro,
no greeting — statement starts at 0.0s. Slight reverb, clean recording. Statement
creates question or controversy.
```

### The Build & Drop
Tension into release.

```
Audio: 0-3s rising synth pad, slow swell from low to high frequency. At 3s: hard
cut to silence (0.2s). Then bass drop + percussion full intensity. Music continues
at full energy through end.
```

### Silence Anchor
Premium / luxury register.

```
Audio: complete silence for first 2s. At 2s: single soft mechanical tick or chime.
Repeats every 1-2s. No music. The silence IS the message. Used in luxury / minimal
brands where presence matters more than energy.
```

---

## Sound × Camera Sync Rules

| Camera move | Sound sync |
|-------------|-----------|
| Snap zoom | Sharp impact + bass hit on zoom complete |
| Whip pan | Whoosh on motion, settle sound on landing |
| Drop shot | Falling whistle + heavy impact on landing |
| Dutch snap | Tension tone slide + click on tilt complete |
| Pull-back reveal | Music swell building over the reveal |
| Orbit reveal | Music opens up as new context appears |
| Rise reveal | Ascending pad, peak at full reveal |

---

## Platform-specific audio

| Platform | Audio priority |
|----------|---------------|
| TikTok | Trending audio at maximum volume. Original audio secondary. Hook line clearly audible 0-1.5s. |
| Instagram Reels | Music quality matters more than trending. Cleaner mix. Hook at 2s. |
| YouTube Shorts | Voiceover-friendly. Audio quality > trending. Hook at 2-3s. |
| LinkedIn | Voiceover + ambient only. No music in many cases (auto-mute default). Caption-driven. |

---

## Audio in Comfy commands

`seedance` natively renders audio when prompted. Other video models won't — describe
the audio anyway to lock motion timing:

```bash
# Audio-rendering (seedance only)
comfy generate seedance --prompt "<visual> ... Audio: bass drop at 1.5s synced to color burst, ASMR steam sound layered, ambient kitchen room tone throughout" --duration 8 --async

# Silent video models (pika, runway, vidu) — audio is post-production
comfy generate pika --prompt "<visual with motion beat timing locked to imagined audio>" --duration 5 --async
# Then sync audio in DAW / video editor
```

---

## Local audio workflow

```bash
# Generate background music with ACE-Step (local)
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
    "/Users/dawizkidmal/ComfyUI/blueprints/Text to Audio (ACE-Step 1.5).json" \
    --prompt "minimal electronic beat, 100 BPM, bass-forward, modern confident" \
    --out /tmp/audio.json

comfy launch --background
comfy run --workflow /tmp/audio.json --wait --timeout 120
```
