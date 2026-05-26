#!/usr/bin/env python3
"""
embed.py — Embed prompt + model + seed + cost into asset metadata.

For PNG images: writes tEXt chunks (model, prompt, seed, cost, timestamp).
For other formats and as a universal fallback: writes a sidecar JSON file
  next to the asset (image.png.json).

Generated assets become self-describing — gallery.py reads them back,
and you'll know what prompt produced what image 6 months later.

Usage:
  python3 embed.py <asset.png> --prompt "..." --model flux-pro [--seed 42] [--cost 0.04]
  python3 embed.py /tmp/out.mp4 --prompt "..." --model seedance --cost 0.60

  # Strip embedded metadata
  python3 embed.py <asset> --strip

  # Read existing metadata
  python3 embed.py <asset> --read

Stdlib only. PNG metadata uses zlib + tEXt chunk format directly
(no PIL dependency). Other formats use sidecar JSON.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    """Build a PNG chunk: length + type + data + CRC32."""
    crc = zlib.crc32(chunk_type + data)
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def _read_png_chunks(data: bytes) -> list[tuple[bytes, bytes]]:
    """Parse PNG chunks. Returns list of (chunk_type, chunk_data) tuples."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file")
    pos = len(PNG_SIGNATURE)
    chunks: list[tuple[bytes, bytes]] = []
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk_data = data[pos + 8:pos + 8 + length]
        chunks.append((chunk_type, chunk_data))
        pos += 12 + length  # length + type + data + CRC
        if chunk_type == b"IEND":
            break
    return chunks


def _make_text_chunk(key: str, value: str) -> bytes:
    """Build a PNG tEXt chunk: keyword \\0 text."""
    payload = key.encode("latin-1", errors="replace") + b"\x00" + value.encode("utf-8", errors="replace")
    return _png_chunk(b"tEXt", payload)


def embed_png(path: Path, meta: dict[str, Any]) -> None:
    """Inject metadata into a PNG file as tEXt chunks."""
    data = path.read_bytes()
    chunks = _read_png_chunks(data)

    # Filter out existing comfy-prompt tEXt chunks for these keys
    filtered = []
    our_keys = {"comfy_prompt", "comfy_model", "comfy_seed", "comfy_cost",
                "comfy_aspect", "comfy_timestamp"}
    for ctype, cdata in chunks:
        if ctype == b"tEXt":
            # Parse keyword
            nul = cdata.find(b"\x00")
            if nul > 0:
                key = cdata[:nul].decode("latin-1", errors="replace")
                if key in our_keys:
                    continue
        filtered.append((ctype, cdata))

    # Build new file: signature + chunks (insert tEXt before IEND)
    out = bytearray(PNG_SIGNATURE)
    for ctype, cdata in filtered:
        if ctype == b"IEND":
            # Insert our metadata chunks before IEND
            for k, v in meta.items():
                if v is not None:
                    out.extend(_make_text_chunk(f"comfy_{k}", str(v)))
        out.extend(_png_chunk(ctype, cdata))

    path.write_bytes(bytes(out))


def read_png(path: Path) -> dict[str, str]:
    """Extract comfy_* tEXt chunks from PNG."""
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        return {}
    chunks = _read_png_chunks(data)
    meta: dict[str, str] = {}
    for ctype, cdata in chunks:
        if ctype == b"tEXt":
            nul = cdata.find(b"\x00")
            if nul > 0:
                key = cdata[:nul].decode("latin-1", errors="replace")
                if key.startswith("comfy_"):
                    short_key = key[len("comfy_"):]
                    value = cdata[nul + 1:].decode("utf-8", errors="replace")
                    meta[short_key] = value
    return meta


def strip_png(path: Path) -> None:
    """Remove all comfy_* tEXt chunks from PNG."""
    data = path.read_bytes()
    chunks = _read_png_chunks(data)
    out = bytearray(PNG_SIGNATURE)
    for ctype, cdata in chunks:
        if ctype == b"tEXt":
            nul = cdata.find(b"\x00")
            if nul > 0:
                key = cdata[:nul].decode("latin-1", errors="replace")
                if key.startswith("comfy_"):
                    continue
        out.extend(_png_chunk(ctype, cdata))
    path.write_bytes(bytes(out))


def write_sidecar(path: Path, meta: dict[str, Any]) -> Path:
    """Write metadata as <path>.json sidecar."""
    sidecar = path.with_suffix(path.suffix + ".json")
    sidecar.write_text(json.dumps(meta, indent=2))
    return sidecar


def read_sidecar(path: Path) -> dict[str, Any]:
    sidecar = path.with_suffix(path.suffix + ".json")
    if sidecar.is_file():
        try:
            return json.loads(sidecar.read_text())
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def main() -> int:
    p = argparse.ArgumentParser(description="Embed Comfy metadata in image/video assets")
    p.add_argument("asset", type=Path)
    p.add_argument("--prompt", help="Generation prompt")
    p.add_argument("--model", help="Model name")
    p.add_argument("--seed", help="Random seed")
    p.add_argument("--cost", type=float, help="Estimated cost in USD")
    p.add_argument("--aspect", help="Aspect ratio")
    p.add_argument("--read", action="store_true", help="Read and print existing metadata")
    p.add_argument("--strip", action="store_true", help="Remove embedded comfy_* metadata")
    p.add_argument("--no-sidecar", action="store_true",
                   help="Skip sidecar JSON (PNG-only metadata)")
    args = p.parse_args()

    if not args.asset.is_file():
        print(f"error: not a file: {args.asset}", file=sys.stderr)
        return 1

    is_png = args.asset.suffix.lower() == ".png"

    if args.read:
        meta = read_png(args.asset) if is_png else {}
        sidecar = read_sidecar(args.asset)
        merged = {**sidecar, **meta}  # PNG chunks win over sidecar if both exist
        if not merged:
            print("(no metadata found)")
            return 1
        print(json.dumps(merged, indent=2))
        return 0

    if args.strip:
        if is_png:
            strip_png(args.asset)
            print(f"stripped PNG metadata: {args.asset}")
        sidecar = args.asset.with_suffix(args.asset.suffix + ".json")
        if sidecar.is_file():
            sidecar.unlink()
            print(f"removed sidecar: {sidecar}")
        return 0

    # Write metadata
    meta = {
        "prompt": args.prompt or "",
        "model": args.model or "",
        "seed": args.seed,
        "cost_usd": args.cost,
        "aspect": args.aspect,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    # Drop None values
    meta = {k: v for k, v in meta.items() if v is not None and v != ""}

    if not meta:
        print("error: nothing to write — provide --prompt or --model", file=sys.stderr)
        return 1

    written: list[str] = []
    if is_png:
        try:
            embed_png(args.asset, meta)
            written.append("PNG tEXt")
        except ValueError as e:
            print(f"PNG embed failed: {e}", file=sys.stderr)

    if not args.no_sidecar:
        sidecar = write_sidecar(args.asset, meta)
        written.append(f"sidecar {sidecar.name}")

    print(f"embedded ({', '.join(written)}): {args.asset.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
