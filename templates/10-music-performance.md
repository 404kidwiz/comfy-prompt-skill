# Template: Music / Dance / Performance

## Genre / Use case
Music videos, concert footage, dance performance, choreography, kinetic typography,
album art, performance stills, club / rave aesthetic.

## When to use
User asks for music video, concert, dance, performance, choreography, club, rave,
album cover, performance still, kinetic typography, lyric video.

## Recommended models
- **Dance / kinetic motion**: `seedance` (motion specialty), `pika`.
- **Concert / stage performance**: `seedance` (audio-capable for live feel), `grok-video`.
- **Album cover / performance still**: `flux-pro`, `flux-ultra`, `stability-ultra`.
- **Kinetic typography**: Composite — generate static letters with `ideogram`, animate with local `Text to Video (LTX-2.3).json`.

## Example prompt — `seedance` (dance performance)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s | Style: Cinematic Dance

A solo dancer in matte-black bodysuit performs in an empty industrial warehouse.
Polished concrete floor reflects single overhead beam of white light.
Camera: low circular orbit around the dancer, full 360° over the duration.
[0-3s] Dancer is still, head bowed, hands at sides.
[3-7s] Sudden burst of motion — sharp angular contractions, hard stops, percussive movement.
[7-10s] Dancer freezes mid-pose, arms extended overhead in a tense diagonal.
Internal motion: bodysuit catches highlights at every angle change.
Environmental motion: dust particles caught in the beam, drifting slowly.
Style: Cinematic dance film. Anamorphic widescreen feel. High contrast monochrome
with single warm-amber backlight from far edge of frame.
Sound: live percussion and breath audio.

Run:
comfy generate seedance --prompt "solo dancer in matte-black bodysuit in empty industrial warehouse, polished concrete floor reflects single overhead beam of white light, low circular orbit camera full 360 over duration, [0-3s] dancer still head bowed hands at sides, [3-7s] sudden burst angular contractions hard stops percussive movement, [7-10s] freezes mid-pose arms extended overhead in tense diagonal, bodysuit catches highlights at every angle change, dust particles caught in beam drifting slowly, cinematic dance film anamorphic feel high contrast monochrome with single warm-amber backlight from far edge, live percussion and breath audio" --duration 10 --aspect_ratio 9:16 --async
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "matte-black bodysuit" | Specific costume — silhouette reads in low light |
| "polished concrete floor reflects single overhead beam" | Reflective surface + named light source |
| "low circular orbit camera, full 360° over the duration" | Named camera move + tempo |
| "[0-3s] / [3-7s] / [7-10s] beats" | Choreography needs per-second structure |
| "sharp angular contractions, hard stops, percussive movement" | Specific dance vocabulary |
| "freezes mid-pose, arms extended overhead in tense diagonal" | Final beat = specific resolution shape |
| "bodysuit catches highlights at every angle change" | Internal motion layer (4-layer hierarchy) |
| "dust particles caught in the beam, drifting slowly" | Environmental motion layer |
| "live percussion and breath audio" | Specific audio request for audio-capable model |

## Negative constraints
```
no morphing limbs across the clip, no identity drift, no warping bodysuit,
no flickering background, no extra dancers appearing/disappearing,
no broken anatomy at extreme poses
```

## Common mistakes
1. **No tempo cues** — Dance lives on rhythm. Per-second beats are mandatory.
2. **Vague motion** — "She dances" does nothing. Name technique: "angular contractions", "fluid arabesque", "popping isolations", "krumping bursts".
3. **Mixed styles** — "Hip-hop ballet contemporary" = mush. Pick one register.
4. **Identity drift in long clips** — Comfy video models can morph faces over 10s. Add: `keep same dancer identity, same costume, no morphing`.
5. **No environmental motion** — Empty backgrounds feel dead. Add dust, smoke, fabric drift, light shifts.

## Variations

### Concert / stage — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 10s

A lead singer at the front of a massive arena stage performs into a microphone,
crowd in shadow below, banks of stage lights behind.
[0-3s] LS slight low angle from front-row, singer mid-belt with eyes closed.
[3-6s] Slow push-in to MCU. Singer opens eyes, locks gaze with camera.
[6-10s] Spotlight flares behind, lens flare crosses frame, singer extends mic toward
the crowd, mouths "sing it back".
Environmental motion: stage haze backlit, lighting rig flicker on beat.
Style: Cinematic concert film. Anamorphic flares. Live performance grit.
Audio: lead vocal mic, distant crowd roar, single sustained synth pad underneath.
```

### Club / rave — `pika`
```
Model: pika (cloud, async)
Aspect: 9:16 | Duration: 5s

Inside a packed underground club. POV chest-level moving through the crowd.
Bodies pressed close, hands in the air, strobe lights freezing motion every beat.
Lasers slice through smoke overhead — green, magenta, cyan.
[0-2s] Forward push through dancing bodies, strobes catching faces.
[2-5s] Camera tilts upward — sees DJ booth above, DJ silhouette against LED wall.
Internal motion: hands waving, hair flying, sweat-shine on skin.
Style: 90s rave authentic. Photoreal. Heavy strobe staccato.
High ISO grain. Audio: pulsing 4-on-the-floor with mid-frequency bass.
```

### Album cover (still) — `flux-pro`
```
Model: flux-pro (cloud)
Aspect: 1:1 | Style: Album Cover

MCU Eye Level of an artist in an empty diner booth at 4am.
Wearing a worn leather jacket, hood half-up.
One arm draped over the booth back, looking just past camera with tired half-smile.
Cup of coffee in foreground, steam rising.
Lighting: single fluorescent practical overhead, harsh and unflattering.
Sodium streetlight from window behind, warm orange rim on shoulder.
Style: 1970s singer-songwriter album cover. 35mm film grain. Bleach-bypass color.
Negative space upper-right for artist name + album title (added in post).
```

### Kinetic typography — composite workflow
```bash
# 1. Generate clean text layer via ideogram
comfy generate ideogram \
  --prompt "bold sans-serif word 'BREATHE' filling the frame, ivory text on pure black background, 200pt extended display typeface, perfect kerning, vector-clean edges" \
  --aspect_ratio 16:9 \
  --download /tmp/word.png

# 2. Animate the text — local LTX text-to-video with controlnet
# (Use Canny to Video LTX 2.0 blueprint with the static frame as canny input)
python3 ~/.claude/skills/comfy-prompt/scripts/parameterize.py \
  "/Users/dawizkidmal/ComfyUI/blueprints/Canny to Video (LTX 2.0).json" \
  --prompt "the word BREATHE pulses with rhythmic breath — letters expand slightly on inhale, contract on exhale, soft warm glow appears behind text on each pulse, black background" \
  --out /tmp/kinetic.json

comfy run --workflow /tmp/kinetic.json --wait --timeout 300 --verbose
```

### Choreography reference video — `seedance` (with reference image)
```bash
# 1. Generate hero pose still
comfy generate flux-pro --prompt "<dance hero pose>" --aspect_ratio 9:16 --download /tmp/pose.png

# 2. Animate with the pose as keyframe
comfy generate seedance --image /tmp/pose.png --prompt "dancer flows into this pose then breaks into rapid percussive movement, returns to pose at end, full 360 orbit camera, industrial warehouse setting" --duration 8 --async
```

## Multi-shot music video pipeline
```bash
# Beat 1: Intro WS
comfy generate seedance --prompt "<WS performer in environment, slow zoom in>" --duration 5 --async
# Log job, sweep when done

# Beat 2: Performance MCU
comfy generate seedance --prompt "<MCU performance, same identity, same lighting>" --duration 5 --async

# Beat 3: Cutaway environment
comfy generate seedance --prompt "<environmental cutaway, same color palette>" --duration 3 --async

# Beat 4: Final hero shot
comfy generate seedance --prompt "<hero pose final beat, same identity, dramatic resolution>" --duration 5 --async

# Track all 4 with jobs.py
python3 ~/.claude/skills/comfy-prompt/scripts/jobs.py list
```
