# comfy-prompt — Production-grade Comfy prompts · v3.2.0

**Premium-first, tier-aware** workflow layer for Comfy Cloud. Single `cf` command-line tool, 8 multi-step recipes, 38 unit tests, tier resolver routing every task to the highest-quality model by default.

Sister skill to `comfyui-cli`. This writes the prompt. `comfyui-cli` runs it.

## What's new in v3.2.0 — premium-first tier system

- **Tier resolver** (`scripts/tiers.py`) — S/A/B/C tier system per task type
- **`cf auto <task>`** — auto-routes to premium model for the task
- **`--budget` flag** — opt-in scale-back from S to B everywhere
- **All 8 recipes updated** — accept `--quality s|a|b|c` and `--budget`
- **Refreshed cost table** — 62 models including gemini-3-pro-image-preview, kling v1-v3, hailuo, luma, moonvalley
- **Premium defaults**:
  - Image → Gemini 3 Pro (`nano-banana --model gemini-3-pro-image-preview`)
  - Image-text → Ideogram
  - Image-edit → Flux Kontext Max
  - Video T2V → Kling v3
  - Video I2V → Kling v3 I2V

Adapted from [Higgsfield AI prompt skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
with all models remapped to Comfy Cloud + local ComfyUI blueprints.

## Install

```bash
# Symlink cf wrapper into PATH
ln -sf ~/.claude/skills/comfy-prompt/bin/cf ~/.local/bin/cf

# Set API key
export COMFY_API_KEY=comfyui-...     # get one at platform.comfy.org/api-keys

# Verify
cf help
cf models                            # list all 50+ cloud models
cf tiers image                       # preview tier resolution for "image" task
```

## File map

```
comfy-prompt/
├── SKILL.md                            ← Main routing + HARD RULES + MCSLA
├── README.md                           ← This file
│
├── model-guide.md                      ← 30+ cloud models + 60+ local blueprints, costs, modes
├── vocab.md                            ← Camera presets, angles, lighting, motion physics
├── prompt-examples.md                  ← Worked examples + before/after improvements
├── hybrid-pipelines.md                 ← Cloud + local stacking patterns
│
├── templates/                          ← 10 genre templates (shape / style)
│   ├── 01-action.md                    ← Chase, pursuit, parkour
│   ├── 02-product.md                   ← Product, commercial, UGC
│   ├── 03-portrait.md                  ← Character, headshot, identity
│   ├── 04-landscape.md                 ← Wide, environment, establishing
│   ├── 05-scifi.md                     ← Cyberpunk, VFX, mecha
│   ├── 06-cinematic-still.md           ← Shot framing formula
│   ├── 07-horror.md                    ← Dread, slasher, cosmic, body
│   ├── 08-fashion.md                   ← Editorial, lookbook, runway
│   ├── 09-comedy.md                    ← TikTok skit, reaction, meme
│   └── 10-music-performance.md         ← Dance, concert, music video
│
├── verticals/                          ← 10 business-channel templates (adapted from Roman Knox)
│   ├── README.md
│   ├── shared/
│   │   ├── hooks.md                    ← 12 universal hook patterns
│   │   ├── sound-design.md             ← 4-layer sound stack
│   │   └── platform-optimization.md    ← TikTok / Reels / Shorts / LinkedIn
│   ├── 01-viral-hook.md
│   ├── 02-saas-launch.md
│   ├── 03-personal-brand.md
│   ├── 04-course-promo.md
│   ├── 05-faceless-channel.md
│   ├── 06-luxury-aesthetic.md
│   ├── 07-before-after.md
│   ├── 08-testimonial-story.md
│   ├── 09-ai-avatar.md
│   └── 10-podcast-visual.md
│
├── styles/                             ← 7 reusable Look-line snippets
│   ├── anamorphic-1970s.md
│   ├── studio-ghibli.md
│   ├── cyberpunk-blade-runner.md
│   ├── film-noir.md
│   ├── pixar-3d.md
│   ├── editorial-vogue.md
│   └── concept-art-painted.md
│
├── recipes/                            ← Multi-step shell pipelines
│   ├── README.md
│   ├── instagram-ad.sh                 ← product → cutout → BG → 4K → animate
│   ├── character-sheet.sh              ← hero + 3 angles, identity locked
│   ├── storyboard-5shot.sh             ← 5-shot cinematic sequence
│   └── product-lifestyle.sh            ← product × 4 lifestyle scenes
│
├── scripts/                            ← Python helpers (stdlib only)
│   ├── parameterize.py                 ← swap prompt/seed/dims in workflow JSON
│   ├── jobs.py                         ← async cloud job tracker
│   ├── preflight.py                    ← validate BEFORE spending credits
│   ├── organize.py                     ← dated output organizer
│   └── schema_cache.py                 ← 24h schema cache
│
└── shared/
    └── negative-constraints.md         ← negative-prompt phrases by category
```

## Quick start

```bash
# Premium auto-routing (default: S tier = Gemini 3 Pro)
cf auto image "matte black coffee mug on wooden counter, golden hour"

# Premium video (default: kling-v3)
cf auto video-t2v "drone shot over Tokyo at night, neon reflections"

# Budget mode (downshift S→B everywhere in one shot)
cf auto image "draft concept" --budget

# Override tier explicitly
cf auto image "..." --quality a            # Force A tier (flux-ultra)
cf auto image "..." --quality b            # Force B tier (flux-pro)

# Preview routing without spending
cf tiers image                             # → nano-banana
cf tiers image --quality b                 # → flux-pro
cf tiers video-t2v                         # → kling --model_name kling-v3

# Recipes — multi-step pipelines (all accept --quality and --budget)
cf character "weathered space pilot in his late 30s"
cf storyboard "lone bounty hunter" "Tokyo neon alley" "Blade Runner anamorphic"
cf product 3angle "matte black coffee mug"
cf product lifestyle "matte black coffee mug" --platform reel
cf social hero.png "Nova Coffee"
cf moodboard "cyberpunk neon detective in rain"
cf thumbnail "AI agents replacing devs" "shocked face, bold red title"

# Budget on a recipe
cf character "test character" --budget     # all 4 angles use B tier

# Manual model invocation (explicit)
cf gen flux-ultra "cinematic hero shot" --platform wide
cf vid seedance "drone shot at night" --platform tiktok --async
```

## How Claude uses this skill

When the user asks for:
- "Write a prompt for X" → read SKILL.md → match template/style → compose MCSLA → output prompt + runnable command
- "Generate X for me" → above + actually run the command via `comfyui-cli`
- "Use Y model" → verify in `model-guide.md` first
- "Make it cyberpunk / 1970s / Ghibli" → grab the matching `styles/` snippet
- "Run the full pipeline" → use a `recipes/` script
- "Multi-step image work" → see `hybrid-pipelines.md`

Always:
1. Apply the HARD RULES checklist from `SKILL.md`
2. Pull negative constraints from `shared/negative-constraints.md`
3. End with the exact `comfy generate ...` or `comfy run --workflow ...` command
4. Use the scripts — don't hand-paste paths or lose async job_ids
