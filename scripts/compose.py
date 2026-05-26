#!/usr/bin/env python3
"""
compose.py — Merge template + vertical + style snippets into one MCSLA prompt.

Killer feature: given a user-supplied subject/action, compose a complete prompt
by stacking three layers from the skill's templates/, verticals/, and styles/.

Usage:
  python3 compose.py "matte black coffee mug" \\
      --template product \\
      --vertical viral-hook \\
      --style cyberpunk-blade-runner \\
      --model flux-pro \\
      --aspect 9:16

  # Just print the composed prompt (don't generate)
  python3 compose.py "subject" --template portrait --style film-noir --print-only

  # List available templates/verticals/styles
  python3 compose.py --list

Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".claude" / "skills" / "comfy-prompt"
TEMPLATES_DIR = SKILL_DIR / "templates"
VERTICALS_DIR = SKILL_DIR / "verticals"
STYLES_DIR = SKILL_DIR / "styles"

# Template ID → file mapping
TEMPLATE_MAP = {
    "action": "01-action.md",
    "product": "02-product.md",
    "portrait": "03-portrait.md",
    "landscape": "04-landscape.md",
    "scifi": "05-scifi.md",
    "cinematic": "06-cinematic-still.md",
    "horror": "07-horror.md",
    "fashion": "08-fashion.md",
    "comedy": "09-comedy.md",
    "music": "10-music-performance.md",
}

VERTICAL_MAP = {
    "viral-hook": "01-viral-hook.md",
    "saas-launch": "02-saas-launch.md",
    "personal-brand": "03-personal-brand.md",
    "course-promo": "04-course-promo.md",
    "faceless-channel": "05-faceless-channel.md",
    "luxury-aesthetic": "06-luxury-aesthetic.md",
    "before-after": "07-before-after.md",
    "testimonial-story": "08-testimonial-story.md",
    "ai-avatar": "09-ai-avatar.md",
    "podcast-visual": "10-podcast-visual.md",
}

STYLE_MAP = {
    "anamorphic-1970s": "anamorphic-1970s.md",
    "studio-ghibli": "studio-ghibli.md",
    "cyberpunk-blade-runner": "cyberpunk-blade-runner.md",
    "film-noir": "film-noir.md",
    "pixar-3d": "pixar-3d.md",
    "editorial-vogue": "editorial-vogue.md",
    "concept-art-painted": "concept-art-painted.md",
}


def extract_quick_paste(text: str) -> str:
    """Extract the 'Quick paste' block from a snippet file."""
    # Look for a code fence right after 'Quick paste' marker
    m = re.search(r"##?#?\s*Quick paste\s*\n+```\s*\n([\s\S]+?)\n```", text)
    if m:
        return m.group(1).strip()
    return ""


def extract_style_line(text: str) -> str:
    """Extract a 'Style:' line if Quick paste not found."""
    m = re.search(r"^Style:\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def extract_camera_lines(text: str) -> list[str]:
    """Pull lines mentioning camera presets / framing from a template."""
    lines = []
    for line in text.splitlines():
        if any(t in line.lower() for t in ["ecu", "mcu", "ms ", "ws ", "ews",
                                            "low angle", "dutch angle", "dolly",
                                            "pan", "tilt", "tracking", "rack focus"]):
            cleaned = line.strip().lstrip("-*").strip()
            if 5 < len(cleaned) < 200:
                lines.append(cleaned)
    return lines[:3]


def extract_hook_block(text: str) -> str:
    """Pull a hook pattern block from a vertical."""
    # Find first ``` fenced block in the file
    m = re.search(r"```\s*\n([\s\S]+?)\n```", text)
    if m:
        return m.group(1).strip()
    return ""


def load_file(path: Path) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text()
    except OSError:
        return ""


def compose_prompt(subject: str,
                   template_id: str | None,
                   vertical_id: str | None,
                   style_id: str | None,
                   action: str | None = None) -> dict[str, str]:
    """
    Compose an MCSLA prompt by stacking template + vertical + style.

    Returns a dict with keys: subject, camera, look, action, hook_pattern, full
    """
    result = {
        "subject": subject,
        "camera": "",
        "look": "",
        "action": action or "",
        "hook_pattern": "",
        "full": "",
    }

    # Layer 1: TEMPLATE → contributes camera and framing
    if template_id:
        if template_id not in TEMPLATE_MAP:
            print(f"unknown template: {template_id}", file=sys.stderr)
            return result
        tpl = load_file(TEMPLATES_DIR / TEMPLATE_MAP[template_id])
        camera_lines = extract_camera_lines(tpl)
        if camera_lines:
            result["camera"] = camera_lines[0]

    # Layer 2: VERTICAL → contributes hook + business framing
    if vertical_id:
        if vertical_id not in VERTICAL_MAP:
            print(f"unknown vertical: {vertical_id}", file=sys.stderr)
            return result
        vert = load_file(VERTICALS_DIR / VERTICAL_MAP[vertical_id])
        hook = extract_hook_block(vert)
        if hook:
            # Take first 2 sentences
            sentences = re.split(r"(?<=[.!?])\s+", hook)
            result["hook_pattern"] = " ".join(sentences[:2])[:300]

    # Layer 3: STYLE → contributes look / register
    if style_id:
        if style_id not in STYLE_MAP:
            print(f"unknown style: {style_id}", file=sys.stderr)
            return result
        style = load_file(STYLES_DIR / STYLE_MAP[style_id])
        qp = extract_quick_paste(style)
        if not qp:
            qp = extract_style_line(style)
        result["look"] = qp

    # Compose MCSLA-shaped prompt
    parts = []
    if result["camera"]:
        parts.append(result["camera"])
    parts.append(f"of {subject}")
    if result["action"]:
        parts.append(result["action"])
    if result["look"]:
        parts.append(result["look"])

    result["full"] = ", ".join(parts)
    return result


def list_options() -> None:
    print("Templates:")
    for k in TEMPLATE_MAP:
        print(f"  {k}")
    print("\nVerticals:")
    for k in VERTICAL_MAP:
        print(f"  {k}")
    print("\nStyles:")
    for k in STYLE_MAP:
        print(f"  {k}")


def main() -> int:
    p = argparse.ArgumentParser(description="Compose MCSLA prompt from template + vertical + style")
    p.add_argument("subject", nargs="?", help="Subject of the prompt")
    p.add_argument("--template", help="Template ID (use --list to see options)")
    p.add_argument("--vertical", help="Vertical ID")
    p.add_argument("--style", help="Style ID")
    p.add_argument("--action", help="Custom action verb / motion description")
    p.add_argument("--model", default="flux-pro", help="Target model")
    p.add_argument("--aspect", default="16:9", help="Aspect ratio")
    p.add_argument("--tag", default="composed", help="Output tag")
    p.add_argument("--list", action="store_true", help="List available options")
    p.add_argument("--print-only", action="store_true",
                   help="Print composed prompt, don't show comfy command")
    args = p.parse_args()

    if args.list:
        list_options()
        return 0

    if not args.subject:
        print("error: subject required (or use --list)", file=sys.stderr)
        return 1

    composed = compose_prompt(args.subject, args.template, args.vertical,
                               args.style, args.action)

    print("━━━ Composed Prompt ━━━")
    print()
    if composed["camera"]:
        print(f"**Camera**: {composed['camera']}")
    print(f"**Subject**: {composed['subject']}")
    if composed["action"]:
        print(f"**Action**: {composed['action']}")
    if composed["look"]:
        print(f"**Look**: {composed['look']}")
    if composed["hook_pattern"]:
        print(f"\n**Vertical hook pattern**:")
        print(composed["hook_pattern"])
    print()
    print("━━━ MCSLA Composed ━━━")
    print(composed["full"])
    print()

    if not args.print_only:
        print("━━━ Run ━━━")
        print(f'comfy generate {args.model} \\')
        print(f'    --prompt "{composed["full"]}" \\')
        print(f'    --aspect_ratio {args.aspect} \\')
        print(f'    --download "$(python3 ~/.claude/skills/comfy-prompt/scripts/organize.py path '
              f'--model {args.model} --tag {args.tag} | head -1)"')

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
