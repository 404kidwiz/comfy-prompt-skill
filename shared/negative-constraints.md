# Comfy Negative Constraints

Pull verbatim. Do not paraphrase. Each model handles negatives differently — many
modern models prefer **positive phrasing** (describe what you want) over negation.

---

## Universal artifact prevention

Append to every cinematic prompt unless overridden:

```
no warped hands, no extra fingers, no duplicate limbs, no morphed faces,
no plastic skin, no oversaturated colors, no overexposed highlights,
no banding artifacts, no aliasing, no chromatic fringing artifacts,
no watermark, no logo overlay, no caption text, no UI elements
```

---

## Face / Identity

For portrait-focused prompts:

```
no asymmetric eyes, no merged irises, no missing eyelashes,
no plasticky skin texture, no waxen sheen, no melted features,
no missing teeth, no extra teeth, no warped jawline
```

---

## Hands / Limbs

For full-body or gesture-focused prompts:

```
no extra fingers, no missing fingers, no warped knuckles, no merged hands,
no extra arms, no extra legs, no duplicated limbs,
no broken joints, no impossible bending
```

---

## Motion / Video

For video prompts:

```
no morphing between frames, no identity drift across the clip,
no jittering background objects, no warping environment, no melting subjects,
no abrupt teleportation, no impossible physics, no popping artifacts
```

---

## Text Rendering

When text is part of the image (use models that handle text well — ideogram, dalle,
nano-banana):

```
no mangled letters, no unreadable typography, no broken kerning,
no extra spurious letters, no rotated/flipped characters
```

For models WEAK at text (most Flux variants except Flux 2 Pro): describe text region as
"text placeholder area, kept blank for post-production" and composite text in editor.

---

## Style-specific

### Photoreal
```
no painterly soft edges, no cartoon stylization, no overly smooth skin
```

### Illustration / concept art
```
no photorealistic textures, no skin pores, no harsh photographic shadows
```

### Anime / manga
```
no 3D rendered look, no photoreal eyes, no real-world skin texture
```

### Product photography
```
no environmental clutter, no busy background, no shadows touching product,
no reflections distorting product label
```

---

## Multi-shot / Identity Consistency

If generating a sequence and identity drift is a known failure:

```
keep same hair color and length across shots,
keep same facial features and skin tone,
keep same clothing color and silhouette
```

(Modern models like seedance + nano-banana handle this well with explicit reminders.)

---

## Aspect / Framing

```
no letterbox bars (unless explicitly requested as anamorphic style),
no black borders, no vignette artifacts at edges (unless requested)
```

---

## Per-model exceptions

| Model | Negative behavior |
|-------|-------------------|
| `flux-pro`, `flux-ultra`, `flux-2` | Prefers positive phrasing. Append negatives sparingly. |
| `stability-sd3`, `stability-ultra` | Accepts explicit negative prompts well. |
| `dalle`, `dalle-edit` | Mostly ignores negatives. Describe desired result positively. |
| `nano-banana` | Accepts negative phrasing but works best with positive descriptions. |
| `seedance` | Accepts both. Video-specific negatives (morphing, drift) matter most. |
| `ideogram` | Strong text handling — append text-specific negatives only. |
| `grok`, `grok-edit`, `grok-video` | Mostly positive phrasing. |
| Local Flux blueprints | Use the negative-prompt node in the workflow if present. |
