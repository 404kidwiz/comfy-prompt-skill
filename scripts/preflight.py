#!/usr/bin/env python3
"""
preflight.py — Validate a Comfy Cloud generation BEFORE spending credits.

Checks:
  1. COMFY_API_KEY set and matches `comfyui-*` format
  2. Model exists in schema cache (or fetches if --refresh)
  3. Image input file exists if --image passed
  4. Output directory writable if --download passed
  5. (best-effort) parameter names in --params match the model's schema

Usage:
  python3 preflight.py <model> [--image PATH] [--download PATH] [--params key1=val1,key2=val2] [--refresh]

Exit codes:
  0 = pass (safe to run)
  1 = fail (one or more checks failed)
  2 = usage error

Stdlib only. Schema cache shared with schema_cache.py at ~/.comfy-cache/schemas/.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CACHE_DIR = Path.home() / ".comfy-cache" / "schemas"
API_KEY_PATTERN = re.compile(r"^comfyui-[a-z0-9]{32,}$")


def check(label: str, passed: bool, detail: str = "") -> bool:
    icon = "✅" if passed else "❌"
    line = f"  {icon} {label}"
    if detail:
        line += f": {detail}"
    print(line)
    return passed


def check_api_key() -> bool:
    key = os.environ.get("COMFY_API_KEY", "").strip()
    if not key:
        return check("COMFY_API_KEY set", False, "env var missing or empty")
    if not API_KEY_PATTERN.match(key):
        return check("COMFY_API_KEY format", False, f"expected 'comfyui-...' got {key[:10]!r}")
    return check("COMFY_API_KEY valid", True, f"{key[:12]}...")


def fetch_schema(model: str) -> dict | None:
    """Use `comfy generate schema <model>` to fetch + parse schema (best-effort)."""
    try:
        result = subprocess.run(
            ["comfy", "generate", "schema", model],
            capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return None
    if result.returncode != 0:
        return None
    return {"raw": result.stdout, "model": model}


def check_model(model: str, refresh: bool) -> tuple[bool, dict | None]:
    """Verify model exists. Use cache or refresh."""
    cache_path = CACHE_DIR / f"{model}.json"
    schema = None

    if cache_path.is_file() and not refresh:
        try:
            schema = json.loads(cache_path.read_text())
        except json.JSONDecodeError:
            schema = None

    if schema is None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        schema = fetch_schema(model)
        if schema:
            cache_path.write_text(json.dumps(schema, indent=2))

    if schema is None:
        check("Model exists", False, f"could not verify {model!r} — check `comfy generate list`")
        return False, None
    return check("Model exists", True, f"{model} (schema cached)"), schema


def check_image(image_path: str) -> bool:
    p = Path(image_path).expanduser()
    if not p.is_file():
        return check("Input image exists", False, str(p))
    return check("Input image exists", True, f"{p} ({p.stat().st_size:,}b)")


def check_download_dir(download_path: str) -> bool:
    p = Path(download_path).expanduser()
    # Strip filename placeholder ({index}, {ext}, etc.) → use parent
    parent = p.parent if "{" in p.name or "." in p.name else p
    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return check("Output dir writable", False, f"{parent}: {e}")
    if not os.access(parent, os.W_OK):
        return check("Output dir writable", False, f"{parent}: no write permission")
    return check("Output dir writable", True, str(parent))


def check_params(params: str, schema: dict | None) -> bool:
    if not params or schema is None:
        return True
    raw = schema.get("raw", "")
    pairs = [p for p in params.split(",") if "=" in p]
    if not pairs:
        return True
    all_ok = True
    for pair in pairs:
        key = pair.split("=", 1)[0].strip()
        # Best-effort: look for `--<key>` mention in schema raw text
        if f"--{key} " in raw or f"--{key}\n" in raw or f"--{key} <" in raw:
            check(f"Param --{key} valid", True)
        else:
            check(f"Param --{key} unknown", False, "not in schema (could be model-version drift)")
            all_ok = False
    return all_ok


def main() -> int:
    p = argparse.ArgumentParser(description="Pre-flight check for comfy generate calls")
    p.add_argument("model")
    p.add_argument("--image", help="Input image path (if using --image)")
    p.add_argument("--download", help="Output download path")
    p.add_argument("--params", help="key=val,key=val parameter check (best-effort)")
    p.add_argument("--refresh", action="store_true", help="Refresh schema cache")
    args = p.parse_args()

    print(f"Pre-flight for: comfy generate {args.model}")
    print()
    results = []

    results.append(check_api_key())
    model_ok, schema = check_model(args.model, args.refresh)
    results.append(model_ok)

    if args.image:
        results.append(check_image(args.image))
    if args.download:
        results.append(check_download_dir(args.download))
    if args.params:
        results.append(check_params(args.params, schema))

    print()
    failed = sum(1 for r in results if not r)
    if failed == 0:
        print(f"✅ All {len(results)} checks passed — safe to run")
        return 0
    print(f"❌ {failed}/{len(results)} checks failed — DO NOT run yet")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
