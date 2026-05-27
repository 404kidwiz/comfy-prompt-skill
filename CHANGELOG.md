# CHANGELOG — comfy-prompt skill

All notable changes to this skill. Follows Keep a Changelog conventions.

---

## [3.2.0] — 2026-05-26 (premium-first tier system)

### Added
- **`scripts/tiers.py`** — premium-first model tier resolver (S/A/B/C) per task type. Single source of truth for which model to pick. Resolver: `pick(task, quality, budget)`. Supports image, image-edit, image-text, illustration, inpaint, outpaint, video-t2v, video-i2v, upscale, bg-remove, bg-replace, vectorize.
- **`cf auto <task> <prompt>`** — tier-aware top-level command. Auto-routes to S-tier model for the task. Accepts `--quality s|a|b|c` and `--budget`.
- **`cf tiers <task>`** — preview tier resolution without spending. Pass `--budget` or `--quality` to compare.
- **`--quality` and `--budget` flags on all 8 recipes** — character-sheet, storyboard-5shot, mood-board, thumbnail-set, product-3angle, product-lifestyle, instagram-ad, social-pack. Default tier S (premium). `--budget` downshifts S→B globally for the run.
- **`bin/cf`** — `cf` wrapper now ships with the skill. Install: `ln -sf ~/.claude/skills/comfy-prompt/bin/cf ~/.local/bin/cf`.

### Changed
- **`scripts/jobs.py` COST_TIERS** — refreshed with 62 models. New entries: `gemini-3-pro-image-preview` ($0.15), `kling-v1` through `kling-v3` ($0.20–$0.60), `hailuo` ($0.30), `luma`/`luma-i2v` ($0.40–$0.45), `moonvalley-t2v`/`moonvalley-i2v` ($0.40), `ideogram-bg`/`ideogram-reframe`/`ideogram-remix`. Corrected stale prices on `flux-2` ($0.06), `reve` ($0.10), `stability-upscale-creative` ($0.15).
- **`model-guide.md`** — rewritten tier-first. Quick resolution table per task, full inventory tables with tier badges, premium-first decision flow.
- **`SKILL.md`** — Fast Path defaults updated to premium-first. Route-to-model section rebuilt as tier table (S/A/B/C × 12 task types).
- **`README.md`** — install instructions for `cf` symlink, premium-first quick-start examples, tier system explanation.

### Premium defaults (S tier)
- Image → `nano-banana --model gemini-3-pro-image-preview` (Gemini 3 Pro)
- Image-text → `ideogram` (strongest text rendering)
- Image-edit → `flux-kontext-max`
- Video text-to-video → `kling --model_name kling-v3`
- Video image-to-video → `kling-i2v --model_name kling-v3`
- Inpaint/outpaint → `flux-fill` / `flux-expand`
- Upscale → `recraft-upscale-creative`

### Compatibility
- Existing `cf gen <model>`, `cf vid <model>`, all recipe calls without `--quality`/`--budget` still work. Default tier S applies; nothing breaks.

---

## [3.1.0] — 2026-05-26 (production hardening)

### Added
- **`scripts/schema_introspect.py`** — runtime parser for `comfy generate schema <model>` output. Detects aspect-flag family + dimension constraints (e.g. /32 for flux-pro) dynamically. 24h cache. Catches new models automatically.
- **`scripts/models_info.py`** — enriched model catalog: type, cost tier, mode, aspect family, partner. `cf models` now uses this; `cf models --raw` falls back to plain `comfy generate list`.
- **`tests/`** — 38 pytest unit tests + 9 bats integration tests. Mocked `comfy` binary, isolated registries. All pass on first run.
  - `test_aspect_flags.py` (8), `test_lint.py` (6), `test_jobs.py` (4), `test_dedup.py` (5), `test_translate.py` (4), `test_schema_introspect.py` (7), `test_compose.py` (4), `test_recipes.bats` (9)
- **`recipes/_runlib.sh`** — shared `AF()` + `run_step()` helpers + `parse_runlib_flag()` for `--dry-run`.
- **`--dry-run` flag on all 8 recipes** — print pipeline without executing. Bypasses API key check.

### Changed
- `scripts/aspect_flags.py` — now uses runtime schema introspection first, falls back to hardcoded families. `COMFY_NO_INTROSPECT=1` forces fallback path. flux-pro dimensions auto-rounded to multiple-of-32 from detected constraint.
- `scripts/lint.py` — validates aspect against live schema enum (e.g. catches `aspect "21:9"` when `--ratio` enum doesn't include it).
- `~/.local/bin/cf gen` — auto-checks dedup before submit, registers output in dedup index after. `COMFY_NO_DEDUP=1` opts out.
- `~/.local/bin/cf models` — routes through `models_info.py` for enriched table.
- `scripts/schema_cache.py` — fixed argparse bug (subparser + positional conflict). Now `python3 schema_cache.py <model>` works directly.
- All 8 recipes — `COMFY_API_KEY` check gated on `DRY_RUN` so dry-run works offline.

### Removed
- N/A

---

## [3.0.1] — 2026-05-26 (schema-fix patch)

### Fixed — Comfy Cloud CLI schema mismatch
Discovered during launch-kit run: `--aspect_ratio` is NOT universal across Comfy Cloud models. 6 distinct flag conventions exist. Before this patch, recipes failed silently on Flux/Seedance/Pika/Runway/DALL-E/Recraft.

### Added
- **`scripts/aspect_flags.py`** — universal translator: `(model, aspect) → correct CLI flags`. Handles all 6 families: width/height, aspect_ratio, ratio+resolution, ratio enum, size string, pika camelCase float. Falls through to `--aspect_ratio` for unknown models with a stderr warning.

### Changed
- `cf` wrapper: `_platform_flags()` replaced with `_platform_to_aspect()` + `_aspect_flags()`. `cf gen` and `cf vid` now route through aspect_flags.py.
- All 7 recipes: added `AF()` helper, replaced inline `--aspect_ratio X` with `$(AF model X)`.
- `recipes/instagram-ad.sh`: Step 5 (pika-i2v) now passes `--resolution 1080p` instead of (invalid) `--aspect_ratio`.
- `scripts/compare.py` + `scripts/variants.py`: import aspect_flags_for at runtime.
- `launch-kit/hero-promo.sh` + `demo-video.sh`: use `AF()` helper.
- `SKILL.md` HARD RULE #6: rewritten with schema-per-model table + translator-script directive.

### Verified
- Hero generation (`hero-promo.sh`) ran successfully: 1920×1080 PNG via flux-ultra
- Demo video (`demo-video.sh`) ran successfully: 1080p MP4 via seedance with `--ratio 16:9 --resolution 1080p`
- aspect_flags.py tested across 12 models — all return correct schema-matching flags

---

## [3.0.0] — 2026-05-26

Workflow-modular release. Skill now operates as 18 slash subcommands +
`cf` wrapper for shell. 13 new scripts. 4 new recipes. Total: 6,844 → ~11,500 lines.

### Added — slash subcommands (`~/.claude/commands/comfy/`)
- `/comfy:help` — workflow map / index
- `/comfy:image` — single still image generation
- `/comfy:video` — video generation (async + job tracking)
- `/comfy:edit` — image editing (kontext, fill, expand, rmbg)
- `/comfy:upscale` — 4K/8K upscale
- `/comfy:character` — 4-angle character sheet
- `/comfy:storyboard` — 5-shot cinematic
- `/comfy:product` — product workflows (lifestyle / 3-angle / ad)
- `/comfy:social` — TikTok/Reels/Shorts
- `/comfy:brand` — manage brand.yaml
- `/comfy:lint` — prompt validation
- `/comfy:gallery` — HTML output gallery
- `/comfy:budget` — spend summary
- `/comfy:digest` — weekly/monthly usage report
- `/comfy:compose` — template+vertical+style merge
- `/comfy:variants` — N-axis variations
- `/comfy:refs` — reference image library
- `/comfy:init` — scaffold new Comfy project
- `/comfy:dash` — TUI dashboard
- `/comfy:watch` — auto-poll async jobs

### Added — Python scripts (stdlib only)
- `scripts/lint.py` — HARD RULES prompt linter (model verification, MCSLA, word count, vocab check, aspect, red-flag phrases)
- `scripts/gallery.py` — auto-generate browsable HTML gallery from output dir
- `scripts/embed.py` — embed prompt/model/seed/cost into PNG tEXt chunks + sidecar JSON
- `scripts/digest.py` — weekly/monthly usage report with sparkline + keyword analysis
- `scripts/variants.py` — N variations across lighting/angle/mood/palette/season axes
- `scripts/compose.py` — merge template+vertical+style → MCSLA prompt
- `scripts/refs.py` — reference image library (add/list/use/show/rm/tag)
- `scripts/blueprints.py` — scan ~/ComfyUI/blueprints/ with category inference + node analysis
- `scripts/init_project.py` — scaffold project dir with brand.yaml + recipes/ + prompts/ + refs/
- `scripts/dedup.py` — content-hash dedup for repeated prompts
- `scripts/translate.py` — cross-model prompt adaptation (flux ↔ dalle ↔ stability ↔ video)
- `scripts/dash.py` — ANSI TUI dashboard (pending jobs, spend, recent outputs)
- `scripts/watch.py` — auto-poll daemon for async jobs

### Added — recipes
- `recipes/thumbnail-set.sh` — YouTube/social thumbnail set (16:9, 1:1, 4:3, 9:16)
- `recipes/social-pack.sh` — same hero on 4 social backgrounds
- `recipes/product-3angle.sh` — product hero + 3 angles (front/side/back/top)
- `recipes/mood-board.sh` — 9-tile creative mood board

### Added — MCP server stub
- `mcp_server/README.md` — blueprint for future MCP exposure

### Changed — `cf` wrapper extended
- 14 new subcommands: `lint`, `gallery`, `embed`, `digest`, `variants`, `compose`, `refs`, `blueprints`, `init`, `dedup`, `translate`, `dash`, `watch`, `compare`, `brand`, `moodboard`, `thumbnail`, `social`
- `cf gen` now auto-runs lint + embeds metadata
- `cf product {lifestyle|3angle|ad}` sub-router
- `cf help` updated with full surface

---

## [2.0.0] — 2026-05-26 (earlier same day)

### Added (pre-launch batch)
- `/comfy` slash command (parent)
- `cf` wrapper CLI v1
- Cost tracker in `jobs.py` (COST_TIERS, `budget` subcommand)
- `brand.yaml` template
- Failure recovery in all 4 original recipes (`--retry`, `--skip-on-fail`)
- `--platform` shortcut (tiktok/reel/square/wide)
- `COMFY_AUTO_OPEN=1` env var support in `organize.py`
- `scripts/compare.py` multi-model A/B helper
- `comfy generate upload` docs in `comfyui-cli/SKILL.md`
- CHANGELOG.md + LICENSE (MIT)

---

## [1.1.0] — 2026-05-25

### Added (enhancement batch)
- 10 `verticals/` business-channel templates (Roman Knox adaptation)
- 7 `styles/` Look-line snippets
- 4 `recipes/` shell pipelines
- 5 `scripts/` Python helpers
- `hybrid-pipelines.md`, `prompt-examples.md`
- 10 `templates/` genre templates

---

## [1.0.0] — 2026-05-24

### Added (initial release)
- `SKILL.md` — HARD RULES + MCSLA + model routing
- `README.md` — file map
- `model-guide.md` — 30+ cloud + 60+ local blueprints
- `vocab.md` — camera/lighting vocabulary
- `shared/negative-constraints.md`
