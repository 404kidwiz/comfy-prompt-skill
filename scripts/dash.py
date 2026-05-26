#!/usr/bin/env python3
"""
dash.py — Simple ANSI-based TUI dashboard for Comfy operations.

Stdlib only (no rich/textual dep). Shows:
  - Pending async jobs
  - Today's spend + month-to-date
  - Recent outputs (last 10)
  - Top models this week
  - Failed jobs (if any)

Usage:
  python3 dash.py            # one-shot snapshot
  python3 dash.py --watch    # auto-refresh every 30s

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REGISTRY = Path.home() / ".comfy-jobs.json"
OUTPUT_ROOT = Path(os.environ.get("COMFY_OUTPUT_ROOT", str(Path.home() / "Comfy-Output")))

# ANSI codes
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"


def clear() -> None:
    print("\033[2J\033[H", end="")


def hr() -> str:
    width = shutil.get_terminal_size((80, 20)).columns
    return DIM + ("─" * width) + RESET


def load_jobs() -> list[dict[str, Any]]:
    if not REGISTRY.is_file():
        return []
    try:
        return json.loads(REGISTRY.read_text())
    except (OSError, json.JSONDecodeError):
        return []


def get_recent_outputs(limit: int = 10) -> list[tuple[Path, datetime]]:
    if not OUTPUT_ROOT.is_dir():
        return []
    candidates: list[tuple[Path, datetime]] = []
    for p in OUTPUT_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg",
                                                  ".webp", ".mp4", ".webm"}:
            candidates.append((p, datetime.fromtimestamp(p.stat().st_mtime)))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:limit]


def parse_iso(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def render(jobs: list[dict[str, Any]]) -> None:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    month = now.strftime("%Y-%m")

    today_cost = 0.0
    month_cost = 0.0
    pending: list[dict[str, Any]] = []
    failed_recent: list[dict[str, Any]] = []
    model_counts: dict[str, int] = {}
    model_costs: dict[str, float] = {}

    week_cutoff = now - timedelta(days=7)

    for j in jobs:
        cost = j.get("cost_usd") or 0.0
        started = j.get("started_at") or ""
        s = parse_iso(started)
        if started.startswith(today):
            today_cost += cost
        if started.startswith(month):
            month_cost += cost

        m = j.get("model", "?")
        if s and s >= week_cutoff:
            model_counts[m] = model_counts.get(m, 0) + 1
            model_costs[m] = model_costs.get(m, 0.0) + cost

        if j.get("status") == "pending":
            pending.append(j)
        if j.get("status") == "failed" and s and s >= week_cutoff:
            failed_recent.append(j)

    # Header
    clear()
    print()
    print(f"  {BOLD}{CYAN}Comfy Dashboard{RESET}  {DIM}{now.strftime('%Y-%m-%d %H:%M:%S UTC')}{RESET}")
    print()

    # Spend gauge
    print(f"  {BOLD}Spend{RESET}")
    print(f"  {DIM}Today:{RESET}  {GREEN}${today_cost:.4f}{RESET}")
    print(f"  {DIM}Month:{RESET}  {GREEN}${month_cost:.4f}{RESET}")
    print(hr())

    # Pending jobs
    print(f"  {BOLD}Pending async jobs{RESET}  {DIM}({len(pending)}){RESET}")
    if pending:
        for j in pending[-10:]:
            jid = (j.get("id") or "")[:24]
            m = j.get("model", "?")[:18]
            cost = j.get("cost_usd") or 0.0
            prompt = (j.get("prompt") or "")[:50]
            print(f"  {YELLOW}●{RESET} {m:18}  {jid:24}  ${cost:.3f}  {DIM}{prompt}{RESET}")
    else:
        print(f"  {DIM}(none){RESET}")
    print(hr())

    # Top models this week
    print(f"  {BOLD}Top models (last 7d){RESET}")
    if model_counts:
        top = sorted(model_counts.items(), key=lambda x: -x[1])[:5]
        for m, cnt in top:
            cost = model_costs.get(m, 0.0)
            bar = "█" * min(cnt, 30)
            print(f"  {BLUE}{m:22}{RESET}  {cnt:>3}  ${cost:.4f}  {DIM}{bar}{RESET}")
    else:
        print(f"  {DIM}(no jobs in last 7 days){RESET}")
    print(hr())

    # Recent outputs
    print(f"  {BOLD}Recent outputs{RESET}")
    recent = get_recent_outputs(8)
    if recent:
        for path, mtime in recent:
            try:
                rel = path.relative_to(OUTPUT_ROOT)
            except ValueError:
                rel = path
            ts = mtime.strftime("%H:%M")
            print(f"  {MAGENTA}▸{RESET} {ts}  {rel}")
    else:
        print(f"  {DIM}(none){RESET}")

    # Failed (if any)
    if failed_recent:
        print(hr())
        print(f"  {BOLD}{RED}Failed jobs (last 7d){RESET}  {DIM}({len(failed_recent)}){RESET}")
        for j in failed_recent[-5:]:
            m = j.get("model", "?")[:18]
            err = (j.get("error") or "(no msg)")[:60]
            print(f"  {RED}✗{RESET} {m:18}  {err}")

    print()


def main() -> int:
    p = argparse.ArgumentParser(description="Comfy TUI dashboard")
    p.add_argument("--watch", action="store_true", help="Auto-refresh every 30s")
    p.add_argument("--interval", type=int, default=30, help="Refresh interval seconds")
    args = p.parse_args()

    try:
        while True:
            jobs = load_jobs()
            render(jobs)
            if not args.watch:
                return 0
            print(f"  {DIM}refreshing in {args.interval}s ... (Ctrl-C to exit){RESET}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\n{DIM}bye{RESET}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
