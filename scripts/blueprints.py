#!/usr/bin/env python3
"""
blueprints.py — Scan ~/ComfyUI/blueprints/ and report on local workflows.

For each blueprint:
  - Filename
  - Category (Text-to-Image, Image-to-Image, Video, Edit, Upscale, etc — inferred)
  - Node count
  - Required models (extracted from CheckpointLoader/LoraLoader node values)
  - File size

Usage:
  python3 blueprints.py list           # table view
  python3 blueprints.py list --category video
  python3 blueprints.py inspect <name>  # full node breakdown
  python3 blueprints.py search "flux"   # filter by keyword

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

BLUEPRINTS_DIR = Path.home() / "ComfyUI" / "blueprints"

CATEGORY_PATTERNS = [
    ("Video",          [r"\bvideo\b", r"wan", r"ltx", r"animate", r"i2v"]),
    ("Edit",           [r"\bedit\b", r"\binpaint", r"\bfill\b", r"kontext"]),
    ("Upscale",        [r"upscale", r"upres", r"\bsr\b"]),
    ("Image-to-Image", [r"i2i", r"image[- ]to[- ]image", r"img2img"]),
    ("ControlNet",     [r"canny", r"depth", r"control", r"openpose"]),
    ("Inpaint",        [r"inpaint", r"mask"]),
    ("Text-to-Image",  [r"text[- ]?to[- ]?image", r"t2i", r"flux", r"sdxl",
                         r"stable[- ]diffusion"]),
]


def infer_category(filename: str) -> str:
    name = filename.lower()
    for cat, patterns in CATEGORY_PATTERNS:
        for pat in patterns:
            if re.search(pat, name):
                return cat
    return "Other"


def extract_models(workflow: dict) -> list[str]:
    """Find checkpoint/lora references in the workflow JSON."""
    models: set[str] = set()

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                # Standard ComfyUI nodes have 'ckpt_name', 'lora_name', etc.
                if k in {"ckpt_name", "lora_name", "model_name", "unet_name",
                         "vae_name", "clip_name"} and isinstance(v, str):
                    models.add(v)
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(workflow)
    return sorted(models)


def load_blueprint(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def count_nodes(workflow: dict) -> int:
    """Count nodes in either standard or Comfy.org blueprint format."""
    if "nodes" in workflow and isinstance(workflow["nodes"], list):
        return len(workflow["nodes"])
    # Standard ComfyUI format: dict keyed by node IDs
    return len([k for k in workflow.keys() if isinstance(workflow.get(k), dict)
                and "class_type" in workflow[k]])


def cmd_list(args: argparse.Namespace) -> int:
    if not BLUEPRINTS_DIR.is_dir():
        print(f"error: not a directory: {BLUEPRINTS_DIR}", file=sys.stderr)
        return 1

    blueprints = sorted(BLUEPRINTS_DIR.glob("*.json"))
    if not blueprints:
        print("(no blueprints found)")
        return 0

    rows = []
    for bp in blueprints:
        cat = infer_category(bp.name)
        if args.category and cat.lower() != args.category.lower():
            continue
        if args.search and args.search.lower() not in bp.name.lower():
            continue
        wf = load_blueprint(bp)
        nodes = count_nodes(wf) if wf else 0
        models = extract_models(wf) if wf else []
        size_kb = bp.stat().st_size / 1024
        rows.append((bp.name[:55], cat, nodes, len(models), f"{size_kb:.1f}K"))

    if not rows:
        print(f"(no blueprints match filters)")
        return 0

    print(f"{'FILE':55} {'CATEGORY':16} {'NODES':>6} {'MODELS':>7} {'SIZE':>7}")
    print(f"{'-' * 55} {'-' * 16} {'-' * 6} {'-' * 7} {'-' * 7}")
    for fname, cat, nodes, models, size in rows:
        print(f"{fname:55} {cat:16} {nodes:>6} {models:>7} {size:>7}")

    print(f"\nTotal: {len(rows)} blueprint{'s' if len(rows) != 1 else ''}")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    # Find by partial name
    matches = list(BLUEPRINTS_DIR.glob(f"*{args.name}*"))
    if not matches:
        print(f"no blueprint matching: {args.name}", file=sys.stderr)
        return 1
    if len(matches) > 1 and not args.first:
        print(f"multiple matches: {[m.name for m in matches]}", file=sys.stderr)
        return 1

    bp = matches[0]
    wf = load_blueprint(bp)
    if not wf:
        print(f"failed to parse: {bp}", file=sys.stderr)
        return 1

    print(f"━━━ {bp.name} ━━━")
    print(f"Path: {bp}")
    print(f"Size: {bp.stat().st_size / 1024:.1f} KB")
    print(f"Category: {infer_category(bp.name)}")
    print(f"Nodes: {count_nodes(wf)}")
    print()

    models = extract_models(wf)
    if models:
        print("Required models:")
        for m in models:
            print(f"  - {m}")
    print()

    # Class types breakdown (standard format only)
    class_types: dict[str, int] = {}
    for k, v in wf.items():
        if isinstance(v, dict) and "class_type" in v:
            ct = v["class_type"]
            class_types[ct] = class_types.get(ct, 0) + 1

    if class_types:
        print("Node class types:")
        for ct, cnt in sorted(class_types.items(), key=lambda x: -x[1]):
            print(f"  {ct} × {cnt}")
    else:
        # Comfy.org UUID format
        if "nodes" in wf:
            print("Comfy.org blueprint format (UUID node types — use parameterize.py --inspect)")

    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Scan local ComfyUI blueprints")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List blueprints")
    p_list.add_argument("--category", help="Filter by category")
    p_list.add_argument("--search", help="Filter by filename substring")
    p_list.set_defaults(func=cmd_list)

    p_inspect = sub.add_parser("inspect", help="Inspect one blueprint")
    p_inspect.add_argument("name", help="Filename substring")
    p_inspect.add_argument("--first", action="store_true",
                            help="Use first match if multiple found")
    p_inspect.set_defaults(func=cmd_inspect)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
