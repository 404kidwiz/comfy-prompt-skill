#!/usr/bin/env python3
"""
gallery.py — Auto-generate browsable HTML gallery for an output dir.

Creates index.html with thumbnail grid, prompt + model + cost overlay.
Drop-in for client previews. No external deps; pure Python + HTML/CSS.

Usage:
  python3 gallery.py <output_dir>
  python3 gallery.py ~/Comfy-Output/2026-05/client-x/ --open
  python3 gallery.py ~/Comfy-Output/2026-05/ --recurse

If a sidecar .json exists for each image (from embed.py), prompt/model/cost
metadata is pulled from there. Otherwise falls back to filename.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root {{
    --bg: #0a0a0b;
    --bg-card: #15151a;
    --bg-card-hover: #1c1c24;
    --fg: #e8e8ec;
    --fg-dim: #8a8a95;
    --accent: #7c9aff;
    --border: #25252e;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--fg);
    font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif;
    padding: 32px;
    min-height: 100vh;
  }}
  header {{
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }}
  h1 {{
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.02em;
  }}
  .meta {{ color: var(--fg-dim); font-size: 13px; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }}
  .card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: background 0.15s ease, transform 0.15s ease;
  }}
  .card:hover {{
    background: var(--bg-card-hover);
    transform: translateY(-2px);
  }}
  .card-media {{
    width: 100%;
    aspect-ratio: 1 / 1;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}
  .card-media img, .card-media video {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
  }}
  .card-body {{ padding: 14px 16px; }}
  .card-title {{
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .card-prompt {{
    color: var(--fg-dim);
    font-size: 12px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 8px;
  }}
  .card-foot {{
    display: flex;
    gap: 12px;
    font-size: 11px;
    color: var(--fg-dim);
    align-items: center;
  }}
  .pill {{
    background: rgba(124, 154, 255, 0.12);
    color: var(--accent);
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
  }}
  .cost {{ color: var(--fg-dim); }}
  .empty {{
    text-align: center;
    padding: 64px 0;
    color: var(--fg-dim);
  }}
</style>
</head>
<body>
<header>
  <div>
    <h1>{title}</h1>
    <div class="meta">{count} asset{plural} · generated {generated_at}</div>
  </div>
  <div class="meta">Total est. cost: ${total_cost:.4f}</div>
</header>
{body}
</body>
</html>
"""


def find_assets(root: Path, recurse: bool) -> list[Path]:
    """Find all image/video files in the directory."""
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".mov"}
    if recurse:
        return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    return sorted(p for p in root.iterdir() if p.is_file() and p.suffix.lower() in exts)


def get_metadata(asset: Path) -> dict:
    """Read sidecar .json metadata if present."""
    sidecar = asset.with_suffix(asset.suffix + ".json")
    if sidecar.is_file():
        try:
            return json.loads(sidecar.read_text())
        except (OSError, json.JSONDecodeError):
            pass
    # Fallback: parse filename
    name = asset.stem
    parts = name.split("_")
    return {
        "model": parts[0] if parts else "unknown",
        "prompt": "(no metadata — run embed.py to attach)",
        "cost_usd": 0.0,
    }


def render_card(asset: Path, gallery_root: Path) -> str:
    meta = get_metadata(asset)
    rel = asset.relative_to(gallery_root)
    is_video = asset.suffix.lower() in {".mp4", ".webm", ".mov"}
    if is_video:
        media = f'<video src="{rel}" controls muted loop preload="metadata"></video>'
    else:
        media = f'<img src="{rel}" alt="{asset.name}" loading="lazy">'

    prompt = meta.get("prompt", "(no prompt)")
    if len(prompt) > 200:
        prompt = prompt[:200] + "…"

    cost = meta.get("cost_usd") or 0.0
    model = meta.get("model", "unknown")

    return f"""    <div class="card">
      <div class="card-media">{media}</div>
      <div class="card-body">
        <div class="card-title">{asset.name}</div>
        <div class="card-prompt">{escape_html(prompt)}</div>
        <div class="card-foot">
          <span class="pill">{escape_html(model)}</span>
          <span class="cost">${cost:.3f}</span>
        </div>
      </div>
    </div>"""


def escape_html(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def build_gallery(root: Path, recurse: bool, out_file: Path | None) -> Path:
    assets = find_assets(root, recurse)
    cards = "\n".join(render_card(a, root) for a in assets)
    body = (f'<div class="grid">\n{cards}\n  </div>'
            if assets else '<div class="empty">No assets found.</div>')

    total_cost = 0.0
    for a in assets:
        total_cost += float(get_metadata(a).get("cost_usd") or 0.0)

    html = HTML_TEMPLATE.format(
        title=root.name,
        count=len(assets),
        plural="" if len(assets) == 1 else "s",
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        total_cost=total_cost,
        body=body,
    )

    target = out_file or (root / "index.html")
    target.write_text(html)
    return target


def main() -> int:
    p = argparse.ArgumentParser(description="Generate HTML gallery from output dir")
    p.add_argument("path", type=Path, help="Output directory")
    p.add_argument("--out", type=Path, help="Custom output HTML path (default: <path>/index.html)")
    p.add_argument("--recurse", action="store_true", help="Recurse into subdirectories")
    p.add_argument("--open", action="store_true", help="Open in browser after generating")
    args = p.parse_args()

    if not args.path.is_dir():
        print(f"error: not a directory: {args.path}", file=sys.stderr)
        return 1

    html_path = build_gallery(args.path, args.recurse, args.out)
    print(f"gallery: {html_path}")

    if args.open:
        if sys.platform == "darwin":
            subprocess.run(["open", str(html_path)], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", str(html_path)], check=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
