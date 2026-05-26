#!/usr/bin/env python3
"""
aspect_flags.py — Translate (model, aspect) → correct CLI flags.

Comfy Cloud models use different parameter conventions for image dimensions:
  - BFL Flux (flux-pro/ultra/2):    --width INT --height INT
  - Stability/Ideogram/Reve/Vidu:    --aspect_ratio STRING
  - Seedance, Runway:                --ratio ENUM (+ --resolution for seedance)
  - DALL-E, Recraft, Grok:           --size "WxH"
  - Pika (text-to-video):            --aspectRatio FLOAT  (camelCase!)
  - kontext/fill/expand/rmbg/etc:    no dimension flag (uses source)

This script returns the correct flag list for any (model, aspect) pair.

Usage:
  python3 aspect_flags.py flux-ultra 16:9
  # → --width 1920 --height 1080

  python3 aspect_flags.py seedance 9:16
  # → --ratio 9:16 --resolution 1080p

  python3 aspect_flags.py pika 16:9
  # → --aspectRatio 1.7778

  # Used in bash:
  ARGS=$(python3 aspect_flags.py flux-pro 16:9)
  comfy generate flux-pro --prompt "..." $ARGS --download out.png

Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Try to import schema_introspect for runtime detection.
# Falls back to hardcoded families if introspection unavailable.
_INTROSPECT_AVAILABLE = False
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from schema_introspect import fetch_schema, parse_schema, detect_aspect_family, detect_dimension_constraints
    _INTROSPECT_AVAILABLE = True
except ImportError:
    pass

# ── ASPECT → DIMENSIONS ───────────────────────────────────────────────────────
# All dimensions are multiples of 32 — flux-pro enforces this constraint.
# flux-ultra is more permissive but also accepts these.
# DALL-E `--size` accepts arbitrary "WxH" strings but these are safe defaults.
ASPECT_TO_DIMS: dict[str, tuple[int, int]] = {
    "1:1":  (1024, 1024),  # exact 1:1
    "16:9": (1344, 768),   # 1.75 (close to 1.778)
    "9:16": (768, 1344),
    "4:3":  (1024, 768),   # exact 1.333
    "3:4":  (768, 1024),
    "4:5":  (1024, 1280),  # exact 0.8 — both /32
    "5:4":  (1280, 1024),
    "21:9": (1792, 768),   # 2.333 — exact
    "9:21": (768, 1792),
    "3:2":  (1536, 1024),  # 1.5 exact
    "2:3":  (1024, 1536),
    "2:1":  (1536, 768),   # 2.0 exact
    "1:2":  (768, 1536),
}

# Higher-res dimensions for models that support larger output (flux-ultra, dalle).
# flux-ultra accepts non-multiples-of-32; dalle accepts arbitrary WxH.
ASPECT_TO_DIMS_HIRES: dict[str, tuple[int, int]] = {
    "1:1":  (1536, 1536),
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "4:3":  (1536, 1152),
    "3:4":  (1152, 1536),
    "21:9": (2520, 1080),
    "9:21": (1080, 2520),
    "3:2":  (1920, 1280),
    "2:3":  (1280, 1920),
}

# Models that support hi-res dimensions
FAMILY_HIRES_OK = {"flux-ultra", "flux-2", "dalle", "dalle-edit"}

# Pika uses --aspectRatio as a FLOAT (camelCase)
ASPECT_TO_PIKA_FLOAT: dict[str, float] = {
    "1:1":  1.0,
    "16:9": 1.7778,
    "9:16": 0.5625,
    "4:3":  1.3333,
    "3:4":  0.75,
    "4:5":  0.8,
    "5:4":  1.25,
    "21:9": 2.3333,
    "9:21": 0.4286,
    "3:2":  1.5,
    "2:3":  0.6667,
}

# ── MODEL FAMILIES ────────────────────────────────────────────────────────────
# Map model → flag convention. Names match `comfy generate list` output.

FAMILY_WIDTH_HEIGHT = {
    "flux-pro", "flux-ultra", "flux-2",
}

FAMILY_ASPECT_RATIO_STR = {
    "stability-sd3", "stability-ultra",
    "ideogram",
    "vidu", "vidu-i2v",
    "reve", "reve-edit",
    "grok", "grok-edit",
    "grok-video",
}

FAMILY_RATIO_ENUM_ONLY = {
    "runway", "runway-i2v",
}

FAMILY_RATIO_PLUS_RESOLUTION = {
    "seedance",
}

FAMILY_SIZE_STRING = {
    "dalle", "dalle-edit",
    "recraft",
}

FAMILY_PIKA_ASPECT_FLOAT = {
    "pika",
}

# Models that do not accept any dimension flag — use source image or default
FAMILY_NO_ASPECT = {
    "flux-kontext", "flux-kontext-max",
    "flux-canny", "flux-depth", "flux-fill", "flux-expand",
    "nano-banana",
    "ideogram-edit",
    "recraft-i2i", "recraft-rmbg", "recraft-replace-bg",
    "recraft-vectorize", "recraft-upscale", "recraft-upscale-creative",
    "recraft-inpaint",
    "stability-upscale", "stability-upscale-fast", "stability-upscale-creative",
    "pika-i2v",
    "vidu-extend",
}


def _round_to_multiple(value: int, multiple: int) -> int:
    """Round down to nearest multiple."""
    return (value // multiple) * multiple


def detect_family_runtime(model: str) -> str | None:
    """
    Detect family via runtime schema introspection.
    Returns family name on success, None if introspection unavailable or failed.
    """
    if not _INTROSPECT_AVAILABLE or os.environ.get("COMFY_NO_INTROSPECT") == "1":
        return None
    try:
        raw = fetch_schema(model)
        if not raw:
            return None
        parsed = parse_schema(raw)
        return detect_aspect_family(parsed)
    except Exception:
        return None


def detect_constraints_runtime(model: str) -> dict | None:
    """Detect dimension constraints (e.g. /32) via introspection."""
    if not _INTROSPECT_AVAILABLE or os.environ.get("COMFY_NO_INTROSPECT") == "1":
        return None
    try:
        raw = fetch_schema(model)
        if not raw:
            return None
        parsed = parse_schema(raw)
        return detect_dimension_constraints(parsed)
    except Exception:
        return None


def aspect_flags_for(model: str, aspect: str, resolution: str = "1080p") -> list[str]:
    """
    Return CLI flag list for (model, aspect).

    Resolution order:
      1. Runtime schema introspection (if `comfy` available + cache fresh)
      2. Hardcoded family sets (fallback)
      3. Empty list (unknown model)

    Empty list if model doesn't accept a dimension flag.
    """
    model = model.lower().strip()
    aspect = aspect.strip()

    # Try runtime introspection first
    runtime_family = detect_family_runtime(model)
    if runtime_family:
        family = runtime_family
        # Also detect constraints for width/height families
        constraints = detect_constraints_runtime(model) or {}
    else:
        # Fall back to hardcoded families
        if model in FAMILY_NO_ASPECT:
            return []
        if model in FAMILY_WIDTH_HEIGHT:
            family = "width_height"
        elif model in FAMILY_ASPECT_RATIO_STR:
            family = "aspect_ratio_str"
        elif model in FAMILY_RATIO_ENUM_ONLY:
            family = "ratio_enum_only"
        elif model in FAMILY_RATIO_PLUS_RESOLUTION:
            family = "ratio_plus_resolution"
        elif model in FAMILY_SIZE_STRING:
            family = "size_string"
        elif model in FAMILY_PIKA_ASPECT_FLOAT:
            family = "pika_aspect_float"
        else:
            print(f"# warning: unknown model {model!r}, guessing --aspect_ratio {aspect}",
                  file=sys.stderr)
            return ["--aspect_ratio", aspect]
        constraints = {"multiple_of": 32 if model in {"flux-pro", "flux-2"} else None}

    # Dispatch by family
    if family == "none":
        return []

    if family == "width_height":
        if model in FAMILY_HIRES_OK:
            w, h = ASPECT_TO_DIMS_HIRES.get(aspect, ASPECT_TO_DIMS.get(aspect, (1024, 1024)))
        else:
            w, h = ASPECT_TO_DIMS.get(aspect, (1024, 1024))
        # Apply constraints (e.g. multiple-of-32 for flux-pro)
        mult = constraints.get("multiple_of")
        if mult:
            w = _round_to_multiple(w, mult)
            h = _round_to_multiple(h, mult)
        return ["--width", str(w), "--height", str(h)]

    if family == "aspect_ratio_str":
        return ["--aspect_ratio", aspect]

    if family == "ratio_enum_only":
        return ["--ratio", aspect]

    if family == "ratio_plus_resolution":
        return ["--ratio", aspect, "--resolution", resolution]

    if family == "size_string":
        if model in FAMILY_HIRES_OK:
            w, h = ASPECT_TO_DIMS_HIRES.get(aspect, ASPECT_TO_DIMS.get(aspect, (1024, 1024)))
        else:
            w, h = ASPECT_TO_DIMS.get(aspect, (1024, 1024))
        return ["--size", f"{w}x{h}"]

    if family == "pika_aspect_float":
        ratio = ASPECT_TO_PIKA_FLOAT.get(aspect, 1.7778)
        return ["--aspectRatio", f"{ratio}"]

    return []


def main() -> int:
    p = argparse.ArgumentParser(
        description="Translate (model, aspect) → correct Comfy CLI flags")
    p.add_argument("model", help="Comfy Cloud model name")
    p.add_argument("aspect", help="Aspect ratio (e.g. 16:9, 1:1, 9:16)")
    p.add_argument("--resolution", default="1080p",
                   help="Resolution enum for video models (default: 1080p)")
    p.add_argument("--family", action="store_true",
                   help="Print the family name instead of flags")
    args = p.parse_args()

    if args.family:
        m = args.model.lower()
        for name, models in [
            ("none", FAMILY_NO_ASPECT),
            ("width_height", FAMILY_WIDTH_HEIGHT),
            ("aspect_ratio_str", FAMILY_ASPECT_RATIO_STR),
            ("ratio_enum_only", FAMILY_RATIO_ENUM_ONLY),
            ("ratio_plus_resolution", FAMILY_RATIO_PLUS_RESOLUTION),
            ("size_string", FAMILY_SIZE_STRING),
            ("pika_aspect_float", FAMILY_PIKA_ASPECT_FLOAT),
        ]:
            if m in models:
                print(name)
                return 0
        print("unknown")
        return 1

    flags = aspect_flags_for(args.model, args.aspect, args.resolution)
    if flags:
        print(" ".join(flags))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
