#!/usr/bin/env python3
"""
schema_introspect.py — Parse `comfy generate schema <model>` output into structured data.

Detects:
  - Which flags accept dimensions (--width/--height, --aspect_ratio, --ratio, --size, --aspectRatio)
  - Enum values per flag
  - Required vs optional flags
  - Returns a "family" classification for use by aspect_flags.py

Caches results via schema_cache.py (24h TTL).

Usage:
  python3 schema_introspect.py <model>           # JSON dump
  python3 schema_introspect.py <model> --family  # just family name
  python3 schema_introspect.py <model> --flags   # just flag names

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = Path.home() / ".comfy-cache" / "schemas"
DEFAULT_TTL_HOURS = 24


def fetch_schema(model: str, force_refresh: bool = False,
                 ttl_hours: int = DEFAULT_TTL_HOURS) -> str | None:
    """
    Fetch schema text via direct `comfy generate schema` call.
    Caches result to ~/.comfy-cache/schemas/<model>.json for ttl_hours.
    """
    cache_file = CACHE_DIR / f"{model}.json"

    # Read from cache if fresh
    if not force_refresh and cache_file.is_file():
        age_seconds = time.time() - cache_file.stat().st_mtime
        if age_seconds < ttl_hours * 3600:
            try:
                data = json.loads(cache_file.read_text())
                return data.get("raw", "")
            except (json.JSONDecodeError, OSError):
                pass  # fall through to fetch fresh

    # Fetch from comfy CLI
    try:
        result = subprocess.run(
            ["comfy", "generate", "schema", model],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            # Try stale cache as last resort
            if cache_file.is_file():
                try:
                    data = json.loads(cache_file.read_text())
                    return data.get("raw", "")
                except (json.JSONDecodeError, OSError):
                    pass
            return None

        raw = result.stdout
        # Write to cache
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({
            "model": model,
            "fetched_at": time.time(),
            "raw": raw,
        }, indent=2))
        return raw
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return None


def parse_schema(raw: str) -> dict[str, Any]:
    """
    Parse a `comfy generate schema` output block.

    Returns:
        {
          "model": str,
          "mode": "sync" | "async" | "unknown",
          "flags": {
              "<flag_name>": {
                  "type": "string" | "integer" | "number" | "boolean" | "enum",
                  "enum": list[str] | None,
                  "required": bool,
                  "description": str
              }
          }
        }
    """
    result = {
        "model": "",
        "mode": "unknown",
        "partner": "",
        "flags": {},
    }

    if not raw:
        return result

    # Header line: Model: flux-pro  (bfl/flux-pro/generate)
    m = re.search(r"^Model:\s+(\S+)", raw, re.MULTILINE)
    if m:
        result["model"] = m.group(1)

    # Mode + partner line
    m = re.search(r"partner:\s*(\S+).*?mode:\s*(\S+)", raw)
    if m:
        result["partner"] = m.group(1)
        mode_raw = m.group(2).lower()
        if "async" in mode_raw:
            result["mode"] = "async"
        elif "sync" in mode_raw:
            result["mode"] = "sync"

    # Parse parameter lines
    # Format:
    #   * --width <integer>          (required, *)
    #       Description...
    #     --negative_prompt <string> (optional)
    #     --resolution <enum=480p|720p|1080p>
    #     --aspect_ratio             (no type after dashes — string default)
    flag_pattern = re.compile(
        r"^(\s*)([*]?)\s*--(\S+)(?:\s+<([^>]+)>)?\s*$",
        re.MULTILINE,
    )

    for match in flag_pattern.finditer(raw):
        leading_ws, star, name, type_spec = match.groups()
        if name in {"download", "async", "json", "timeout", "api-key"}:
            # Common options, not model params
            continue

        required = (star == "*")
        type_str = (type_spec or "string").strip()
        enum_values = None

        # Parse enum=A|B|C
        em = re.match(r"enum=(.+)$", type_str)
        if em:
            enum_values = em.group(1).split("|")
            type_str = "enum"
        elif type_str in {"integer", "number", "boolean", "string"}:
            pass
        else:
            # Default to string
            type_str = "string"

        result["flags"][name] = {
            "type": type_str,
            "enum": enum_values,
            "required": required,
        }

    return result


def detect_aspect_family(parsed: dict[str, Any]) -> str:
    """
    Classify model into one of the 6 aspect-flag families based on parsed schema.

    Returns one of:
      width_height | aspect_ratio_str | ratio_enum_only |
      ratio_plus_resolution | size_string | pika_aspect_float |
      grok_video | none
    """
    flags = parsed.get("flags", {})
    has = lambda *names: all(n in flags for n in names)
    any_of = lambda *names: any(n in flags for n in names)

    if has("width", "height"):
        return "width_height"
    if "aspectRatio" in flags:  # camelCase — Pika
        return "pika_aspect_float"
    if has("ratio", "resolution"):
        return "ratio_plus_resolution"
    if "ratio" in flags:
        return "ratio_enum_only"
    if "aspect_ratio" in flags:
        return "aspect_ratio_str"
    if "size" in flags and not has("width", "height"):
        return "size_string"
    return "none"


def detect_dimension_constraints(parsed: dict[str, Any]) -> dict[str, Any]:
    """
    Detect known dimension constraints (e.g. multiple-of-32 for flux-pro).

    NOTE: comfy generate schema doesn't advertise these, so we hardcode known
    constraints by model name. Future: scrape from API errors if needed.
    """
    model = parsed.get("model", "").lower()
    constraints = {"multiple_of": None, "max_width": None, "max_height": None}

    # Known constraints (discovered empirically)
    if any(m in model for m in ["flux-pro", "flux-2", "flux-kontext-max"]):
        constraints["multiple_of"] = 32
    if "flux-ultra" in model:
        # flux-ultra is permissive on /32 but max ~2520
        constraints["max_width"] = 2520
        constraints["max_height"] = 2520

    return constraints


def cmd_dump(args: argparse.Namespace) -> int:
    raw = fetch_schema(args.model, force_refresh=args.refresh)
    if not raw:
        print(f"error: could not fetch schema for {args.model}", file=sys.stderr)
        return 1

    parsed = parse_schema(raw)
    parsed["aspect_family"] = detect_aspect_family(parsed)
    parsed["constraints"] = detect_dimension_constraints(parsed)

    if args.family:
        print(parsed["aspect_family"])
        return 0

    if args.flags:
        for name, info in sorted(parsed["flags"].items()):
            req = "*" if info["required"] else " "
            type_str = info["type"]
            if info["enum"]:
                type_str = f"enum={'|'.join(info['enum'][:5])}"
            print(f"  {req} --{name:24} <{type_str}>")
        return 0

    print(json.dumps(parsed, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Parse Comfy Cloud model schema")
    p.add_argument("model", help="Model name (e.g. flux-pro)")
    p.add_argument("--refresh", action="store_true", help="Force refresh from API")
    p.add_argument("--family", action="store_true",
                   help="Print only the aspect-flag family name")
    p.add_argument("--flags", action="store_true",
                   help="Print only the flag list")
    args = p.parse_args()
    return cmd_dump(args)


if __name__ == "__main__":
    raise SystemExit(main())
