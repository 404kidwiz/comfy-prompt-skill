#!/usr/bin/env python3
"""
refs.py — Reference image library manager.

Curated library of brand/style/character references. Each ref gets a slug,
tags, description, and path. `refs use <slug>` returns the path for piping
into `comfy generate --image`.

Storage: ~/.comfy-refs/
  - refs.json — index
  - assets/    — copied images

Usage:
  refs add <slug> <path> [--desc "..."] [--tags brand,nova,hero]
  refs list [--tag TAG]
  refs use <slug>    # prints absolute path → pipe into --image
  refs show <slug>
  refs rm <slug>
  refs tag <slug> --add TAG  | --remove TAG

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path.home() / ".comfy-refs"
INDEX = ROOT / "refs.json"
ASSETS_DIR = ROOT / "assets"


def ensure_init() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX.is_file():
        INDEX.write_text(json.dumps({}, indent=2))


def load_index() -> dict[str, dict[str, Any]]:
    ensure_init()
    try:
        return json.loads(INDEX.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def save_index(idx: dict[str, dict[str, Any]]) -> None:
    INDEX.write_text(json.dumps(idx, indent=2))


def cmd_add(args: argparse.Namespace) -> int:
    ensure_init()
    src = Path(args.path).expanduser()
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 1

    idx = load_index()
    if args.slug in idx and not args.force:
        print(f"error: slug '{args.slug}' exists. Use --force to replace.", file=sys.stderr)
        return 1

    # Copy into assets dir
    dest = ASSETS_DIR / f"{args.slug}{src.suffix.lower()}"
    shutil.copy2(src, dest)

    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    idx[args.slug] = {
        "path": str(dest),
        "original": str(src),
        "description": args.desc or "",
        "tags": tags,
        "added": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    save_index(idx)
    print(f"added: {args.slug} → {dest}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    idx = load_index()
    if not idx:
        print("(no refs)")
        return 0

    rows = []
    for slug, meta in sorted(idx.items()):
        tags = meta.get("tags") or []
        if args.tag and args.tag not in tags:
            continue
        rows.append((slug, ", ".join(tags) or "-", meta.get("description", "")[:50]))

    if not rows:
        print(f"(no refs with tag '{args.tag}')")
        return 0

    print(f"{'SLUG':24} {'TAGS':30} DESCRIPTION")
    for slug, tags, desc in rows:
        print(f"{slug:24} {tags:30} {desc}")
    return 0


def cmd_use(args: argparse.Namespace) -> int:
    idx = load_index()
    if args.slug not in idx:
        print(f"not found: {args.slug}", file=sys.stderr)
        return 1
    print(idx[args.slug]["path"])
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    idx = load_index()
    if args.slug not in idx:
        print(f"not found: {args.slug}", file=sys.stderr)
        return 1
    print(json.dumps(idx[args.slug], indent=2))
    return 0


def cmd_rm(args: argparse.Namespace) -> int:
    idx = load_index()
    if args.slug not in idx:
        print(f"not found: {args.slug}", file=sys.stderr)
        return 1
    path = Path(idx[args.slug]["path"])
    if path.is_file():
        path.unlink()
    del idx[args.slug]
    save_index(idx)
    print(f"removed: {args.slug}")
    return 0


def cmd_tag(args: argparse.Namespace) -> int:
    idx = load_index()
    if args.slug not in idx:
        print(f"not found: {args.slug}", file=sys.stderr)
        return 1
    tags = set(idx[args.slug].get("tags") or [])
    if args.add:
        tags.add(args.add)
    if args.remove:
        tags.discard(args.remove)
    idx[args.slug]["tags"] = sorted(tags)
    save_index(idx)
    print(f"tags for {args.slug}: {', '.join(sorted(tags)) or '(none)'}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Comfy reference image library")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a reference image")
    p_add.add_argument("slug")
    p_add.add_argument("path")
    p_add.add_argument("--desc", help="Description")
    p_add.add_argument("--tags", help="Comma-separated tags")
    p_add.add_argument("--force", action="store_true", help="Replace existing slug")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List references")
    p_list.add_argument("--tag", help="Filter by tag")
    p_list.set_defaults(func=cmd_list)

    p_use = sub.add_parser("use", help="Print path (for pipe into --image)")
    p_use.add_argument("slug")
    p_use.set_defaults(func=cmd_use)

    p_show = sub.add_parser("show", help="Show metadata for one ref")
    p_show.add_argument("slug")
    p_show.set_defaults(func=cmd_show)

    p_rm = sub.add_parser("rm", help="Remove a reference")
    p_rm.add_argument("slug")
    p_rm.set_defaults(func=cmd_rm)

    p_tag = sub.add_parser("tag", help="Manage tags on a ref")
    p_tag.add_argument("slug")
    p_tag.add_argument("--add", help="Add tag")
    p_tag.add_argument("--remove", help="Remove tag")
    p_tag.set_defaults(func=cmd_tag)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
