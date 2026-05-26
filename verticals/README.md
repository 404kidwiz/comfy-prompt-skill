# Verticals — Business Use-Case Templates

Adapted from [Roman Knox AI Video Generator](https://github.com/rediumvex/ai-video-generator-claude)
(originally for Seedance 2.0 on Higgsfield).

Verticals are **business-channel templates** complementing the genre-based `templates/`
directory:
- `templates/` = shape/style (action, portrait, landscape, scifi, horror, fashion, comedy, music, etc.)
- `verticals/` = channel / business use case (viral hook, SaaS launch, course promo, etc.)

Use both together: pick a vertical for the business context, then borrow language from a
matching template for visual specificity.

---

## The 10 verticals

| # | Vertical | Use for |
|---|----------|---------|
| 01 | [viral-hook](./01-viral-hook.md) | TikTok / Reels / Shorts scroll-stoppers, retention-engineered |
| 02 | [saas-launch](./02-saas-launch.md) | Product launches, software demos, Apple-keynote register |
| 03 | [personal-brand](./03-personal-brand.md) | Founder authority, day-in-the-life, thought leadership |
| 04 | [course-promo](./04-course-promo.md) | Online course trailers, coaching ads, masterclass teasers |
| 05 | [faceless-channel](./05-faceless-channel.md) | YouTube/TikTok without showing face, voiceover-driven |
| 06 | [luxury-aesthetic](./06-luxury-aesthetic.md) | High-end brand video, watches, fashion, fragrance, hospitality |
| 07 | [before-after](./07-before-after.md) | Transformation reveals, makeovers, renovations, glow-ups |
| 08 | [testimonial-story](./08-testimonial-story.md) | Customer wins, case studies, social proof reels |
| 09 | [ai-avatar](./09-ai-avatar.md) | Digital persona, virtual spokesperson, AI presenter |
| 10 | [podcast-visual](./10-podcast-visual.md) | Audio-to-video, audiogram replacement, podcast clips |

---

## Shared resources

| File | Contains |
|------|----------|
| [shared/hooks.md](./shared/hooks.md) | 12 universal hook patterns (pattern interrupt, curiosity, dopamine, primal attention) |
| [shared/sound-design.md](./shared/sound-design.md) | 4-layer sound stack + templates by hook type + platform-specific audio |
| [shared/platform-optimization.md](./shared/platform-optimization.md) | TikTok / Reels / Shorts / Feed / LinkedIn / Twitter specs |

---

## How to combine vertical + template

User asks: "Write a viral TikTok hook for a coffee brand."

Compose:
- **Vertical**: `01-viral-hook` — gives you hook pattern, 9:16 aspect, retention engineering
- **Template**: `02-product` (genre) — gives you product cinematography vocabulary
- **Style**: `styles/anamorphic-1970s.md` (optional Look register) — adds cinematic finish
- **Model**: `seedance` (cloud, audio-capable for hook) or `pika-i2v` (image-to-video from product still)

Output: MCSLA-structured prompt + runnable `comfy generate` command.

---

## Source / credit

Adapted from Roman Knox's open-source skill set:
- Repo: https://github.com/rediumvex/ai-video-generator-claude
- Original target: Seedance 2.0 on higgsfield.ai
- This adaptation: Comfy Cloud (`seedance`, `pika`, `runway-i2v`, `vidu`, `grok-video`)
  + local ComfyUI blueprints (Wan 2.2, LTX-2.3)

All hook patterns, camera language, lighting setups, and sound design preserved verbatim
where universal. Comfy-specific:
- `@material[name]` → `--image <path>` flag
- Model references → Comfy Cloud model names
- Asset limits adjusted per Comfy model
- Every example ends with runnable `comfy generate ...` command

MIT license respected.
