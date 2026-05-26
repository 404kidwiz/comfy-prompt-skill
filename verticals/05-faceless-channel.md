# Vertical: Faceless Channel — No-Face B-Roll Content

Adapted from Roman Knox `seedance-faceless-channel` skill for Comfy.

## When to use
Faceless YouTube channel, anonymous TikTok, narration-driven content, stock-footage-
style AI content, no creator on camera, voiceover video, finance / news / educational
channels without host face.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Hero faceless b-roll (10s, atmospheric) | `seedance`, `grok-video` | Cloud, async |
| Quick atmospheric clip (5s) | `pika`, `vidu` | Cloud, async |
| Hands / object detail (image-to-video) | `pika-i2v`, `runway-i2v` | Cloud, async |
| B-roll still pack | `flux-pro`, `nano-banana` | Cloud, sync |
| Local batch generation (no cost) | `Text to Video (Wan 2.2).json` | Local |

---

## Three Laws of Faceless Content

1. **Visual must carry the story** — without face, every other element works harder
2. **Audio drives pacing** — voiceover or music dictates cut rhythm, not visual energy
3. **Texture > spectacle** — viewers connect to specific tactile detail, not generic scenes

---

## Hook Patterns for Faceless

### Object-as-Character
```
ECU of inanimate object treated as the protagonist — pen on desk, coin on counter,
single leaf falling. Camera tracks it with care, as if it has agency. Soft natural
light. ASMR-quality close audio. Object IS the character.
```

### Hands at Work
```
Tight framing on hands only — typing, writing, assembling, cooking, drawing. Macro
lens, shallow DOF. Slow motion 0.5x. Sound: tactile work sounds amplified. No face,
no body — hands tell the story.
```

### Money Shot
```
ECU of cash being counted, coins stacking, dollar bills falling slow motion, gold
catching light. Common faceless-finance hook. Cinematic lighting (warm key + cool
rim). Sound: cash riffle or coin-clink ASMR.
```

### Atmospheric Establishing
```
WS of a moody location — empty city at night, foggy mountain at dawn, candlelit
room. Slow camera move. Music or voiceover enters at 2s. The location IS the hook.
```

---

## Visual Style Templates

### Finance / Business Faceless
```
Dark luxury aesthetic. Money close-ups, watch/jewelry shots, skyline at night,
luxury car detail, hand pouring whiskey. Color palette: black, gold, deep amber.
Slow cinematic camera. Voiceover-driven.
```

### Educational / News Faceless
```
Clean infographics + b-roll. Animated text overlays, charts, maps. B-roll of generic
hands typing, screens, lab equipment, archival footage feel. Voice authority register.
Music: neutral ambient, doesn't pull focus from voiceover.
```

### Self-Improvement / Hustle Faceless
```
Energetic montage: cityscape at dawn, hands lacing running shoes, coffee being poured,
notebook with goals written, gym detail. Color: warm sunrise + cool ambient mix.
Music: building electronic with motivational pads.
```

### True Crime / Mystery Faceless
```
Vintage / archival aesthetic. Empty rooms, single objects with history, old maps,
black-and-white photos, hands turning pages. Slow camera. Music: low ambient drone.
Voiceover dominates.
```

---

## Camera Movement Library — Faceless

| Move | Use |
|------|-----|
| Slow Push-In on Object | Treat the object as a character. 4-5s slow push. |
| Macro Rack Focus | Pull focus from background detail to foreground texture. ASMR for the eye. |
| Locked-Off Static | Single shot, no movement, lets the voiceover work. Premium register. |
| Top-Down Overhead | Hands working from above. Cooking, writing, assembling. Camera bird's-eye. |
| Slow Orbit on Object | 90° orbit around hero object reveals 3D form. Product / artifact register. |

---

## Lighting Playbook

| Setup | Use |
|-------|-----|
| **Single Window Key** | Natural soft light, side angle. Premium documentary feel. |
| **Candle / Practical Only** | Single warm practical source. Mystery / luxury / contemplative. |
| **Dark Mode Glow** | Subject in shadow with single rim of color. Tech / business register. |
| **Overcast Diffused** | Soft even light, no shadows. Educational / instructional register. |

---

## Sound Design — Two Approaches

### Voiceover-Driven (most faceless content)
```
Voice as primary track. Music as bed, mixed -12dB below voice. Sound effects
synced to cut points (whoosh on transition, click on text reveal). No overpowering
music swells — voice is king.
```

### Pure Ambient (luxury / contemplative)
```
No voiceover. Ambient sound design carries everything — rain, fire crackle, wind,
city hum. Maybe single music layer extremely sparse. The atmosphere IS the message.
```

---

## Worked Example — Finance Faceless Hook (10s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s | Style: Dark Luxury Finance

[0-2s] HOOK — Money Shot:
ECU of hundred-dollar bills riffling between fingers, macro lens, shallow DOF.
Warm side key from left, deep amber color grade. Slow motion 0.5x. Sound: ASMR
cash riffle amplified. No voiceover yet.

[2-5s] CONTEXT:
Cut to MCU of luxury wristwatch on a dark wood desk, glass of whiskey beside it,
warm amber light. Camera slow orbit 30° around watch. Voiceover begins: confident
authority register, 3-second statement.

[5-8s] BUILD:
Cut to WS of nighttime city skyline from high-rise window. Slow camera pull-back
revealing reflected skyline in dark window. Subtle electronic ambient enters.
Voiceover continues with key insight.

[8-10s] CTA / LOOP:
Cut back to ECU of cash riffling (matches opening shot — loop continuity). Music
peaks. Voiceover delivers final hook line. Final frame holds on cash with subtle
brand mark visible in corner.

Sound: 0-2s ASMR cash + ambient. 2-5s warm ambient pad + voiceover. 5-8s subtle
electronic enters under voice. 8-10s music peaks, voiceover lands final line.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 10 --async
```

---

## Worked Example — Educational Faceless (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Clean Educational

[0-2s] HOOK — Hands at Work:
Top-down ECU of hands sketching a simple diagram on a notebook. Macro lens. Soft
even daylight. Sound: pen on paper ASMR, faint ambient room tone. No music.

[2-5s] BUILD:
Cut to MS of the diagram filled in, text overlays appear next to each element
labeling them with caption-style typography. Voiceover begins explaining the
concept. Camera slight push-in.

[5-8s] LANDING:
Cut to clean text-overlay screen: key takeaway statement in bold sans-serif.
Music subtle ambient enters. Voiceover delivers final summary. Final frame holds
on text for 2s.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Identity locks for faceless content
- NEVER show faces. Hands, objects, environments, atmosphere only.
- ASMR-tier sound on tactile shots. Sound is half the hook.
- Voiceover drives pacing. Cut on word emphasis, not random.
- Texture > spectacle. Specific detail beats generic vista.
- Color palette ruthlessly consistent across all b-roll in same video.
- B-roll feels intentional, not stock. Specific, not generic.
