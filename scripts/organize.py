#!/usr/bin/env python3
"""
organize.py — Move/copy comfy outputs into a dated, tagged structure.

Default tree:
  ~/Comfy-Output/<YYYY-MM>/<tag>/<model>_<id>_<idx>.<ext>

Usage:
  # Build a download path string for `comfy generate --download`
  python3 organize.py path --model flux-pro --tag hero-renders
  → /Users/.../Comfy-Output/2026-05/hero-renders/flux-pro_{request_id}_{index}.{ext}

  # Move existing files from /tmp/ into the organized tree
  python3 organize.py move --src /tmp/*.png --tag hero-renders [--model flux-pro] [--copy]

  # Sweep ~/ComfyUI/output/ into the organized tree (local blueprint outputs)
  python3 organize.py sweep [--tag local] [--model wan-2.2] [--copy]

Env:
  COMFY_OUTPUT_ROOT  — override default ~/Comfy-Output
  COMFY_AUTO_OPEN=1  — auto-open the output directory in Finder/xdg-open after path/move/sweep

Stdlib only.
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(os.environ.get("COMFY_OUTPUT_ROOT", str(Path.home() / "Comfy-Output")))


def month_dir() -> str:
    return datetime.now().strftime("%Y-%m")


def build_dir(tag: str | None) -> Path:
    parts = [ROOT, month_dir()]
    if tag:
        parts.append(tag)
    d = Path(*parts)
    d.mkdir(parents=True, exist_ok=True)
    return d


def auto_open(path: Path) -> None:
    """Open path in system file manager if COMFY_AUTO_OPEN=1."""
    if os.environ.get("COMFY_AUTO_OPEN") != "1":
        return
    target = str(path)
    if sys.platform == "darwin":
        subprocess.run(["open", target], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", target], check=False)
    # Windows not in scope for this skill


def cmd_path(args: argparse.Namespace) -> int:
    d = build_dir(args.tag)
    name = args.model or "comfy"
    template = f"{name}_{{request_id}}_{{index}}.{{ext}}"
    print(d / template)
    auto_open(d)
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    # Expand glob patterns
    srcs: list[Path] = []
    for pattern in args.src:
        matched = [Path(p) for p in glob.glob(pattern)]
        if not matched and Path(pattern).is_file():
            matched = [Path(pattern)]
        srcs.extend(matched)

    if not srcs:
        print("no files matched", file=sys.stderr)
        return 1

    dest_dir = build_dir(args.tag)
    op = shutil.copy2 if args.copy else shutil.move
    op_name = "copied" if args.copy else "moved"

    for src in srcs:
        if not src.is_file():
            continue
        prefix = f"{args.model}_" if args.model else ""
        dest = dest_dir / f"{prefix}{src.name}"
        # Avoid clobber
        if dest.exists():
            stem, suffix = dest.stem, dest.suffix
            i = 1
            while (dest := dest_dir / f"{stem}_{i}{suffix}").exists():
                i += 1
        op(str(src), str(dest))
        print(f"{op_name}: {src} → {dest}")

    auto_open(dest_dir)
    return 0


def cmd_sweep(args: argparse.Namespace) -> int:
    comfy_out = Path.home() / "ComfyUI" / "output"
    if not comfy_out.is_dir():
        print(f"not found: {comfy_out}", file=sys.stderr)
        return 1
    # Pick up files modified in last 24h by default; user can broaden by re-running.
    cutoff_seconds = args.since_hours * 3600
    now = datetime.now().timestamp()
    candidates = [
        p for p in comfy_out.iterdir()
        if p.is_file() and (now - p.stat().st_mtime) <= cutoff_seconds
    ]
    if not candidates:
        print(f"no files in {comfy_out} modified in last {args.since_hours}h")
        return 0

    dest_dir = build_dir(args.tag or "local")
    op = shutil.copy2 if args.copy else shutil.move
    op_name = "copied" if args.copy else "moved"
    for src in candidates:
        prefix = f"{args.model}_" if args.model else ""
        dest = dest_dir / f"{prefix}{src.name}"
        if dest.exists():
            stem, suffix = dest.stem, dest.suffix
            i = 1
            while (dest := dest_dir / f"{stem}_{i}{suffix}").exists():
                i += 1
        op(str(src), str(dest))
        print(f"{op_name}: {src.name} → {dest}")

    auto_open(dest_dir)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Organize Comfy outputs into a dated structure")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_path = sub.add_parser("path", help="Print a structured --download path template")
    p_path.add_argument("--model", help="Model name for filename prefix")
    p_path.add_argument("--tag", help="Sub-folder tag (e.g. 'client-x' or 'tests')")
    p_path.set_defaults(func=cmd_path)

    p_move = sub.add_parser("move", help="Move files into the structured tree")
    p_move.add_argument("--src", nargs="+", required=True, help="Source files / glob patterns")
    p_move.add_argument("--tag", help="Sub-folder tag")
    p_move.add_argument("--model", help="Prefix model name to filename")
    p_move.add_argument("--copy", action="store_true", help="Copy instead of move")
    p_move.set_defaults(func=cmd_move)

    p_sweep = sub.add_parser("sweep", help="Sweep ~/ComfyUI/output/ into structured tree")
    p_sweep.add_argument("--tag", help="Sub-folder tag (default: 'local')")
    p_sweep.add_argument("--model", help="Prefix model name to filename")
    p_sweep.add_argument("--copy", action="store_true", help="Copy instead of move")
    p_sweep.add_argument("--since-hours", type=int, default=24, help="Files modified within this window (default 24h)")
    p_sweep.set_defaults(func=cmd_sweep)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
