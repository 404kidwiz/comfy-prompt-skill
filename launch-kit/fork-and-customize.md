# Fork & Customize — Make comfy-prompt Yours

How to extend, modify, and adapt the skill to your specific workflow.

## What lives where

```
~/.claude/skills/comfy-prompt/
├── SKILL.md              ← main rules + MCSLA + HARD RULES
├── README.md             ← file map
├── brand.yaml            ← YOUR brand identity (edit this first)
├── model-guide.md        ← model routing decisions
├── vocab.md              ← camera/lighting vocabulary
├── templates/            ← 10 genre templates (action, product, portrait, ...)
├── verticals/            ← 10 business-channel templates
├── styles/               ← 7 reusable Look snippets
├── recipes/              ← 8 shell pipelines
├── scripts/              ← 19 Python helpers (stdlib only)
├── shared/               ← negative constraints
├── mcp_server/           ← MCP stub (deferred)
├── launch-kit/           ← THIS folder — promotional assets
└── CHANGELOG.md          ← version history

~/.claude/commands/comfy/
└── *.md                  ← 20 slash subcommands
```

## 5-Minute Customization Path

### 1. Brand identity (the single highest-leverage change)

Edit `brand.yaml`:

```yaml
name: "Your Brand"
palette: "your specific color words"
mood: "your tone of voice"
lighting: "your lighting register"
camera: "your camera approach"
look_keywords: "your visual signature"
negatives: "what to never include"
preferred_image_model: "flux-pro"  # or whatever fits
output_tag: "your-brand-slug"
```

Now every prompt auto-injects these into the Look line. No more retyping.

### 2. Add a custom recipe

Copy + adapt an existing one:

```bash
cp ~/.claude/skills/comfy-prompt/recipes/instagram-ad.sh \
   ~/.claude/skills/comfy-prompt/recipes/my-custom-flow.sh

# Edit to taste, then expose via cf:
# Edit ~/.local/bin/cf — add `my-flow) cmd_my_flow "$@" ;;` to the dispatch case
```

### 3. Add a custom template

```bash
cat > ~/.claude/skills/comfy-prompt/templates/11-your-genre.md << 'EOF'
# Your Genre Template

## Camera language
- ...

## Look register
- ...

## Action patterns
- ...
EOF

# Then register in scripts/compose.py TEMPLATE_MAP dict
```

### 4. Add a custom style

```bash
cat > ~/.claude/skills/comfy-prompt/styles/your-style.md << 'EOF'
# Your Style

## Quick paste
```
your style descriptor line goes here
```
EOF

# Register in scripts/compose.py STYLE_MAP dict
```

### 5. Add a custom slash subcommand

```bash
cat > ~/.claude/commands/comfy/your-flow.md << 'EOF'
---
description: "Your custom workflow description."
---

**Workflow: Your Flow**

Steps:
1. ...
2. ...

User request: $ARGUMENTS
EOF
```

Restart Claude Code or run `/help`. Now `/comfy:your-flow` works.

---

## Common Customizations

### "I want different cost tiers"

Edit `scripts/jobs.py` → `COST_TIERS` dict at the top. Numbers in USD per generation.

### "I want different aspect ratios in --platform"

Edit `~/.local/bin/cf` → `_platform_flags()` function. Add your platform name + aspect mapping.

### "I want different default models for different recipes"

Edit the recipe `.sh` files. Each uses `comfy generate <model>` calls directly — change the model name.

### "I want to track my own metric (e.g. latency, quality score)"

Add field to `~/.comfy-jobs.json` schema in `scripts/jobs.py`. The registry is just JSON — extend freely.

### "I want different lighting/angle/mood axes for variants"

Edit `scripts/variants.py` → `AXES` dict at top. Each axis is a list of (label, modifier-text) tuples. Add yours.

### "I want a different gallery design"

Edit `scripts/gallery.py` → `HTML_TEMPLATE` constant. Pure CSS, no framework.

### "I want to integrate with X (Slack/Notion/Drive)"

Add a new script in `scripts/`. Use stdlib `urllib.request` for HTTP. Wire into `cf` wrapper.

---

## Contribute Back

Found something useful? Open a PR:

```bash
cd ~/.claude/skills/comfy-prompt/
git checkout -b your-feature
# ... edits ...
git commit -m "Add: your feature"
git push origin your-feature
```

Areas where contributions are most welcome:

- More templates / verticals / styles
- Recipes for specific platforms (Substack, Beehiiv, ConvertKit headers)
- Cross-model prompt translators for newer models
- Better embed.py for video formats (FFmpeg metadata)
- Working MCP server implementation
- More variant axes
- Per-region brand presets

---

## Sharing Your Variant

If you fork and customize for a specific use case (e-comm, podcast, course creator):

1. Document the changes in your fork's README
2. Share the customized `brand.yaml` + custom recipes/templates
3. Tag @dawizkidmal on X / LinkedIn — happy to amplify

The skill is more valuable as a constellation of forks than a single repo.
