# Vertical: Podcast Visual — Audio-to-Cinematic Video

Adapted from Roman Knox `seedance-podcast-visual` skill for Comfy.

## When to use
Podcast clip video, audiogram alternative, podcast highlight reel, interview clip,
sound bite visualization, audio-to-visual content, episode promo.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Podcast scene generation (10s, audio-aware) | `seedance` | Cloud, async |
| Single visual layer (5s, image-to-video) | `pika-i2v`, `runway-i2v` | Cloud, async |
| Kinetic typography frames | `ideogram` (text), then `Canny to Video (LTX 2.0).json` | Cloud + local |
| Local repeat / batch (no cost) | `Text to Video (LTX-2.3).json` | Local |

---

## The Podcast Visual Problem

Audiograms (waveform + static photo) get 1% retention. Cinematic visual treatments
of podcast audio can hit 60%+ retention. The visual must:

1. **Match audio rhythm** — cuts and motion sync to speech beats
2. **Reinforce content** — visual metaphor or context for what's being said
3. **Maintain visual interest** — never static for 15+ seconds

---

## Visual Formats for Podcast Clips

### Cinematic Talking-Head Replacement
Generate visual that "represents" the speaker without showing them. Their voice
plays over scenes that match their content. Hand details, workspace, related
environments. Faceless register (see vertical 05).

### Kinetic Typography
Words from the audio appear on screen synced to speech. Bold, animated, beat-driven.
Best for short punchy quotes (15s or less).

### Visual Metaphor Montage
Each sentence gets a visual representation. Quick cuts (1-2s each) following the
speech narrative. Example: speaker says "building a business is like climbing a
mountain" → cut to mountain climbing footage / sunrise from peak / hands gripping
rope.

### Single Sustained Scene
One cinematic shot held throughout. Audio is primary, visual provides mood. Best
for premium / contemplative content (interviews, reflective episodes).

### Animated Quote Card
Bold typography with speaker name + quote text. Subtle motion (slow zoom, slight
particle effect). Best for sharing on Twitter/LinkedIn.

---

## Hook Patterns for Podcast Clips

### Quote-First
```
Black screen. Bold text overlay appears synced to speaker's opening line: their
strongest sentence first. Hold 2s. Cut to visual content with audio continuing.
The QUOTE is the hook.
```

### Sound-First
```
1.5s of silence (black screen or single image). Then audio drops in HARD with
speaker's opening line. Hard visual cut synced to first word. The sudden audio
IS the hook.
```

### Visual Metaphor Lead
```
0-2s: cinematic establishing shot related to topic (city skyline for business clip,
forest for nature clip, etc.). Speaker audio begins underneath. Visual carries the
mood while audio carries the message.
```

### Reaction Shot Open
```
ECU of hands gesturing, eyes widening, mouth in mid-word — implying an emotional
beat about to happen. Audio begins underneath. Build tension visually then deliver
the audio payoff.
```

---

## Audio-Visual Sync Techniques

### Beat-Synced Cuts
```
Cut on word emphasis or sentence breaks. Never cut mid-syllable. The cut points
align with speech rhythm, making the visual feel native to the audio.
```

### Motion-Synced Camera
```
Camera moves accelerate during energetic speech, slow during calm moments.
Push-in during emotional intensity, pull-back during summary statements.
```

### Color-Synced Mood
```
Color grade shifts subtly with speech tone. Warm during personal/emotional, cool
during analytical/serious. Saturation rises during energy, falls during gravity.
```

### Typography Beat
```
For kinetic typography: text appears one word at a time synced to speech.
Each word lands on its spoken syllable. Bold, brief, no full sentences.
```

---

## Camera and Composition for Non-Live Content

Since you don't have live footage of the speaker:

| Format | Camera approach |
|--------|----------------|
| Faceless cinematic | Slow Steadicam through workspace / location |
| Visual metaphor | Each shot has different camera move synced to beat |
| Single scene | Locked-off or extremely slow push-in for the duration |
| Kinetic typography | Camera locked, text animates within frame |
| Quote card | Slow zoom or static with subtle particle motion |

---

## Lighting for Podcast Visuals

| Setup | Use |
|-------|-----|
| **Warm Documentary** | Single window key. Reads as captured-moment authenticity. |
| **Dark Premium** | Single side-key, deep ambient. Reads as serious / luxury podcast. |
| **Clean Editorial** | Even softbox + brand color rim. Reads as polished podcast brand. |
| **Cinematic Color** | Two-tone (warm + cool) for visual interest in single scene. |

---

## Typography for Podcast

Use `ideogram` or `dalle` for clean text rendering. Avoid Flux models for primary
text (they butcher fine kerning).

```bash
comfy generate ideogram \
  --prompt "kinetic typography frame, bold sans-serif word 'BREATHE' filling 70% of frame, ivory text on pure black background, 200pt extended display typeface, perfect kerning, tight letter-spacing, vector-clean edges, with subtle soft glow effect" \
  --aspect_ratio 9:16 \
  --download /tmp/word.png
```

For animated kinetic typography, generate static frames then animate via local
`Canny to Video (LTX 2.0).json` or composite in DAW/video editor.

---

## Worked Example — Cinematic Podcast Clip (12s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 12s | Style: Premium Faceless Podcast

[0-2s] HOOK — Quote-First:
Black screen. Bold text overlay: speaker's strongest sentence appears word-by-word
synced to their audio. Final word lands with bass hit. Audio: speaker's voice
clear, slight reverb, intimate close-mic register. Sound: ambient room tone
underneath.

[2-5s] VISUAL METAPHOR:
Cut to cinematic visual matching speech content. Example for business podcast:
ECU of hands on a notebook drawing a diagram. Macro lens, warm window light.
Speaker continues audio with key insight. Camera slow push-in.

[5-8s] BUILD:
Cut to MS or WS — wider context of the workspace or environment. Reveal scale
of what the speaker is describing. Camera Steadicam smooth movement. Subtle
music ambient pad enters underneath voice.

[8-10s] LANDING:
Cut to text-overlay frame again — speaker's punchline sentence appears synced
to audio. Bold, brief, impactful. Background: blurred visual continuation from
previous shot.

[10-12s] OUTRO:
Final frame: speaker name + podcast brand mark in clean typography. Sustained
hold. Voice ends. Music resolves on sustained chord. Silence on last frame.

Material references: --image $BRAND (podcast brand visual style reference).

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 12 --async
```

---

## Worked Example — Kinetic Typography (8s)

```
Step 1: Generate static text frames via ideogram
for word in YOU MUST LEARN TO BREATHE FIRST; do
    comfy generate ideogram \
      --prompt "bold word '$word' centered in frame, 200pt extended display typeface, ivory on pure black, perfect kerning, vector-clean edges, subtle drop shadow" \
      --aspect_ratio 9:16 \
      --download "/tmp/kt_${word}.png"
done

Step 2: Composite into video timeline via editor (Premiere / DaVinci / ffmpeg)
       — each word displays for 0.8s synced to spoken word in audio track

# OR use local Canny-to-Video for animated text
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
  "/Users/dawizkidmal/ComfyUI/blueprints/Canny to Video (LTX 2.0).json" \
  --prompt "the typed words BREATHE pulse with rhythmic breath, letters expand on inhale contract on exhale, soft glow accent on each pulse" \
  --out /tmp/kinetic.json

comfy launch --background
comfy run --workflow /tmp/kinetic.json --wait --timeout 300
```

---

## Worked Example — Visual Metaphor Montage (10s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s | Style: Documentary Metaphor Cuts

[0-2s] HOOK:
Speaker audio begins immediately: opening line. Visual: ECU of hands on a guitar
neck, soft amber light. Sound: speaker's voice + faint room tone.

[2-4s] CUT 2:
Wide shot of a mountain at sunrise — visual metaphor matching speaker's content
about challenge / aspiration. Camera slow push toward peak. Speaker continues.

[4-6s] CUT 3:
ECU of pen on paper writing, words appearing — sync to speaker explaining a
concept. Camera top-down. Macro register.

[6-8s] CUT 4:
WS of person walking through forest at golden hour — silhouette only. Speaker
lands key emotional beat. Music enters subtle pad.

[8-10s] LANDING:
Final frame: minimal text overlay — speaker name + podcast title. Held over a
soft blurred continuation of forest visual. Music resolves.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 10 --async
```

---

## Identity locks for podcast visual
- Audio is PRIMARY. Visual serves the audio, not the reverse.
- Cut on speech beats, never mid-syllable.
- Visual metaphor should reinforce content, not distract from it.
- Kinetic typography: one word at a time, synced to spoken word.
- Music sparse, mixed -12dB below voice. Voice must always read clearly.
- Length matches the natural breath of the audio quote — don't pad.
- Final frame holds long enough for speaker name + brand to register.
