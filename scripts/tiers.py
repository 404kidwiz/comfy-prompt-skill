#!/usr/bin/env python3
"""
tiers.py — Premium-first model tier resolver.

Single source of truth for which model to pick given:
  - task type:   image | image-edit | video-t2v | video-i2v | upscale | bg
  - quality:     s (premium) | a (high) | b (mid) | c (cheapest)
  - budget mode: True downshifts S→B by default

Quality philosophy:
  S — best-in-class. Maximum quality. No compromise.
  A — strong premium. ~70% of S quality, ~50% of S cost.
  B — solid mid. Reliable, fast, cheap.
  C — bargain. Drafts, iteration, throwaway.

Usage from Python:
    from tiers import pick
    pick("image")                        # → "gemini-3-pro-image-preview" (S default)
    pick("image", quality="b")           # → "flux-pro"
    pick("video-t2v", budget=True)       # → "pika" (downshifted from kling-v3)
    pick("image-edit")                   # → "flux-kontext-max"

Usage from bash:
    MODEL=$(python3 scripts/tiers.py image)
    MODEL=$(python3 scripts/tiers.py video-t2v --budget)
    python3 scripts/tiers.py image --quality s --json   # full envelope

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Tier definitions — premium first
# ---------------------------------------------------------------------------

# Each task maps to {S, A, B, C} model name.
# nano-banana entries with model variant: tuple (base_model, --model arg)
TIERS: dict[str, dict[str, str | tuple[str, str]]] = {
    # ── Text-to-image ──────────────────────────────────────────────────────
    "image": {
        "s": ("nano-banana", "gemini-3-pro-image-preview"),  # Gemini 3 Pro — premium
        "a": "flux-ultra",                                   # BFL Flux Pro 1.1 Ultra
        "b": "flux-pro",                                     # BFL Flux Pro 1.1
        "c": ("nano-banana", "gemini-2.5-flash-image"),      # Cheapest reliable
    },

    # ── Image edit ─────────────────────────────────────────────────────────
    "image-edit": {
        "s": "flux-kontext-max",     # Max quality edit
        "a": "flux-kontext",         # Pro edit
        "b": ("nano-banana", "gemini-2.5-flash-image"),  # Fast Gemini edit
        "c": "recraft-i2i",          # Cheap image-to-image
    },

    # ── Inpaint (mask-driven edit) ────────────────────────────────────────
    "inpaint": {
        "s": "flux-fill",
        "a": "flux-fill",
        "b": "recraft-inpaint",
        "c": "recraft-inpaint",
    },

    # ── Outpaint / expand ─────────────────────────────────────────────────
    "outpaint": {
        "s": "flux-expand",
        "a": "flux-expand",
        "b": "flux-expand",
        "c": "flux-expand",
    },

    # ── Text-rendering-heavy images (typography, posters with copy) ──────
    "image-text": {
        "s": "ideogram",             # Ideogram is text king
        "a": ("nano-banana", "gemini-3-pro-image-preview"),
        "b": "dalle",                # OpenAI is solid for text
        "c": ("nano-banana", "gemini-2.5-flash-image"),
    },

    # ── Illustration / vector-style ───────────────────────────────────────
    "illustration": {
        "s": "recraft",
        "a": "ideogram",
        "b": "stability-sd3",
        "c": "recraft",
    },

    # ── Text-to-video ─────────────────────────────────────────────────────
    "video-t2v": {
        "s": "kling",                # kling-v3 (set via --model_name)
        "a": "seedance",             # ByteDance cinematic
        "b": "hailuo",               # MiniMax fast
        "c": "pika",                 # Cheapest reliable
    },

    # ── Image-to-video ────────────────────────────────────────────────────
    "video-i2v": {
        "s": "kling-i2v",            # kling-v3 (set via --model_name)
        "a": "runway-i2v",           # Runway cinematic
        "b": "vidu-i2v",             # Solid mid
        "c": "pika-i2v",             # Cheapest
    },

    # ── Background remove ─────────────────────────────────────────────────
    "bg-remove": {
        "s": "recraft-rmbg",
        "a": "recraft-rmbg",
        "b": "recraft-rmbg",
        "c": "recraft-rmbg",
    },

    # ── Background replace ────────────────────────────────────────────────
    "bg-replace": {
        "s": "recraft-replace-bg",
        "a": "recraft-replace-bg",
        "b": "ideogram-bg",
        "c": "recraft-replace-bg",
    },

    # ── Upscale ───────────────────────────────────────────────────────────
    "upscale": {
        "s": "recraft-upscale-creative",   # Creative upscale (slow but premium)
        "a": "stability-upscale-creative",
        "b": "recraft-upscale",
        "c": "stability-upscale-fast",
    },

    # ── Vectorize ─────────────────────────────────────────────────────────
    "vectorize": {
        "s": "recraft-vectorize",
        "a": "recraft-vectorize",
        "b": "recraft-vectorize",
        "c": "recraft-vectorize",
    },
}


# Premium video sub-model defaults (for models with --model_name variants)
VIDEO_PREMIUM_VARIANT = {
    "kling": "kling-v3",
    "kling-i2v": "kling-v3",
}
VIDEO_BUDGET_VARIANT = {
    "kling": "kling-v1-6",
    "kling-i2v": "kling-v1-6",
}


# Quality fallback chain — applied when downshifting via --budget
DOWNSHIFT = {"s": "b", "a": "b", "b": "c", "c": "c"}


@dataclass
class Pick:
    model: str
    sub_model: str | None      # nano-banana --model OR kling --model_name
    sub_flag: str | None       # name of the flag to set sub-model (--model | --model_name)
    quality: str
    task: str


def normalize_quality(q: str) -> str:
    q = q.lower().strip()
    if q in ("s", "premium", "max"):
        return "s"
    if q in ("a", "high"):
        return "a"
    if q in ("b", "mid", "medium"):
        return "b"
    if q in ("c", "budget", "cheap", "low"):
        return "c"
    raise ValueError(f"unknown quality: {q!r}. Use s|a|b|c")


def pick(task: str, quality: str = "s", budget: bool = False) -> Pick:
    """Resolve task + quality (+budget flag) → model + sub-model."""
    task = task.lower().strip()
    if task not in TIERS:
        raise ValueError(f"unknown task: {task!r}. Choices: {', '.join(TIERS)}")

    q = normalize_quality(quality)
    if budget:
        q = DOWNSHIFT[q]

    entry = TIERS[task][q]

    if isinstance(entry, tuple):
        base, sub = entry
        # nano-banana uses --model, kling uses --model_name
        sub_flag = "--model_name" if base.startswith("kling") else "--model"
        return Pick(model=base, sub_model=sub, sub_flag=sub_flag,
                    quality=q, task=task)

    # Video models with implicit sub-model defaults
    if entry in VIDEO_PREMIUM_VARIANT:
        sub = (VIDEO_BUDGET_VARIANT[entry] if budget or q in ("b", "c")
               else VIDEO_PREMIUM_VARIANT[entry])
        return Pick(model=entry, sub_model=sub, sub_flag="--model_name",
                    quality=q, task=task)

    return Pick(model=entry, sub_model=None, sub_flag=None,
                quality=q, task=task)


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolve task → premium model")
    ap.add_argument("task", help=f"Task type: {', '.join(TIERS)}")
    ap.add_argument("--quality", "-q", default="s",
                    help="s (premium, default) | a | b | c")
    ap.add_argument("--budget", action="store_true",
                    help="Downshift quality (S→B, A→B, B→C)")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON envelope with all flags")
    ap.add_argument("--flags", action="store_true",
                    help="Emit ready-to-paste CLI flags (model + sub-flag)")
    ap.add_argument("--sub-flags", action="store_true",
                    help="Emit only the sub-model flag pair (or empty)")
    args = ap.parse_args()

    try:
        p = pick(args.task, quality=args.quality, budget=args.budget)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({
            "model": p.model,
            "sub_model": p.sub_model,
            "sub_flag": p.sub_flag,
            "quality": p.quality,
            "task": p.task,
        }, indent=2))
        return 0

    if args.flags:
        parts = [p.model]
        if p.sub_model and p.sub_flag:
            parts += [p.sub_flag, p.sub_model]
        print(" ".join(parts))
        return 0

    if args.sub_flags:
        # Just the sub-flag pair (or empty), ready to interpolate after model name.
        # E.g. "--model gemini-3-pro-image-preview" or "--model_name kling-v3" or ""
        if p.sub_model and p.sub_flag:
            print(f"{p.sub_flag} {p.sub_model}")
        else:
            print("")
        return 0

    # Default: just the model name (for $(python3 tiers.py image))
    print(p.model)
    return 0


if __name__ == "__main__":
    sys.exit(main())
