#!/usr/bin/env python3
"""
models_info.py — Enriched model catalog with capabilities, cost, mode.

Combines:
  - `comfy generate list` (live model availability)
  - Hardcoded cost tiers (from jobs.py COST_TIERS)
  - Runtime schema introspection (aspect family, async/sync, output format)

Usage:
  python3 models_info.py                # full table
  python3 models_info.py --type video   # filter
  python3 models_info.py --type image
  python3 models_info.py --json         # machine-readable
  python3 models_info.py <model>        # one model detail

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from jobs import COST_TIERS, DEFAULT_COST
except ImportError:
    COST_TIERS = {}
    DEFAULT_COST = 0.05

try:
    from schema_introspect import fetch_schema, parse_schema, detect_aspect_family
except ImportError:
    fetch_schema = parse_schema = detect_aspect_family = None


# Heuristic: model name → type
def model_type(model: str) -> str:
    m = model.lower()
    video_markers = ["video", "seedance", "pika", "runway", "vidu", "v2v", "i2v"]
    edit_markers = ["edit", "inpaint", "fill", "expand", "kontext", "rmbg",
                    "replace-bg", "vectorize"]
    upscale_markers = ["upscale", "upres"]
    if any(v in m for v in video_markers):
        return "video"
    if any(u in m for u in upscale_markers):
        return "upscale"
    if any(e in m for e in edit_markers):
        return "edit"
    return "image"


def cost_tier(cost_usd: float) -> str:
    """Return tier label for a cost."""
    if cost_usd < 0.02:
        return "$"
    if cost_usd < 0.10:
        return "$$"
    if cost_usd < 0.30:
        return "$$$"
    if cost_usd < 0.60:
        return "$$$$"
    return "$$$$$"


def fetch_model_list() -> list[str]:
    """Get available models from `comfy generate list`."""
    try:
        result = subprocess.run(
            ["comfy", "generate", "list"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return []
        # Output is a Rich table — extract model names from lines that look like
        # data rows
        models = []
        for line in result.stdout.splitlines():
            # Look for "│ <model-name>" with non-header content
            if line.startswith("│") and not line.startswith("│ Model"):
                # Split on │ and take first non-empty cell
                parts = [p.strip() for p in line.split("│") if p.strip()]
                if parts and parts[0] and not parts[0].startswith("━"):
                    name = parts[0].split()[0]
                    if name and name not in {"Model", "Partner"}:
                        models.append(name)
        return models
    except Exception:
        # Fallback to hardcoded list from COST_TIERS keys
        return list(COST_TIERS.keys())


def enrich(model: str, include_schema: bool = True) -> dict:
    """Build enriched info dict for a model."""
    cost = COST_TIERS.get(model, DEFAULT_COST)
    info = {
        "model": model,
        "type": model_type(model),
        "cost_usd": cost,
        "tier": cost_tier(cost),
        "aspect_family": "unknown",
        "mode": "unknown",
        "partner": "",
    }
    if include_schema and fetch_schema is not None:
        raw = fetch_schema(model)
        if raw:
            parsed = parse_schema(raw)
            info["aspect_family"] = detect_aspect_family(parsed)
            info["mode"] = parsed.get("mode", "unknown")
            info["partner"] = parsed.get("partner", "")
    return info


def print_table(rows: list[dict], filter_type: str | None) -> None:
    """Print a fixed-width table."""
    if filter_type:
        rows = [r for r in rows if r["type"] == filter_type]
    if not rows:
        print("(no models match)")
        return

    print(f"{'MODEL':24} {'TYPE':8} {'TIER':6} {'COST':>8}  {'MODE':6} {'ASPECT FAMILY':22} PARTNER")
    print("─" * 100)
    for r in sorted(rows, key=lambda x: (x["type"], -x["cost_usd"], x["model"])):
        print(f"{r['model']:24} {r['type']:8} {r['tier']:6} "
              f"${r['cost_usd']:7.3f}  {r['mode']:6} "
              f"{r['aspect_family']:22} {r['partner']}")


def main() -> int:
    p = argparse.ArgumentParser(description="Enriched Comfy Cloud model catalog")
    p.add_argument("model", nargs="?", help="Specific model (omit for full table)")
    p.add_argument("--type", choices=["image", "video", "edit", "upscale"],
                   help="Filter by type")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--no-schema", action="store_true",
                   help="Skip live schema introspection (faster)")
    args = p.parse_args()

    include_schema = not args.no_schema

    if args.model:
        # Single model detail
        info = enrich(args.model, include_schema=include_schema)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"━━━ {info['model']} ━━━")
            print(f"  Type:           {info['type']}")
            print(f"  Cost tier:      {info['tier']} (~${info['cost_usd']:.4f})")
            print(f"  Mode:           {info['mode']}")
            print(f"  Partner:        {info['partner']}")
            print(f"  Aspect family:  {info['aspect_family']}")
        return 0

    # Full table
    models = fetch_model_list()
    if not models:
        models = list(COST_TIERS.keys())
        print("# warning: could not fetch live model list, using hardcoded", file=sys.stderr)

    rows = [enrich(m, include_schema=include_schema) for m in models]

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print_table(rows, args.type)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
