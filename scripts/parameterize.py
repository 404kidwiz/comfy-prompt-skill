#!/usr/bin/env python3
"""
parameterize.py — Swap prompt/seed/dimensions in a ComfyUI workflow JSON.

Usage:
  python3 parameterize.py <blueprint.json> --prompt "..." [--seed N] [--width W] [--height H] [--out PATH]
  python3 parameterize.py <blueprint.json> --inspect    # print node types found

Locates common node types by class_type and swaps values:
  - CLIPTextEncode / CLIPTextEncodeFlux / CLIPTextEncodeSDXL (prompts)
  - KSampler / KSamplerAdvanced / SamplerCustom (seed)
  - EmptyLatentImage / EmptyHunyuanLatentVideo / EmptySD3LatentImage (dims)

Writes to --out (default /tmp/run.json) and prints the path.

LIMITATION: Comfy.org blueprints (in ~/ComfyUI/blueprints/) use proprietary UUID-based
node types instead of standard class_type names. For those, run `--inspect` to see
the structure, then edit manually. Standard ComfyUI workflow exports (from the UI's
"Save (API Format)") work as expected.

Stdlib only, no external deps.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROMPT_NODE_TYPES = {"CLIPTextEncode", "CLIPTextEncodeSDXL", "T5TextEncode"}
SAMPLER_NODE_TYPES = {"KSampler", "KSamplerAdvanced", "SamplerCustom", "SamplerCustomAdvanced"}
LATENT_NODE_TYPES = {
    "EmptyLatentImage",
    "EmptyHunyuanLatentVideo",
    "EmptySD3LatentImage",
    "ModelSamplingFlux",
}


def find_nodes_by_type(workflow: dict, types: set[str]) -> list[tuple[str, dict]]:
    """Return list of (node_id, node) matching any class_type."""
    nodes = workflow.get("nodes") or workflow  # support both formats
    if isinstance(nodes, list):
        # ComfyUI saved-workflow format
        return [(str(n.get("id")), n) for n in nodes if n.get("type") in types]
    # API format: dict keyed by node id
    return [(nid, n) for nid, n in nodes.items() if n.get("class_type") in types]


def set_prompt(workflow: dict, prompt: str, negative: bool = False) -> bool:
    """Set positive (or negative) prompt. Returns True if swap occurred."""
    matches = find_nodes_by_type(workflow, PROMPT_NODE_TYPES)
    if not matches:
        return False

    # Prefer title match; fall back to first/second node
    target = None
    for nid, node in matches:
        title = (node.get("_meta", {}).get("title") or node.get("title") or "").lower()
        if negative and "negative" in title:
            target = (nid, node)
            break
        if not negative and ("positive" in title or "prompt" in title) and "negative" not in title:
            target = (nid, node)
            break

    if target is None:
        # No title match — use first node for positive, second for negative
        if negative and len(matches) >= 2:
            target = matches[1]
        elif not negative:
            target = matches[0]
        else:
            return False

    _nid, node = target
    inputs = node.get("inputs") or node.get("widgets_values")
    if isinstance(inputs, dict):
        if "text" in inputs:
            inputs["text"] = prompt
            return True
    if isinstance(inputs, list) and inputs:
        # saved-workflow widgets_values format — text is usually first
        inputs[0] = prompt
        return True
    return False


def set_seed(workflow: dict, seed: int) -> bool:
    matches = find_nodes_by_type(workflow, SAMPLER_NODE_TYPES)
    if not matches:
        return False
    _nid, node = matches[0]
    inputs = node.get("inputs")
    if isinstance(inputs, dict) and "seed" in inputs:
        inputs["seed"] = seed
        return True
    # saved-workflow format
    widgets = node.get("widgets_values")
    if isinstance(widgets, list) and widgets:
        widgets[0] = seed
        return True
    return False


def set_dimensions(workflow: dict, width: int | None, height: int | None) -> bool:
    if width is None and height is None:
        return False
    matches = find_nodes_by_type(workflow, LATENT_NODE_TYPES)
    if not matches:
        return False
    _nid, node = matches[0]
    inputs = node.get("inputs")
    changed = False
    if isinstance(inputs, dict):
        if width is not None and "width" in inputs:
            inputs["width"] = width
            changed = True
        if height is not None and "height" in inputs:
            inputs["height"] = height
            changed = True
        return changed
    return False


def inspect_workflow(workflow: dict) -> None:
    """Print all node types + IDs for manual inspection."""
    nodes = workflow.get("nodes") or workflow
    if isinstance(nodes, list):
        print(f"Format: ComfyUI saved-workflow ({len(nodes)} nodes)")
        for n in nodes:
            nid = n.get("id", "?")
            ntype = n.get("type", "?")
            title = n.get("title", "")
            print(f"  [{nid:>4}] type={ntype}  title={title!r}")
    else:
        print(f"Format: ComfyUI API ({len(nodes)} nodes)")
        for nid, n in nodes.items():
            ctype = n.get("class_type", "?")
            inputs = list((n.get("inputs") or {}).keys())[:5]
            print(f"  [{nid}] class_type={ctype}  inputs={inputs}")


def main() -> int:
    p = argparse.ArgumentParser(description="Parameterize a ComfyUI workflow JSON.")
    p.add_argument("blueprint", help="Path to blueprint .json")
    p.add_argument("--prompt", help="Positive prompt text")
    p.add_argument("--negative", help="Negative prompt text")
    p.add_argument("--seed", type=int, help="Sampler seed")
    p.add_argument("--width", type=int, help="Output width (latent)")
    p.add_argument("--height", type=int, help="Output height (latent)")
    p.add_argument("--out", default="/tmp/run.json", help="Output path (default /tmp/run.json)")
    p.add_argument("--inspect", action="store_true", help="Print all node types and exit")
    args = p.parse_args()

    src = Path(args.blueprint).expanduser()
    if not src.is_file():
        print(f"error: blueprint not found: {src}", file=sys.stderr)
        return 2

    try:
        workflow = json.loads(src.read_text())
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON in {src}: {e}", file=sys.stderr)
        return 2

    if args.inspect:
        inspect_workflow(workflow)
        return 0

    report: list[str] = []
    if args.prompt and set_prompt(workflow, args.prompt, negative=False):
        report.append(f"prompt → {args.prompt[:60]!r}")
    if args.negative and set_prompt(workflow, args.negative, negative=True):
        report.append(f"negative → {args.negative[:60]!r}")
    if args.seed is not None and set_seed(workflow, args.seed):
        report.append(f"seed → {args.seed}")
    if (args.width or args.height) and set_dimensions(workflow, args.width, args.height):
        report.append(f"dims → {args.width}x{args.height}")

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(workflow, indent=2))

    if report:
        print(f"swapped: {', '.join(report)}")
    else:
        print("no swaps performed (no matching nodes found)", file=sys.stderr)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
