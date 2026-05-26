# Before / After — Prompt Comparison Samples

Generate these for the launch carousel. Each pair shows the value of
the skill: weak prompt → strong MCSLA prompt → better output.

## Pair 1 — Portrait

### BEFORE (lazy prompt)
```
a man in a coat, rainy, cyberpunk
```
Generated with: `cf gen flux-pro "a man in a coat, rainy, cyberpunk"`

### AFTER (MCSLA composed via `/comfy:compose`)
```
MCU low angle of a weathered detective in dark wool overcoat, looking off-camera with focused gaze, rain-soaked Tokyo alley background visible behind out-of-focus, neon practical lights bleed into frame from sides, atmospheric haze, lens flares, slight chromatic aberration, anamorphic widescreen letterboxed, heavy 35mm film grain, crushed blacks, bleach-bypass color, muted saturation, photoreal cinematic
```
Generated with:
```bash
cf compose "a weathered detective in dark wool overcoat" \
    --template portrait \
    --style cyberpunk-blade-runner \
    --model flux-pro \
    --aspect 16:9
```

The composed version is 4x longer. Every clause does work. The lint would fail the "before" version on missing camera + weak phrasing.

---

## Pair 2 — Product

### BEFORE
```
matte black coffee mug, professional photo
```

### AFTER
```
MCU static locked-off camera, matte black coffee mug on seamless white background, soft overhead key with even fill, gentle rim from camera-back-left, catalog photography register, ultra-sharp, color-accurate, deep blacks, no environmental clutter, photoreal commercial photography
```
Generated with: `cf gen flux-ultra "<above>" --tag product-test --platform square`

After is auto-organized to `~/Comfy-Output/2026-05/product-test/`, metadata embedded, gallery auto-generated. Before lands somewhere random in `/tmp/`.

---

## Pair 3 — Video

### BEFORE
```
city at night, cool video
```
Linted as:
```
❌ video prompt has no explicit camera vocabulary
❌ no action verb — Action layer weak
❌ weak phrasing: 'cool'
```

### AFTER (passes lint)
```
slow Steadicam push-in over 10 seconds toward neon-drenched Tokyo intersection at 2am, rain reflections rippling on wet pavement, atmospheric haze, headlight streaks dragging in slow motion, holographic billboards strobing softly in distance, condensed steam drifting from a manhole cover in foreground, no people visible
```
Generated with: `cf vid seedance "<above>" --platform wide --duration 10 --async`

Async job auto-logged. `cf jobs pending` shows it. `cf watch --loop` auto-downloads when ready.

---

## Pair 4 — Edit (identity locked)

### BEFORE
```
same person but in profile
```
(no image reference, no identity lock — generates a different face)

### AFTER
```bash
# Add reference to library
cf refs add detective-hero /tmp/hero.png --desc "Detective hero shot" --tags character,client-x

# Edit with identity locked
cf gen flux-kontext "same character as reference, same wardrobe, same hair, same age and features, now in pure profile facing camera-left, identity locked" \
    --image $(cf refs use detective-hero) \
    --tag client-x
```

The reference is now reusable across the entire project. No more hunting for "what was that PNG called?"

---

## Pair 5 — Brand-aware

### BEFORE (no brand context)
```
cf gen flux-pro "hero image for our launch"
```
Generates generic stock-looking output.

### AFTER (brand.yaml configured)
```yaml
# brand.yaml
name: "Nova Coffee Co."
palette: "deep espresso brown, warm cream, matte black accents"
mood: "minimal industrial — warm but no-nonsense"
lighting: "single overhead key, warm fill, deep shadows"
look_keywords: "heavy film grain, crushed blacks, warm shadows, matte finish"
```

```bash
cf gen flux-pro "hero image for our launch"
# → Claude auto-injects palette + mood + lighting + look_keywords into the Look line
```

Every prompt becomes brand-consistent without retyping the brand identity each time.

---

## How to use this doc

1. Generate the "AFTER" examples on your own account (one-time setup, ~$0.30 total)
2. Save the side-by-side comparison as carousel slides
3. Caption each pair with the time/cost saved
4. Final slide: "All of this is the skill. Link in comments."
