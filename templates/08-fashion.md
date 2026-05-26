# Template: Fashion / Editorial / Lookbook

## Genre / Use case
Fashion photography, editorial covers, runway, lookbook stills, brand campaign imagery,
streetwear, couture, jewelry / accessory hero shots.

## When to use
User asks for fashion, editorial, Vogue / Harper's-style, lookbook, runway, magazine
cover, couture, streetwear hero, model shot, brand campaign.

## Recommended models
- **High fashion editorial**: `flux-pro`, `flux-ultra`, `stability-sd3`.
- **Versatile commercial**: `nano-banana`, `recraft`.
- **Strong text rendering (cover lines)**: `ideogram`.
- **Video walk / runway**: `seedance`, `runway-i2v`.

## Example prompt — `flux-pro` (editorial cover)

```
Model: flux-pro (cloud)
Aspect: 3:4 | Style: Editorial Vogue

Full-body LS Eye Level of a woman in flowing silver couture gown.
Standing motionless against a blank concrete wall.
Pose: arms loose at sides, weight on one hip, gaze directly into camera, lips slightly parted.
Hair: jet-black bob, sharp blunt cut, glossy.
Lighting: single overhead diffused softbox, soft fill from below, no shadows on face.
Background: cool gray seamless. No environmental clutter.
Style: Vogue editorial. High-contrast monochrome with single silver accent.
Magazine cover composition — negative space top-third for masthead.
Skin photoreal, no airbrushed plasticity.

Run:
comfy generate flux-pro --prompt "full-body LS eye level of woman in flowing silver couture gown standing motionless against blank concrete wall, arms loose at sides weight on one hip gaze directly into camera lips slightly parted, jet-black sharp blunt bob glossy, single overhead diffused softbox with soft fill from below no shadows on face, cool gray seamless background no clutter, Vogue editorial high-contrast monochrome with single silver accent, magazine cover composition negative space top-third for masthead, skin photoreal no airbrushed plasticity" --aspect_ratio 3:4 --download /tmp/editorial_{index}.{ext}
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "flowing silver couture gown" | Specific garment + material |
| "Standing motionless against a blank concrete wall" | Pose specificity + clean background |
| "arms loose at sides, weight on one hip" | Exact pose direction |
| "gaze directly into camera, lips slightly parted" | Emotional register specific |
| "single overhead diffused softbox, soft fill from below" | Beauty-dish lighting setup named |
| "negative space top-third for masthead" | Compositional rule for cover usage |
| "skin photoreal, no airbrushed plasticity" | Anti-failure for editorial register |

## Negative constraints
Pull face + universal + fashion-specific:
```
no overly airbrushed skin, no waxy plastic complexion, no over-smoothed pores,
no warped fabric drape, no impossible body proportions, no extra limbs,
no logo on garment unless explicitly described, no branded text
```

## Common mistakes
1. **"Beautiful model"** — Style slop. Describe specific features: hair cut, skin tone, age, demeanor.
2. **Over-detailed garment** — Three adjectives max. "Silver couture gown" beats "long flowing iridescent metallic silver A-line halter couture gown with beading".
3. **Busy background** — Editorial usually = clean seamless. If you want context, name a specific location with cinematic register.
4. **Generic lighting** — "Studio lighting" is meaningless. Name softbox direction, fill ratio.
5. **Plastic skin** — Modern image models default to over-smoothed. Always add "photoreal skin texture, visible pores, no airbrushing".

## Variations

### Streetwear hero — `nano-banana`
```
Model: nano-banana (cloud)
Aspect: 4:5 | Style: Streetwear Editorial

MS Eye Level of a young man in oversized matte-black puffer jacket, baggy cargo pants,
clean white sneakers.
Pose: hands in pockets, leaning against rusted shipping container.
Lighting: overcast natural daylight, soft and diffused, no harsh shadows.
Background: industrial loading dock, soft blur, single graffiti tag visible.
Style: Supreme/Off-White editorial. Cinematic muted color grade.
Slight grain. Wide-format 4:5.
```

### Runway video — `seedance`
```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s

Vertical full-body of a model walking the runway in flowing tangerine gown.
Camera: locked off eye-level, model walks directly toward camera.
[0-5s] Distant LS, model takes 4 strides toward camera.
[5-8s] Camera holds — she reaches MS framing, pauses, holds gaze.
[8-10s] She turns 180°, walks back, gown trailing.
Style: Paris fashion week. Sharp focus on model, background soft blur.
Cold white runway lighting, single spotlight overhead.
Slight slow motion on each step.
```

### Jewelry / accessory hero — `flux-ultra`
```
Model: flux-ultra (cloud)
Aspect: 1:1 | Style: Luxury Product

ECU Macro Rack Focus of a diamond solitaire ring on black velvet.
Single dewdrop of water beaded on velvet beside ring.
Lighting: ringlight from camera direction, single sharp accent from upper-right
to catch ring's primary facet.
Background: deep black velvet, no other objects.
Style: Tiffany / Cartier luxury product. Ultra-sharp focus on stone,
silky bokeh on velvet texture. Color-accurate.
```

### Concept fashion (avant-garde) — `stability-sd3`
```
Model: stability-sd3 (cloud)
Aspect: 9:16 | Style: Avant-Garde Concept

Vertical full-body of a model in an architectural pleated gown — origami folds in
matte white, asymmetric collar rising past the head like a sail.
Posed against curved white architectural backdrop, perfect symmetry.
Lighting: hard direct overhead with single shadow casting downward from collar.
Style: Iris van Herpen / Comme des Garçons. Concept fashion editorial.
Painted matte register, slight desaturation, dramatic geometry.
```

## Multi-shot lookbook
```bash
# Generate 6 looks with consistent style register
for i in 1 2 3 4 5 6; do
  comfy generate flux-pro \
    --prompt "full-body LS editorial fashion look $i: <describe look here>, same lighting setup as previous, same gray seamless background, Vogue editorial style, photoreal skin" \
    --aspect_ratio 3:4 \
    --download /tmp/look_${i}.png
done

# Composite into lookbook grid in post (Photoshop / ffmpeg / imagemagick)
```
