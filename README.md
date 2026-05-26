# comfy-prompt — Production-grade Comfy prompts

Sister skill to `comfyui-cli`. This writes the prompt. `comfyui-cli` runs it.

Adapted from [Higgsfield AI prompt skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
with all models remapped to Comfy Cloud + local ComfyUI blueprints.

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
# Set API key (one-time)
export COMFY_API_KEY=comfyui-...

# Try a recipe
~/.claude/skills/comfy-prompt/recipes/instagram-ad.sh "matte black coffee mug" "sunlit kitchen, plants"

# Or a manual workflow
python3 ~/.claude/skills/comfy-prompt/scripts/preflight.py flux-pro --download /tmp/out.png
OUT=$(python3 ~/.claude/skills/comfy-prompt/scripts/organize.py path --model flux-pro --tag tests)
comfy generate flux-pro --prompt "..." --download "$OUT"
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
