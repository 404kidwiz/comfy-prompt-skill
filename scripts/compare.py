#!/usr/bin/env python3
"""
compare.py — Multi-model A/B generation helper.

Runs the same prompt on 2–4 different models simultaneously (or sequentially),
saves outputs into a comparison folder, and prints a summary table.

Usage:
  python3 compare.py <prompt> --models <m1> <m2> [m3] [m4]
                     [--aspect_ratio RATIO]
                     [--tag TAG]
                     [--image PATH]         # for i2i models
                     [--seq]               # sequential instead of parallel (default: parallel)
                     [--no-open]           # skip auto-open

Examples:
  python3 compare.py "cinematic portrait, rain-soaked detective" \\
      --models flux-pro flux-ultra nano-banana

  python3 compare.py "product hero on white" \\
      --models flux-ultra stability-ultra dalle \\
      --aspect_ratio 1:1 --tag product-ab

  python3 compare.py "same character, three-quarter back" \\
      --models flux-kontext flux-kontext-max \\
      --image /tmp/hero.png

Stdlib only. Requires COMFY_API_KEY.
Output: ~/Comfy-Output/<YYYY-MM>/<tag>/compare_<timestamp>/
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

SKILL_DIR = Path.home() / ".claude" / "skills" / "comfy-prompt"
SCRIPTS = SKILL_DIR / "scripts"


def check_api_key() -> None:
    if not os.environ.get("COMFY_API_KEY"):
        print("error: COMFY_API_KEY not set", file=sys.stderr)
        sys.exit(1)


def build_compare_dir(tag: str) -> Path:
    root = Path(os.environ.get("COMFY_OUTPUT_ROOT", str(Path.home() / "Comfy-Output")))
    month = datetime.now().strftime("%Y-%m")
    ts = datetime.now().strftime("%H%M%S")
    d = root / month / tag / f"compare_{ts}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_generation(model: str, prompt: str, out_path: Path,
                   aspect_ratio: str, image: str | None) -> dict[str, Any]:
    """Run one comfy generate call and return result info."""
    t0 = time.time()
    cmd = [
        "comfy", "generate", model,
        "--prompt", prompt,
    ]
    # Translate aspect to model-specific flags (--width/--height/--ratio/--size/...)
    import sys as _sys
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from aspect_flags import aspect_flags_for
        cmd += aspect_flags_for(model, aspect_ratio)
    except ImportError:
        # Fallback: try --aspect_ratio (works for stability, ideogram, reve, vidu, etc)
        cmd += ["--aspect_ratio", aspect_ratio]
    cmd += ["--download", str(out_path)]
    if image:
        cmd += ["--image", image]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - t0
        if result.returncode == 0:
            return {
                "model": model,
                "status": "ok",
                "output": str(out_path),
                "elapsed": elapsed,
                "stderr": result.stderr.strip()[:200],
            }
        else:
            return {
                "model": model,
                "status": "error",
                "output": None,
                "elapsed": elapsed,
                "error": (result.stderr or result.stdout).strip()[:200],
            }
    except subprocess.TimeoutExpired:
        return {
            "model": model,
            "status": "timeout",
            "output": None,
            "elapsed": 300.0,
            "error": "timed out after 300s",
        }
    except Exception as e:
        return {
            "model": model,
            "status": "error",
            "output": None,
            "elapsed": time.time() - t0,
            "error": str(e),
        }


def print_summary(results: list[dict[str, Any]], compare_dir: Path) -> None:
    print()
    print("┌" + "─" * 70 + "┐")
    print(f"│  A/B COMPARISON RESULTS{' ' * 46}│")
    print(f"│  {compare_dir}{' ' * max(0, 67 - len(str(compare_dir)))}│")
    print("├" + "─" * 70 + "┤")
    print(f"│  {'MODEL':22} {'STATUS':8} {'TIME':7} OUTPUT{'':35}│")
    print("├" + "─" * 70 + "┤")
    for r in sorted(results, key=lambda x: x["elapsed"]):
        model = r["model"][:22]
        status = r["status"][:8]
        elapsed = f"{r['elapsed']:.1f}s"
        output = (r.get("output") or r.get("error") or "")[:35]
        print(f"│  {model:22} {status:8} {elapsed:7} {output:35}│")
    print("└" + "─" * 70 + "┘")
    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"\n  {ok_count}/{len(results)} succeeded  •  dir: {compare_dir}\n")


def auto_open(path: Path) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", str(path)], check=False)


def main() -> int:
    check_api_key()

    p = argparse.ArgumentParser(
        description="Run same prompt on multiple Comfy models for side-by-side comparison"
    )
    p.add_argument("prompt", help="The generation prompt")
    p.add_argument("--models", nargs="+", required=True,
                   help="2–4 model names to compare")
    p.add_argument("--aspect_ratio", default="1:1",
                   help="Aspect ratio for all models (default: 1:1)")
    p.add_argument("--tag", default="compare",
                   help="Output tag for folder naming (default: 'compare')")
    p.add_argument("--image", help="Reference image path (for i2i models)")
    p.add_argument("--seq", action="store_true",
                   help="Run sequentially instead of in parallel")
    p.add_argument("--no-open", action="store_true",
                   help="Skip auto-opening the output directory")
    args = p.parse_args()

    if len(args.models) < 2:
        print("error: need at least 2 models to compare", file=sys.stderr)
        return 1
    if len(args.models) > 4:
        print("warning: only first 4 models used", file=sys.stderr)
        args.models = args.models[:4]

    compare_dir = build_compare_dir(args.tag)
    print(f"compare dir: {compare_dir}")
    print(f"models: {', '.join(args.models)}")
    print(f"aspect: {args.aspect_ratio}")
    if args.image:
        print(f"image: {args.image}")
    print()

    # Build output paths
    jobs = []
    for model in args.models:
        ext = "mp4" if any(v in model for v in ["vid", "pika", "runway", "seedance", "vidu"]) else "png"
        out = compare_dir / f"{model}.{ext}"
        jobs.append((model, out))

    results: list[dict[str, Any]] = []

    if args.seq:
        # Sequential
        for model, out in jobs:
            print(f"  generating: {model} ...", flush=True)
            r = run_generation(model, args.prompt, out, args.aspect_ratio, args.image)
            results.append(r)
            status = "✅" if r["status"] == "ok" else "❌"
            print(f"  {status} {model}  ({r['elapsed']:.1f}s)")
    else:
        # Parallel
        print(f"  running {len(jobs)} models in parallel ...", flush=True)
        with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
            futures = {
                executor.submit(run_generation, model, args.prompt, out,
                                args.aspect_ratio, args.image): model
                for model, out in jobs
            }
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                status = "✅" if r["status"] == "ok" else "❌"
                print(f"  {status} {r['model']}  ({r['elapsed']:.1f}s)", flush=True)

    print_summary(results, compare_dir)

    # Log to jobs.py
    for r in results:
        if r["status"] == "ok" and r.get("output"):
            try:
                subprocess.run(
                    [sys.executable, str(SCRIPTS / "jobs.py"),
                     "log", r["model"], f"compare-{datetime.now().strftime('%H%M%S')}",
                     "--prompt", args.prompt[:80],
                     "--note", f"A/B compare in {compare_dir.name}"],
                    check=False, capture_output=True
                )
            except Exception:
                pass  # non-critical

    if not args.no_open and os.environ.get("COMFY_AUTO_OPEN") == "1":
        auto_open(compare_dir)

    return 0 if any(r["status"] == "ok" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
