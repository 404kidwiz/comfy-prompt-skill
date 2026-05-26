#!/usr/bin/env python3
"""
translate.py — Cross-model prompt adaptation.

Different cloud models respond best to different prompt phrasings:
  - Flux family:    cinematic descriptive language, technical camera terms
  - DALL-E / GPT:   "a photograph of...", natural sentence structure
  - Ideogram:       text-heavy prompts work, literal description of text
  - Stability:      tag-style with quality boosters
  - Recraft:        vector/illustration vocabulary
  - Seedance/Pika:  motion verbs, time-explicit (e.g. "over 5 seconds")
  - nano-banana:    multimodal-friendly, conversational

This script takes a prompt written for one model and re-phrases for another.

Usage:
  python3 translate.py "your prompt" --from flux-pro --to dalle
  python3 translate.py "your prompt" --to seedance --duration 5
  python3 translate.py --list

Stdlib only — uses rule-based transformation, no LLM call.
"""

from __future__ import annotations

import argparse
import re
import sys

# Model families
FAMILIES = {
    "flux": ["flux-2", "flux-pro", "flux-ultra", "flux-kontext", "flux-kontext-max",
             "flux-canny", "flux-depth", "flux-fill", "flux-expand"],
    "openai": ["dalle", "dalle-edit"],
    "ideogram": ["ideogram", "ideogram-edit"],
    "stability": ["stability-sd3", "stability-ultra"],
    "recraft": ["recraft", "recraft-i2i", "recraft-inpaint", "recraft-rmbg",
                "recraft-replace-bg", "recraft-vectorize"],
    "video": ["seedance", "pika", "pika-i2v", "runway", "runway-i2v",
              "vidu", "vidu-i2v", "vidu-extend", "grok-video"],
    "google": ["nano-banana"],
    "xai": ["grok", "grok-edit"],
    "reve": ["reve", "reve-edit"],
}


def model_family(model: str) -> str:
    for fam, models in FAMILIES.items():
        if model in models:
            return fam
    return "unknown"


# Adapters: tweak prompt phrasing for target family
def adapt_flux(prompt: str) -> str:
    """Flux likes cinematic descriptive language. Strip tag-style."""
    # Strip stability-style boosters
    prompt = re.sub(r",?\s*(8k|4k|hyper[- ]?detailed|masterpiece|best quality)\b",
                     "", prompt, flags=re.IGNORECASE)
    # Strip trailing commas
    prompt = re.sub(r",\s*$", "", prompt.strip())
    return prompt


def adapt_openai(prompt: str) -> str:
    """DALL-E prefers natural sentence structure with 'a photograph of...'"""
    # Strip technical camera abbreviations and rewrite
    abbrev = {
        r"\bECU\b": "extreme close-up shot",
        r"\bMCU\b": "medium close-up shot",
        r"\bMS\b":  "medium shot",
        r"\bWS\b":  "wide shot",
        r"\bEWS\b": "extreme wide establishing shot",
    }
    for pat, repl in abbrev.items():
        prompt = re.sub(pat, repl, prompt)
    # Add natural framing if not present
    if not re.search(r"^(a |an |the |photograph|image|portrait)", prompt, re.IGNORECASE):
        prompt = "A photograph of " + prompt[0].lower() + prompt[1:]
    return prompt


def adapt_ideogram(prompt: str) -> str:
    """Ideogram is good at text-in-image. Boost text rendering keywords."""
    if "text" in prompt.lower() or "type" in prompt.lower() or "sign" in prompt.lower():
        if "vector-clean" not in prompt.lower():
            prompt += ", clean kerning, vector-clean edges, perfect text rendering"
    return prompt


def adapt_stability(prompt: str) -> str:
    """Stability SD3 likes tag-style with quality boosters appended."""
    if "8k" not in prompt.lower() and "highly detailed" not in prompt.lower():
        prompt += ", highly detailed, sharp focus, professional"
    return prompt


def adapt_recraft(prompt: str) -> str:
    """Recraft works well with vector/illustration vocabulary."""
    if "vector" not in prompt.lower() and "illustration" not in prompt.lower():
        # Don't force vector if user is doing photo — only if it's already stylized
        pass
    return prompt


def adapt_video(prompt: str, duration: int | None) -> str:
    """Video models need motion verbs and time-explicit framing."""
    motion_verbs = ["dolly", "pan", "tilt", "crane", "track", "push", "pull", "drift",
                     "walk", "run", "rise", "fall", "spin", "fly", "swing"]
    has_motion = any(v in prompt.lower() for v in motion_verbs)
    if not has_motion:
        prompt = "subtle camera dolly in over " + (f"{duration} seconds, " if duration else "the shot, ") + prompt
    # Add duration cue
    if duration and f"{duration}" not in prompt and "over" not in prompt.lower():
        prompt += f", motion sustained over {duration} seconds"
    return prompt


def adapt_google(prompt: str) -> str:
    """nano-banana is multimodal — conversational works."""
    return prompt


ADAPTERS = {
    "flux": adapt_flux,
    "openai": adapt_openai,
    "ideogram": adapt_ideogram,
    "stability": adapt_stability,
    "recraft": adapt_recraft,
    "google": adapt_google,
}


def translate(prompt: str, from_family: str, to_family: str,
              duration: int | None = None) -> str:
    """Adapt a prompt from one model family to another."""
    if to_family == "video":
        return adapt_video(prompt, duration)
    adapter = ADAPTERS.get(to_family)
    if adapter:
        return adapter(prompt)
    return prompt  # unknown target — passthrough


def main() -> int:
    p = argparse.ArgumentParser(description="Adapt prompts across model families")
    p.add_argument("prompt", nargs="?", help="Source prompt")
    p.add_argument("--from", dest="from_model", default="flux-pro",
                   help="Source model (default: flux-pro)")
    p.add_argument("--to", dest="to_model", help="Target model")
    p.add_argument("--duration", type=int, help="Video duration in seconds (for video targets)")
    p.add_argument("--list", action="store_true", help="List supported families")
    args = p.parse_args()

    if args.list:
        for fam, models in FAMILIES.items():
            print(f"{fam}: {', '.join(models)}")
        return 0

    if not args.prompt or not args.to_model:
        print("usage: translate.py PROMPT --to TARGET_MODEL", file=sys.stderr)
        return 1

    from_fam = model_family(args.from_model)
    to_fam = model_family(args.to_model)

    if to_fam == "unknown":
        print(f"warning: unknown target model {args.to_model!r}", file=sys.stderr)

    adapted = translate(args.prompt, from_fam, to_fam, args.duration)
    print(adapted)

    if from_fam != to_fam:
        print(f"  # translated: {from_fam} → {to_fam}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
