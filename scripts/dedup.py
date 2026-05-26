#!/usr/bin/env python3
"""
dedup.py — Content-hash dedup for repeated generations.

Given a generation request (prompt + model + seed + image), compute a hash
and check if an identical request has been generated before. If yes, return
the existing output path. If no, register the request for next time.

Storage: ~/.comfy-dedup.json
  { "<sha256>": {"output": "...", "timestamp": "...", "prompt": "...", "model": "..."} }

Usage:
  python3 dedup.py check --prompt "..." --model flux-pro [--seed 42] [--image PATH]
  python3 dedup.py register --hash <hash> --output PATH --prompt "..." --model X
  python3 dedup.py list
  python3 dedup.py purge [--days N]

For shell integration:
  HASH=$(python3 dedup.py hash --prompt "..." --model flux-pro)
  EXISTING=$(python3 dedup.py check --prompt "..." --model flux-pro)
  if [[ -n "$EXISTING" ]]; then
      echo "Already generated: $EXISTING"; exit 0
  fi
  # ... generate ...
  python3 dedup.py register --hash "$HASH" --output /path/to/output --prompt "..." --model flux-pro

Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REGISTRY = Path.home() / ".comfy-dedup.json"


def compute_hash(prompt: str, model: str, seed: str | None,
                 image: str | None, aspect: str | None) -> str:
    """SHA256 of normalized request signature."""
    h = hashlib.sha256()
    h.update(b"v1\n")  # version prefix for future schema changes
    h.update(b"prompt:" + prompt.strip().encode("utf-8") + b"\n")
    h.update(b"model:" + (model or "").encode("utf-8") + b"\n")
    h.update(b"seed:" + (seed or "").encode("utf-8") + b"\n")
    h.update(b"aspect:" + (aspect or "").encode("utf-8") + b"\n")
    if image:
        img_path = Path(image)
        if img_path.is_file():
            # Hash the image file content (small enough at <10MB)
            h.update(b"image_content:")
            with img_path.open("rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    h.update(chunk)
        else:
            h.update(b"image_path:" + image.encode("utf-8"))
    return h.hexdigest()


def load_registry() -> dict[str, dict]:
    if not REGISTRY.is_file():
        return {}
    try:
        return json.loads(REGISTRY.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def save_registry(reg: dict[str, dict]) -> None:
    REGISTRY.write_text(json.dumps(reg, indent=2))


def cmd_hash(args: argparse.Namespace) -> int:
    h = compute_hash(args.prompt or "", args.model or "", args.seed,
                     args.image, args.aspect)
    print(h)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    h = compute_hash(args.prompt or "", args.model or "", args.seed,
                     args.image, args.aspect)
    reg = load_registry()
    existing = reg.get(h)
    if existing:
        path = existing.get("output", "")
        if Path(path).is_file():
            print(path)
            return 0
        # File deleted — remove from registry
        del reg[h]
        save_registry(reg)
    # No match — print empty (so shell can detect)
    return 1


def cmd_register(args: argparse.Namespace) -> int:
    reg = load_registry()
    if args.hash:
        h = args.hash
    else:
        h = compute_hash(args.prompt or "", args.model or "", args.seed,
                         args.image, args.aspect)
    reg[h] = {
        "output": args.output,
        "prompt": args.prompt or "",
        "model": args.model or "",
        "seed": args.seed,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    save_registry(reg)
    print(f"registered: {h[:16]}... → {args.output}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    reg = load_registry()
    if not reg:
        print("(empty)")
        return 0
    for h, meta in sorted(reg.items(), key=lambda x: x[1].get("timestamp", "")):
        out = meta.get("output", "")
        model = meta.get("model", "?")
        prompt = (meta.get("prompt") or "")[:60]
        ts = meta.get("timestamp", "")
        exists = "✓" if Path(out).is_file() else "✗"
        print(f"{exists} {h[:12]}  {model:15}  {ts}  {prompt!r}")
    return 0


def cmd_purge(args: argparse.Namespace) -> int:
    reg = load_registry()
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    kept = {}
    purged = 0
    for h, meta in reg.items():
        ts = meta.get("timestamp", "")
        try:
            t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if t < cutoff:
                purged += 1
                continue
        except ValueError:
            pass
        # Also drop entries where the output file is gone
        if not Path(meta.get("output", "")).is_file():
            purged += 1
            continue
        kept[h] = meta
    save_registry(kept)
    print(f"purged {purged} entries")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Dedup helper for repeated Comfy requests")
    sub = p.add_subparsers(dest="cmd", required=True)

    for cmd_name in ("hash", "check"):
        sp = sub.add_parser(cmd_name)
        sp.add_argument("--prompt", required=True)
        sp.add_argument("--model", required=True)
        sp.add_argument("--seed")
        sp.add_argument("--image")
        sp.add_argument("--aspect")
        sp.set_defaults(func=cmd_hash if cmd_name == "hash" else cmd_check)

    p_reg = sub.add_parser("register")
    p_reg.add_argument("--hash")
    p_reg.add_argument("--prompt")
    p_reg.add_argument("--model")
    p_reg.add_argument("--seed")
    p_reg.add_argument("--image")
    p_reg.add_argument("--aspect")
    p_reg.add_argument("--output", required=True)
    p_reg.set_defaults(func=cmd_register)

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    p_purge = sub.add_parser("purge")
    p_purge.add_argument("--days", type=int, default=30)
    p_purge.set_defaults(func=cmd_purge)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
