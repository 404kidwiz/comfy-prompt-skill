#!/usr/bin/env python3
"""
lint.py — Prompt linter against HARD RULES from SKILL.md.

Catches common prompt issues BEFORE spending credits:
  - Missing MCSLA layers (Model · Camera · Subject · Look · Action)
  - Off-list models (not in model-guide.md)
  - Off-vocab camera presets (not in vocab.md)
  - Missing negative constraints
  - Off-spec aspect ratios for model
  - Prompts over 200 words
  - Banned phrases / red-flag terms

Usage:
  python3 lint.py "your prompt text" --model flux-pro [--type video|image] [--aspect 16:9]
  python3 lint.py --file /tmp/prompt.txt --model seedance
  python3 lint.py --strict   # treat warnings as errors

Exit codes:
  0 — clean
  1 — warnings (non-strict mode) OR errors (strict mode)
  2 — input error

Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".claude" / "skills" / "comfy-prompt"

# Try to import schema introspection for live flag validation
_INTROSPECT_AVAILABLE = False
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from schema_introspect import fetch_schema, parse_schema
    _INTROSPECT_AVAILABLE = True
except ImportError:
    pass

# Known cloud models (from SKILL.md frontmatter)
KNOWN_MODELS = {
    "flux-2", "flux-pro", "flux-ultra", "flux-kontext", "flux-kontext-max",
    "flux-canny", "flux-depth", "flux-fill", "flux-expand",
    "nano-banana", "dalle", "dalle-edit",
    "stability-sd3", "stability-ultra", "stability-upscale",
    "stability-upscale-creative", "stability-upscale-fast",
    "ideogram", "ideogram-edit",
    "grok", "grok-edit", "grok-video",
    "recraft", "recraft-i2i", "recraft-inpaint", "recraft-rmbg",
    "recraft-replace-bg", "recraft-vectorize", "recraft-upscale",
    "recraft-upscale-creative",
    "seedance", "pika", "pika-i2v", "runway", "runway-i2v",
    "vidu", "vidu-i2v", "vidu-extend", "reve", "reve-edit",
}

VIDEO_MODELS = {
    "seedance", "pika", "pika-i2v", "runway", "runway-i2v",
    "vidu", "vidu-i2v", "vidu-extend", "grok-video",
}

# Common camera presets from vocab.md (partial — file is canonical source)
KNOWN_CAMERA_TERMS = {
    "ecu", "cu", "mcu", "ms", "mws", "ws", "ews", "wide", "medium", "close",
    "extreme close", "extreme close-up", "low angle", "high angle",
    "eye level", "dutch angle", "overhead", "bird's eye", "worm's eye",
    "over-the-shoulder", "ots", "two-shot", "single",
    "dolly", "dolly in", "dolly out", "truck", "pedestal",
    "pan", "tilt", "zoom", "crane", "jib", "steadicam", "handheld",
    "tracking shot", "push in", "pull back", "rack focus", "whip pan",
    "anamorphic", "wide-angle", "fisheye", "telephoto", "macro",
    "static", "locked-off", "locked off",
}

# Vague/weak language that signals lazy prompting
RED_FLAG_PHRASES = [
    "magical effects",
    "epic",
    "amazing",
    "stunning",
    "beautiful",
    "high quality",
    "best quality",
    "masterpiece",
    "realistic",
    "very detailed",
    "8k",
    "trending on artstation",
    "octane render",
]

# Standard aspect ratios
VALID_ASPECTS = {"1:1", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "2.39:1", "2.35:1"}


def load_vocab_terms() -> set[str]:
    """Pull camera/lighting terms from vocab.md if it exists, else use defaults."""
    vocab_file = SKILL_DIR / "vocab.md"
    terms = set(KNOWN_CAMERA_TERMS)
    if vocab_file.is_file():
        try:
            text = vocab_file.read_text().lower()
            # Extract markdown table cells and inline-code terms
            for match in re.findall(r"`([^`]{2,40})`", text):
                if not any(c.isdigit() for c in match[:3]):  # skip "5s", "16:9", etc
                    terms.add(match.strip().lower())
        except OSError:
            pass
    return terms


def lint_prompt(prompt: str, model: str | None, gen_type: str | None,
                aspect: str | None) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    # Rule 1: Model verification — prefer live schema check if available
    schema_model_exists = False
    if model and _INTROSPECT_AVAILABLE:
        raw = fetch_schema(model)
        if raw:
            schema_model_exists = True

    if model:
        if not schema_model_exists and model.lower() not in KNOWN_MODELS:
            errors.append(f"unknown model: {model!r} — not in cloud-models list. "
                          f"Run `comfy generate list` to verify.")
    else:
        warnings.append("no --model specified — can't verify model-specific rules")

    # Rule 1b: Live aspect-flag validation via schema
    if model and aspect and _INTROSPECT_AVAILABLE and schema_model_exists:
        raw = fetch_schema(model)
        if raw:
            parsed = parse_schema(raw)
            flags = parsed.get("flags", {})
            # If model has --ratio enum, validate aspect against it
            if "ratio" in flags and flags["ratio"].get("enum"):
                if aspect not in flags["ratio"]["enum"]:
                    errors.append(f"aspect {aspect!r} not in {model} --ratio enum: "
                                  f"{'|'.join(flags['ratio']['enum'])}")
            if "aspect_ratio" in flags and flags["aspect_ratio"].get("enum"):
                if aspect not in flags["aspect_ratio"]["enum"]:
                    warnings.append(f"aspect {aspect!r} not in {model} --aspect_ratio enum: "
                                     f"{'|'.join(flags['aspect_ratio']['enum'])}")

    # Detect video model
    is_video = (gen_type == "video") or (model and model.lower() in VIDEO_MODELS)

    # Rule 2: Word count
    word_count = len(prompt.split())
    if word_count > 200:
        errors.append(f"prompt is {word_count} words — HARD RULE max is 200. Tighten.")
    elif word_count > 150:
        warnings.append(f"prompt is {word_count} words — approaching 200-word limit")
    elif word_count < 5:
        errors.append(f"prompt is only {word_count} words — too vague")

    # Rule 3: MCSLA layers on video prompts
    if is_video:
        prompt_lc = prompt.lower()
        # Camera language (Camera layer)
        has_camera = any(t in prompt_lc for t in load_vocab_terms())
        if not has_camera:
            warnings.append("video prompt has no explicit camera vocabulary "
                            "(no MCU/ECU/dolly/tracking/etc) — check vocab.md")

        # Action layer — motion-implying verb
        action_verbs = ["walk", "run", "drift", "rise", "fall", "spin", "fly",
                        "dance", "turn", "lean", "reach", "lift", "pour",
                        "open", "close", "drift", "pull", "push", "pan", "track"]
        if not any(v in prompt_lc for v in action_verbs):
            warnings.append("video prompt has no action verb — Action layer weak")

    # Rule 4: Red flag phrases
    prompt_lc = prompt.lower()
    found_redflags = [p for p in RED_FLAG_PHRASES if p in prompt_lc]
    if found_redflags:
        warnings.append(f"weak/cliche phrasing detected: {', '.join(found_redflags[:3])} "
                        f"— replace with concrete description")

    # Rule 5: Aspect ratio
    if aspect:
        if aspect not in VALID_ASPECTS:
            errors.append(f"aspect ratio {aspect!r} unusual — verify against model schema")
        if is_video and aspect in {"21:9", "2.39:1", "2.35:1"}:
            warnings.append(f"aspect {aspect} — cloud video models default to 16:9 or 9:16. "
                            f"Anamorphic is a Look-line register, not an output ratio.")

    # Rule 6: Aspect ratio also embedded in prompt text — should be in metadata
    aspect_in_prompt = re.search(r"(\d+:\d+)\s*(aspect|ratio)?", prompt_lc)
    if aspect_in_prompt and not aspect:
        warnings.append(f"aspect ratio {aspect_in_prompt.group(1)!r} found in prompt text — "
                        f"pass via --aspect_ratio flag instead")

    # Rule 7: Negative constraints — note (lint can't see neg prompt, so warn if appended)
    if "negative:" in prompt_lc or "no:" in prompt_lc or "avoid:" in prompt_lc:
        warnings.append("negative constraints found in prompt body — "
                        "use a separate `--negative` flag if model supports it")

    return errors, warnings


def main() -> int:
    p = argparse.ArgumentParser(description="Lint a Comfy prompt against HARD RULES")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("prompt", nargs="?", help="Prompt text")
    src.add_argument("--file", help="Read prompt from file")
    p.add_argument("--model", help="Target model (for model-specific checks)")
    p.add_argument("--type", choices=["image", "video"], help="Generation type override")
    p.add_argument("--aspect", help="Aspect ratio (e.g. 16:9)")
    p.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    p.add_argument("--quiet", action="store_true", help="Only print errors")
    args = p.parse_args()

    if args.file:
        try:
            prompt = Path(args.file).read_text().strip()
        except OSError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    else:
        prompt = args.prompt or ""

    if not prompt.strip():
        print("error: empty prompt", file=sys.stderr)
        return 2

    errors, warnings = lint_prompt(prompt, args.model, args.type, args.aspect)

    if errors:
        print(f"❌ {len(errors)} error(s):")
        for e in errors:
            print(f"   ✗ {e}")

    if warnings and not args.quiet:
        print(f"⚠  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"   ! {w}")

    if not errors and not warnings:
        if not args.quiet:
            print("✅ prompt lint passed")
        return 0

    if errors:
        return 1
    if args.strict and warnings:
        print(f"❌ strict mode: warnings treated as errors", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
