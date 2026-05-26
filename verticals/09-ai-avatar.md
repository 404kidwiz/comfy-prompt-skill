# Vertical: AI Avatar — Digital Persona Content at Scale

Adapted from Roman Knox `seedance-ai-avatar` skill for Comfy.

## When to use
Virtual spokesperson, digital twin, AI presenter clip, avatar-based marketing,
virtual influencer, synthetic media, animated spokesperson.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Avatar hero video (10s, audio, talking head) | `seedance` | Cloud, async |
| Image-to-video avatar animation | `pika-i2v`, `runway-i2v` | Cloud, async |
| Avatar identity hero still | `flux-pro`, `flux-ultra` | Cloud, sync |
| Identity-locked variations | `flux-kontext` | Cloud, sync |
| Local avatar testing | `Image to Video (Wan 2.2).json` | Local |

---

## Why AI Avatars Now

AI avatars work because:
1. **Scale** — generate 100 variations of the same persona without re-shoot
2. **Consistency** — character looks the same across thousands of clips
3. **No talent risk** — no scheduling, no fatigue, no PR drama
4. **Brand control** — exact appearance, voice, register every time

The fail state: uncanny valley. The fix: lean into the synthetic register
deliberately, or push hard for photoreal with consistent identity locking.

---

## Avatar Style Spectrum

| Style | Use case | Recommended models |
|-------|---------|-------------------|
| **Photoreal Human** | Customer-facing spokesperson | `flux-pro` (still) + `seedance` (animate) |
| **Stylized 3D** | Tech / SaaS / gaming brand | `nano-banana`, `stability-sd3` (Pixar-leaning) |
| **Anime / Illustrated** | Creator / lifestyle / niche | `stability-sd3`, `recraft` |
| **Synthetic Premium** | Luxury / fashion brand | `flux-ultra` (deliberate uncanny polish) |
| **Holographic / Cyber** | Sci-fi / futuristic register | `flux-pro` + style snippet from cyberpunk |

---

## Hook Patterns for Avatars

### Direct Address Lock
```
ECU of avatar's face. Eyes already locked into camera at 0s. Subtle micro-expressions
(blink, slight head tilt, half-smile). At 1.5s, avatar begins speaking. Voiceover
delivered cleanly. The eye contact + immediate address = primal attention.
```

### Avatar Reveal
```
0-1.5s: tight detail of an object/environment with brand colors. At 1.5s, avatar
walks/enters frame from edge. Camera pulls back to MS. Avatar establishes presence
through movement + environment context.
```

### Multi-Self Cuts
```
Same avatar in multiple contexts/poses, quick cuts (0.5s each, 4-6 shots). Each
shot different angle, environment, action — but same identity. Music synced to
cuts. Reads as "this persona exists across all these contexts."
```

### Synthetic Self-Aware
```
Avatar in clean studio environment. Avatar gestures to environment or themselves
acknowledging the AI nature. Subtle motion glitches or interface elements visible
around them (data lines, particle effects). Embrace the synthetic register openly.
```

---

## Environment Design for Avatars

### Clean Studio (default)
```
Seamless background (white / gray / brand color). Avatar centered MS or 3/4.
Three-point lighting. No environmental clutter. Reads as production-grade
spokesperson.
```

### Branded Context
```
Avatar in environment that signals brand (office for SaaS, gym for fitness,
kitchen for food brand). Environment carefully designed with brand colors and
props. Avatar interacts naturally with environment.
```

### Holographic Frame
```
Avatar appears as hologram in dark space. Particle/data effects around them.
Subtle blue/cyan rim light. Reads as future/AI register without being cliché.
```

### Cinematic Real-World
```
Avatar in realistic location — coffee shop, street, office. Treated as a real
person in real space. Lighting consistent with environment. Most ambitious — must
nail identity locking and physics.
```

---

## Camera Techniques for Avatar Content

| Move | Use |
|------|-----|
| Static Locked-Off MCU | Spokesperson register. Lets avatar do the work. |
| Slow Push-In | Emotional intensification on avatar speaking. |
| Slight Handheld Drift | Adds "captured moment" realism, mitigates uncanny. |
| Match-Cut Between Cuts | Same avatar identity across multiple contexts. |
| Through-Avatar Transition | Camera moves through avatar to next scene (sci-fi register). |

---

## Lighting for Avatar Content

### Premium Spokesperson
```
Three-point: warm key 45° front-left, soft fill right, cool/brand rim light behind.
Avatar face evenly lit, slight separation from background. Reads professional.
```

### Cinematic Authority
```
Single side-key from camera-left, low ambient fill, subject reads sculptural.
Background falls 1-2 stops below. Used for confident / serious avatars.
```

### Holographic Register
```
Multiple colored rims (cyan + magenta or warm + cool) with cool ambient base.
Avatar reads luminous, slightly otherworldly. Particle/data effects in environment.
```

### Beauty/Editorial
```
Large softbox key positioned slightly above, soft eye-light, no fill. Avatar in
high-end editorial register. Cool background, warm subject. Fashion / lifestyle
avatars.
```

---

## Sound Design for Avatars

| Layer | What it does |
|-------|--------------|
| Avatar voice | Primary track. Cloned voice or synthetic. Consistent across clips. |
| Music | Subtle pad / beat. Mixed -12dB below voice. Brand-consistent across avatar's videos. |
| Environment | Light room tone or environmental ambience. Avoids "sound studio" sterility. |
| Branding | Subtle audio logo on intro/outro frames (optional). |

For audio-rendering models, describe voice quality + tone explicitly:
"Voiceover: confident female voice, slight reverb, warm low-mid presence, no high-end
sibilance, clean recording" — locks the voice register.

---

## Worked Example — Avatar Spokesperson (10s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s | Style: Premium Spokesperson

[0-2s] HOOK — Direct Address Lock:
ECU of avatar's face. Eyes already locked into camera at 0s. Subtle micro-
expressions — slight blink at 0.8s, gentle head tilt forward at 1.2s. Soft warm
key from camera-left, brand-color rim light behind. Background falls to soft
gray bokeh.
At 1.5s: avatar begins speaking. Voice: confident, warm low-mid presence.

[2-5s] STATEMENT:
Camera slight pull-back to MCU. Avatar delivers first sentence — key value
proposition. Subtle gestures with hands visible at bottom of frame. Environment
softens into bokeh: clean modern workspace implied by brand-color hints in
background.

[5-7s] BUILD:
Slight push-in toward avatar face. Avatar continues with key insight or specific
benefit. Music ambient pad enters at 5s underneath voice. Avatar's micro-
expressions support the message (slight smile on benefit moment, raised eyebrow
on key point).

[7-9s] LANDING:
Cut to MS angle, avatar 3/4 facing camera, gesturing toward a brand element or
product (out of frame, implied). Voice lands CTA — clear call to action.

[9-10s] BRAND BEAT:
Brand mark / logo fades in lower-third. Avatar holds confident expression. Music
resolves on sustained chord.

Sound: 0-1.5s ambient + soft pad. 1.5-9s avatar voice primary, pad underneath.
9-10s music resolution.

Material references: --image $AVATAR_PORTRAIT (avatar identity hero).

Run:
AVATAR=/path/to/avatar.png
comfy generate seedance \
  --prompt "<...>" \
  --image "$AVATAR" \
  --aspect_ratio 9:16 --duration 10 --async
```

---

## Worked Example — Multi-Self Cuts (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Multi-Context Avatar

[0-1.5s] HOOK:
Avatar in CUT 1 — clean studio MCU, looking at camera, slight smile, gentle wave.
Sound: upbeat electronic enters immediately.

[1.5-3s] CUT 2:
Same avatar in workspace context — typing on laptop, MCU 3/4 angle. Warm window
light register. Avatar looks up briefly at camera. 1.5s hold.

[3-4.5s] CUT 3:
Avatar in outdoor context — sidewalk, casual register, walking toward camera,
WS angle. Golden hour lighting. 1.5s hold.

[4.5-6s] CUT 4:
Avatar in branded environment — coffee shop or studio with brand elements visible.
MCU laughing at something off-camera. 1.5s hold.

[6-8s] FINAL:
Avatar in clean studio, MS, eye contact with camera, slight smile, single gesture.
Text overlay: brand mark + tagline. Music resolves.

Identity lock note: --image $AVATAR ensures same identity across all four cuts.

Run:
comfy generate seedance --image /path/to/avatar.png --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Identity locking for avatar content

**Critical pattern.** Avatar drift across clips = brand destruction. Always:

```bash
# 1. Generate hero avatar identity reference
comfy generate flux-pro \
  --prompt "premium spokesperson portrait, [age, gender, ethnicity, hair, wardrobe specifics], MCU 3/4 angle, warm three-point lighting, photoreal skin texture, brand-color rim light, neutral expression, eye contact" \
  --aspect_ratio 3:4 \
  --download /tmp/avatar_hero.png

# 2. For every subsequent gen, pass as --image with explicit identity lock
comfy generate seedance \
  --image /tmp/avatar_hero.png \
  --prompt "SAME PERSON FROM IMAGE: same face same hair same wardrobe same age. Now in [new context/action]. Identity locked." \
  --duration 10 --async
```

---

## Identity locks for avatar content
- ALWAYS pass hero portrait as --image when generating any avatar video.
- Explicit "SAME PERSON FROM IMAGE" phrasing locks identity better than vague refs.
- Avatar voice/tone consistent across ALL clips for brand. Use cloned voice or
  same model+settings.
- Avoid uncanny valley by either embracing synthetic register OR going full photoreal.
- Background environment can vary — identity must not.
- Subtle micro-expressions sell realness. Eye contact + slight blink + half-smile.
