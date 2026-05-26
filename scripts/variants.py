#!/usr/bin/env python3
"""
variants.py — Auto-generate N variations of one prompt across an axis.

Given a base prompt, mutate it across:
  - lighting: 4 setups (warm-window, hard-side-key, golden-hour, blue-hour)
  - angle:    5 framings (ECU, MCU, MS, WS, EWS)
  - mood:     4 tones (intimate, dramatic, documentary, ethereal)
  - palette:  4 color registers (warm-amber, cool-cyan, monochrome, sunset)
  - season:   4 seasons (spring/summer/fall/winter)

Usage:
  python3 variants.py "base prompt" --axis lighting --model flux-pro [--exec]
  python3 variants.py "base prompt" --axis angle --tag client-x --exec
  python3 variants.py "base prompt" --axis mood --aspect 9:16

Output:
  By default — prints the N variant prompts + ready-to-paste comfy commands.
  With --exec — runs each generation, saves to organized output dir.

Stdlib only.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AXES: dict[str, list[tuple[str, str]]] = {
    "lighting": [
        ("warm-window",
         "soft warm window light from camera-right, golden tones, "
         "natural shadow fall-off, documentary register"),
        ("hard-side-key",
         "single hard side-key from camera-right with deep chiaroscuro shadow on "
         "opposite half, dramatic falloff, cinematic"),
        ("golden-hour",
         "golden-hour sunset light, long warm shadows, soft rim light from behind, "
         "amber atmosphere"),
        ("blue-hour",
         "blue-hour twilight, cool ambient light, neon practicals as fill, "
         "moody atmospheric haze"),
    ],
    "angle": [
        ("ecu", "ECU extreme close-up, intimate framing, eyes filling frame"),
        ("mcu", "MCU medium close-up, eye level, shallow depth of field"),
        ("ms",  "MS medium shot, waist-up, environmental context visible behind"),
        ("ws",  "WS wide shot, full body, environment dominant, deep focus"),
        ("ews", "EWS extreme wide shot, character small in vast environment, cinematic scale"),
    ],
    "mood": [
        ("intimate",     "intimate quiet tone, soft warm lighting, gentle expression, "
                          "personal register, close framing"),
        ("dramatic",     "dramatic tense register, hard chiaroscuro, intense expression, "
                          "high contrast, cinematic gravity"),
        ("documentary",  "documentary observational register, natural light, candid "
                          "expression, untreated authentic feel"),
        ("ethereal",     "ethereal dreamlike register, soft diffused light, surreal "
                          "atmosphere, otherworldly tones, slight glow"),
    ],
    "palette": [
        ("warm-amber",   "warm amber and cream color palette, golden tones, soft warm shadows"),
        ("cool-cyan",    "cool cyan and steel-blue palette, desaturated, slight teal cast"),
        ("monochrome",   "monochromatic black and white, high contrast, rich grays, no color"),
        ("sunset",       "sunset palette of magenta, orange and deep purple, vibrant warmth"),
    ],
    "season": [
        ("spring", "spring season, fresh green foliage, soft pastels, blossoms, gentle warm light"),
        ("summer", "summer season, lush vibrant green, harsh midday sun, vivid colors, heat haze"),
        ("fall",   "fall season, amber and rust foliage, soft overcast light, melancholic warmth"),
        ("winter", "winter season, bare branches, cool blue cast, soft snow light, crisp atmosphere"),
    ],
}


def render_variant(base: str, axis: str, label: str, modifier: str) -> str:
    """Compose base prompt + axis-specific modifier."""
    return f"{base.rstrip('.,')}, {modifier}"


def run_one(model: str, prompt: str, out_path: Path, aspect: str) -> int:
    cmd = ["comfy", "generate", model, "--prompt", prompt]
    # Translate aspect → model-specific flags
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from aspect_flags import aspect_flags_for
        cmd += aspect_flags_for(model, aspect)
    except ImportError:
        cmd += ["--aspect_ratio", aspect]
    cmd += ["--download", str(out_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"  ✓ {out_path.name}")
            return 0
        print(f"  ✗ {out_path.name} — {result.stderr.strip()[:120]}", file=sys.stderr)
        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"  ✗ {out_path.name} — timed out", file=sys.stderr)
        return 1


def main() -> int:
    p = argparse.ArgumentParser(description="Generate variations of one prompt across an axis")
    p.add_argument("prompt", help="Base prompt")
    p.add_argument("--axis", required=True, choices=list(AXES.keys()),
                   help="Variation axis")
    p.add_argument("--model", default="flux-pro", help="Target model")
    p.add_argument("--aspect", default="1:1", help="Aspect ratio")
    p.add_argument("--tag", default="variants", help="Output tag")
    p.add_argument("--exec", action="store_true",
                   help="Actually run the generations (default: just print prompts)")
    p.add_argument("--limit", type=int, help="Only generate first N variants")
    args = p.parse_args()

    axis_variants = AXES[args.axis]
    if args.limit:
        axis_variants = axis_variants[:args.limit]

    print(f"━━━ Variants on axis '{args.axis}' ━━━")
    print(f"Base prompt: {args.prompt}")
    print(f"Model: {args.model}  •  Aspect: {args.aspect}")
    print()

    # Build output dir
    ts = datetime.now().strftime("%H%M%S")
    out_dir = (Path.home() / "Comfy-Output" /
               datetime.now().strftime("%Y-%m") /
               args.tag / f"variants_{args.axis}_{ts}")
    if args.exec:
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output: {out_dir}\n")

    failures = 0
    for label, modifier in axis_variants:
        variant_prompt = render_variant(args.prompt, args.axis, label, modifier)
        out_path = out_dir / f"{args.axis}_{label}.png"

        if args.exec:
            print(f"▶ {label}: {variant_prompt[:80]}...")
            rc = run_one(args.model, variant_prompt, out_path, args.aspect)
            if rc != 0:
                failures += 1
        else:
            print(f"## Variant: {label}")
            print(f'comfy generate {args.model} \\')
            print(f'    --prompt "{variant_prompt}" \\')
            print(f'    --aspect_ratio {args.aspect} \\')
            print(f'    --download "{out_path}"')
            print()

    if args.exec:
        print()
        if failures:
            print(f"⚠  {failures}/{len(axis_variants)} variants failed")
            return 1
        print(f"✅ {len(axis_variants)} variants in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
