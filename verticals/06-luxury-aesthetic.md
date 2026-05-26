# Vertical: Luxury Aesthetic — Chanel-Level Brand Video

Adapted from Roman Knox `seedance-luxury-aesthetic` skill for Comfy.

## When to use
Luxury brand content, premium product showcases, high-end lifestyle, minimalist
aesthetic, sophisticated brand videos, watch / fragrance / fashion / hotel.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Hero brand film (8s, slow, silent or sparse audio) | `seedance` | Cloud, async |
| Product still on dark | `flux-ultra`, `flux-pro` | Cloud, sync |
| Image-to-video micro-orbit | `pika-i2v`, `runway-i2v` | Cloud, async |
| Local repeat iteration | `Image to Video (Wan 2.2).json` | Local |

---

## The Visual Language of Luxury

Luxury reads differently from every other vertical:

| Common content | Luxury content |
|---------------|----------------|
| Fast cuts | Long takes, single sustained shot |
| Loud music | Silence or single mechanical tick |
| Multiple subjects | One subject, vast negative space |
| Camera moves dramatically | Camera moves imperceptibly |
| Color-saturated | Monochromatic or two-tone palette |
| Text overlays | Zero text, brand mark at end only |
| Quick hooks | Slow build, restraint |
| Dynamic action | Stillness, weight, presence |

---

## Hook Patterns for Luxury

### Sustained Silence
```
Black screen. Hold for 1.5-2s of complete silence. Single soft chime or mechanical
tick at 2s, synced to subtle fade-in of product. Product holds in frame perfectly
still. The silence IS the luxury.
```

### Imperceptible Push
```
Open on product in center frame with vast negative space. Camera begins push-in at
imperceptibly slow rate — 10cm of apparent distance over 8 seconds. Light catches
new facets as camera moves. Movement so slow viewer notices only on second watch.
```

### Light Reveal
```
Dark frame, product barely visible. Single soft light source slowly increases over
2s, revealing form. Light source could be candle, window, single LED. Product
emerges from shadow with restraint. No music, only the implied warmth.
```

---

## Visual Style Templates

### Watch / Mechanical Luxury
```
Polished black marble surface. Single hard point light at 45° above-left. Watch
catches one bright specular highlight. Vast dark negative space. Camera locked off
or imperceptible micro-push. Color: warm metallic accents preserved, all other tones
desaturated 75%.
```

### Fragrance / Glassware
```
Faceted glass bottle on dark lacquered surface. Single warm candle light out-of-frame
right creating amber rim. Camera barely-perceptible orbit 8° over 5s. Background
deep near-black. No fill. Liquid catches and releases candlelight as camera moves.
```

### Fashion / Silk
```
Garment hangs from invisible mount, centered, 20% of frame. Remaining 80% warm pale
grey negative space. Camera locked, no movement. Only motion: barely perceptible
thermal drift, fabric swaying 1-2cm over 8s as if in faintest air current. Single
large softbox camera-left wraps the silk.
```

### Architectural / Hotel / Spa
```
WS interior with monumental ceiling. Floor-to-ceiling frosted glass filters uniform
diffused daylight. Single figure in dark structured coat in far middle distance,
occupying 8% of frame height. Camera locked, then imperceptible push-in. Diffused
daylight only, no shadows.
```

---

## Camera: Slow and Deliberate Only

Luxury allows ONE of:
- **Locked off, no movement** — let stillness do the work
- **Imperceptible push-in** — 10-15cm apparent over 5-8s
- **Imperceptible orbit** — 5-10° of arc over 5-8s
- **Single thermal drift** — for fabric / liquid / smoke shots only

NEVER use:
- Whip pan, snap zoom, dutch tilt, drop shot — luxury rejects energy
- Quick cuts — single sustained shot is the discipline
- Hand-held — too documentary, breaks the polish

---

## Lighting Presets

### Single-Source Drama
```
One hard point light positioned 45° above-left. Defined clean shadow falls to lower
right. Subject catches one bright specular highlight. No fill light. Background
absorbs light, falls to pure black. Cinematic chiaroscuro.
```

### Candlelight Simulation
```
1900K color temperature, warm amber dominant. No fill. No cool tones in frame. Subject
lit only by warm side light. Movement of flame implied through subtle light flicker
at 0.3Hz over duration.
```

### Diffused Daylight (architectural)
```
Large frosted glass / softbox source filling one side of frame. 5600K cool daylight
register. Even, enveloping, no harsh shadows. Compressed contrast — luxurious midtones.
```

### Two-Tone Split
```
Subject lit by warm key from one side, cool rim from other. No fill in between.
Subject reads as sculptural — half warm, half cool, single bright form.
```

---

## Color Grading

| Palette | Use |
|---------|-----|
| Black & Gold | Watches, fragrance, luxury auto. Strip all hues except warm metallics. |
| Cream Monochrome | Fashion, silk, beauty. Ivory + warm grey only. |
| Cool Architectural | Hotels, spas, modern luxury. Travertine + pale daylight. |
| Deep Warm | Whiskey, leather, candlelit interiors. Rich amber + deep brown. |

Never: vivid saturation, multiple bright hues, anything trendy-colorful.

---

## Sound Direction

```
Silence is luxury. Use silence for first 1-3s. Single soft mechanical tick, chime,
or breath at 2-3s. Repeat sparsely. No music — or single sustained pad at -18dB
that barely exists. The viewer leans in.
```

For audio-rendering models (`seedance`), describe this explicitly. For silent models
(`pika`, `runway-i2v`), the prompt locks the motion to imaginary audio timing.

---

## Worked Example — Luxury Watch Hero (5s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 5s | Style: Single-Source Luxury

Extremely slow push-in toward a mechanical watch resting on polished black marble
surface. Watch occupies lower center third of frame. Vast dark space above and
around it. Single hard point light positioned 45° from above-left, casting defined
clean shadow to lower right. Watch face catches the light; bezel glints with single
bright specular highlight. Camera begins at 60cm apparent distance and inches
toward 40cm over the full 5 seconds — movement barely perceptible.

Locked composition, no lateral drift. Background: pure deep black, no texture.
Surface: black marble with fine veining, slight reflection of watch visible.

Lighting: single-source drama, warm-cool split, main light at 5500K, rim light at
3200K catching the case edge.

Color grade: cream highlight roll, deep warm shadow, metallic accent preservation —
gold indices fully saturated, all other tones desaturated 75%.

No motion blur. No depth of field effect — watch in full sharp focus front to back.
No camera shake. No text or graphics.

Sound: silence for first 2s. At 2s: single soft mechanical tick. Tick repeats every
1s. No music. The silence IS the luxury.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 5 --async
```

---

## Worked Example — Fashion Silk Editorial (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Negative-Space Editorial

A silk slip dress in ivory hangs from invisible mount, centered in frame, occupying
20% of total frame area. Remaining 80% is warm pale grey — almost white, almost
cream — no texture, no furniture, no background elements. Nothing competes with
the dress.

Camera locked off, static, perfectly still. The only motion: dress moves in
barely perceptible extremely slow thermal drift — fabric swaying 1-2 centimeters
over 8 seconds as if in faintest air current.

Lighting: large format softbox positioned camera-left, wrapping light across silk,
revealing fabric sheen and drape. No hard shadow. No rim light. Single source only.

Lens renders fabric in perfect sharp focus throughout.

Color grade: monochromatic warm palette — ivory, cream, warm grey. No cool tones.
Slight overexposure of highlights (0.3 stops) to push fabric luminosity.

Sound: ASMR close-mic silk movement, no music, room silence.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Luxury vs. Non-Luxury Quick Comparison

| Element | Non-Luxury | Luxury |
|---------|-----------|--------|
| Camera | Whip pan, snap zoom | Imperceptible push, locked off |
| Music | Bass-heavy, energetic | Silence or single sustained pad |
| Cuts | Quick 0.3-0.5s | Single 5-8s sustained shot |
| Text overlay | Bold, frequent | None or single brand mark at end |
| Color | Saturated, multi-hue | Monochromatic or two-tone |
| Subject density | Multiple elements | One subject + vast negative space |
| Lighting | Three-point or dramatic | Single source, often with no fill |
| Pacing | Energetic, building | Restrained, contemplative |
| Voiceover | Confident, present | None |
| Watch time goal | 100% retention | Watch once carefully, rewatch later |

---

## Identity locks for luxury
- ONE shot per video when possible. No multi-cut.
- Camera imperceptibly slow or completely locked off.
- Silence > music. Single tick / chime / breath beats any track.
- One subject + vast negative space.
- Monochromatic or two-tone color only.
- No text overlay except brand mark at final beat.
- The viewer leans in, not the prompt pushing them.
