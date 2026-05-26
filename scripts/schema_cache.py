#!/usr/bin/env python3
"""
schema_cache.py — 24h cache wrapper around `comfy generate schema <model>`.

Caches raw schema output to ~/.comfy-cache/schemas/<model>.json. Refreshes if older
than 24h or if --refresh passed.

Usage:
  python3 schema_cache.py <model> [--refresh] [--ttl-hours N]
  python3 schema_cache.py list                 # list all cached models
  python3 schema_cache.py clear [<model>]      # clear cache (one or all)

Returns schema raw text on stdout. Suitable for piping or capturing.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

CACHE_DIR = Path.home() / ".comfy-cache" / "schemas"
DEFAULT_TTL_HOURS = 24


def cache_path(model: str) -> Path:
    return CACHE_DIR / f"{model}.json"


def is_fresh(path: Path, ttl_hours: int) -> bool:
    if not path.is_file():
        return False
    age = time.time() - path.stat().st_mtime
    return age < (ttl_hours * 3600)


def fetch(model: str) -> str | None:
    try:
        result = subprocess.run(
            ["comfy", "generate", "schema", model],
            capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        print("error: `comfy` CLI not found in PATH", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"error: timeout fetching schema for {model}", file=sys.stderr)
        return None
    if result.returncode != 0:
        print(f"error: comfy returned {result.returncode}: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout


def cmd_get(args: argparse.Namespace) -> int:
    path = cache_path(args.model)
    if not args.refresh and is_fresh(path, args.ttl_hours):
        data = json.loads(path.read_text())
        print(data.get("raw", ""), end="")
        return 0

    raw = fetch(args.model)
    if raw is None:
        # Fall back to stale cache if present
        if path.is_file():
            print("(using stale cache)", file=sys.stderr)
            data = json.loads(path.read_text())
            print(data.get("raw", ""), end="")
            return 0
        return 1

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "model": args.model,
        "fetched_at": time.time(),
        "raw": raw,
    }, indent=2))
    print(raw, end="")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    if not CACHE_DIR.is_dir():
        print("(cache empty)")
        return 0
    files = sorted(CACHE_DIR.glob("*.json"))
    if not files:
        print("(cache empty)")
        return 0
    now = time.time()
    for f in files:
        age_hr = (now - f.stat().st_mtime) / 3600
        marker = "✅" if age_hr < DEFAULT_TTL_HOURS else "⚠️ "
        print(f"{marker} {f.stem:25} (age {age_hr:5.1f}h)")
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    if not CACHE_DIR.is_dir():
        return 0
    if args.model:
        p = cache_path(args.model)
        if p.is_file():
            p.unlink()
            print(f"cleared: {args.model}")
        else:
            print(f"not cached: {args.model}")
        return 0
    count = 0
    for f in CACHE_DIR.glob("*.json"):
        f.unlink()
        count += 1
    print(f"cleared {count} cached schema(s)")
    return 0


def main() -> int:
    # Manual arg parsing — argparse subparsers + positional don't mix cleanly
    argv = sys.argv[1:]
    if not argv:
        print("usage: schema_cache.py <model> [--refresh] [--ttl-hours N]")
        print("       schema_cache.py list")
        print("       schema_cache.py clear [<model>]")
        return 2

    if argv[0] == "list":
        class _A: pass
        return cmd_list(_A())

    if argv[0] == "clear":
        class _A: pass
        a = _A()
        a.model = argv[1] if len(argv) > 1 else None
        return cmd_clear(a)

    # Default: get mode
    p = argparse.ArgumentParser(description="24h schema cache for comfy generate")
    p.add_argument("model", help="Model name")
    p.add_argument("--refresh", action="store_true", help="Force refresh")
    p.add_argument("--ttl-hours", type=int, default=DEFAULT_TTL_HOURS,
                   help="Cache TTL (default 24h)")
    args = p.parse_args(argv)
    return cmd_get(args)


if __name__ == "__main__":
    raise SystemExit(main())
