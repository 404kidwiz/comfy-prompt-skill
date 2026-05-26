#!/usr/bin/env python3
"""
init_project.py — Scaffold a new Comfy project directory.

Creates:
  <project>/
  ├── brand.yaml            (template from skill, ready to edit)
  ├── recipes/              (project-specific recipe shortcuts)
  │   └── _README.md
  ├── prompts/              (saved prompts as .txt files)
  │   └── _README.md
  ├── refs/                 (project-local reference images)
  │   └── _README.md
  ├── outputs/              (gitignored output dir override)
  │   └── .gitkeep
  ├── .gitignore
  ├── README.md
  └── COMFY.md              (project context for Claude)

Usage:
  python3 init_project.py <project_dir> --name "Nova Coffee" [--brand-style "minimal industrial"]
  python3 init_project.py ~/projects/nova-launch --name "Nova Launch"

Stdlib only.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path.home() / ".claude" / "skills" / "comfy-prompt"

README_TEMPLATE = """# {name}

Comfy project — generated assets, prompts, and brand config.

## Structure

- `brand.yaml` — brand identity. Tells Claude how to compose MCSLA prompts.
- `recipes/` — project-specific shell recipes (drop-in custom pipelines)
- `prompts/` — saved/versioned prompt text files
- `refs/` — reference images for this project
- `outputs/` — generated assets (gitignored)

## Workflow

```bash
# Set output root to this project
export COMFY_OUTPUT_ROOT="$PWD/outputs"
export COMFY_API_KEY=comfyui-...

# Compose a prompt using project brand
cf gen flux-pro "$(< prompts/hero.txt)" --tag {name_slug}

# Or run a project recipe
./recipes/launch-hero.sh
```

## Adding a reference image

```bash
cf refs add {name_slug}-hero ./refs/hero.png --desc "{name} hero reference" --tags brand,{name_slug}
```

Then in any prompt:
```bash
cf gen flux-kontext "tagline" --image $(cf refs use {name_slug}-hero)
```

Generated {date}.
"""

CLAUDE_CONTEXT = """# COMFY.md — Project context for Claude

When working in this project, Claude should:

1. Read `brand.yaml` first — it has all the visual identity rules.
2. Use `cf` wrapper for all generation (don't hand-write `comfy generate`).
3. Save useful prompts to `prompts/` as `.txt` files (one per use case).
4. Add reference images via `cf refs add` so they're reusable.
5. Default `--tag` to `{name_slug}` so outputs organize cleanly.
6. Generated assets land in `outputs/` (gitignored).

## Project-specific recipes

If a standard recipe doesn't fit, add a custom one to `recipes/` based on
templates in `~/.claude/skills/comfy-prompt/recipes/`.

## Brand summary

(Filled in from brand.yaml when known.)

- Name: {name}
- Style: {style}
"""

GITIGNORE = """# Generated outputs
outputs/
*.png
*.jpg
*.webp
*.mp4
*.webm

# Comfy metadata sidecars
*.png.json
*.mp4.json

# Local secrets
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Allow refs/ images explicitly (not generated)
!refs/*.png
!refs/*.jpg
!refs/*.webp
"""

RECIPES_README = """# Project recipes

Drop custom shell recipes here. Use the standard recipes in
`~/.claude/skills/comfy-prompt/recipes/` as templates.

Example: copy and adapt for project-specific cinematography:
```bash
cp ~/.claude/skills/comfy-prompt/recipes/instagram-ad.sh ./launch-hero.sh
chmod +x launch-hero.sh
```
"""

PROMPTS_README = """# Saved prompts

One prompt per `.txt` file. Use descriptive filenames:
  - hero-launch.txt
  - product-detail.txt
  - founder-portrait.txt

To use:
```bash
cf gen flux-pro "$(< prompts/hero-launch.txt)" --tag project-tag
```
"""

REFS_README = """# Project reference images

Put brand references, character references, style references here. Add them
to the global refs library with:

```bash
cf refs add <slug> ./refs/<image> --desc "..." --tags <tags>
```

Then use globally:
```bash
cf gen flux-kontext "prompt" --image $(cf refs use <slug>)
```
"""


def slugify(name: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-"
                   for c in name).strip("-").replace("--", "-")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold a Comfy project directory")
    p.add_argument("path", type=Path, help="Project directory to create")
    p.add_argument("--name", required=True, help="Display name (e.g. 'Nova Coffee')")
    p.add_argument("--brand-style", default="", help="Brand style description")
    p.add_argument("--force", action="store_true", help="Overwrite existing dir")
    args = p.parse_args()

    target = args.path.expanduser().resolve()

    if target.exists():
        if not args.force:
            print(f"error: {target} exists. Use --force to overwrite.", file=sys.stderr)
            return 1

    name_slug = slugify(args.name)
    date = datetime.now().strftime("%Y-%m-%d")

    # Create structure
    target.mkdir(parents=True, exist_ok=True)
    (target / "recipes").mkdir(exist_ok=True)
    (target / "prompts").mkdir(exist_ok=True)
    (target / "refs").mkdir(exist_ok=True)
    (target / "outputs").mkdir(exist_ok=True)

    # Files
    brand_template = SKILL_DIR / "brand.yaml"
    if brand_template.is_file():
        shutil.copy2(brand_template, target / "brand.yaml")
    else:
        write_text(target / "brand.yaml", f'name: "{args.name}"\nstyle: "{args.brand_style}"\n')

    write_text(target / "README.md",
                README_TEMPLATE.format(name=args.name, name_slug=name_slug, date=date))
    write_text(target / "COMFY.md",
                CLAUDE_CONTEXT.format(name=args.name, name_slug=name_slug,
                                       style=args.brand_style or "(set in brand.yaml)"))
    write_text(target / ".gitignore", GITIGNORE)
    write_text(target / "recipes" / "_README.md", RECIPES_README)
    write_text(target / "prompts" / "_README.md", PROMPTS_README)
    write_text(target / "refs" / "_README.md", REFS_README)
    write_text(target / "outputs" / ".gitkeep", "")

    print(f"✅ Project initialized: {target}")
    print(f"   Name: {args.name}")
    print(f"   Slug: {name_slug}")
    print(f"")
    print(f"Next steps:")
    print(f"  cd {target}")
    print(f"  $EDITOR brand.yaml         # fill in brand identity")
    print(f"  cf gen flux-pro 'test prompt' --tag {name_slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
