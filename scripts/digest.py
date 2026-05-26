#!/usr/bin/env python3
"""
digest.py — Generate weekly/monthly usage digest from jobs.py registry.

Outputs:
  - Total spend
  - Top 5 models by spend
  - Top 5 models by count
  - Fail rate
  - Avg latency (started → completed)
  - Prompt theme analysis (top recurring keywords)
  - Daily breakdown (sparkline)

Usage:
  python3 digest.py week
  python3 digest.py month [--month 2026-05]
  python3 digest.py all
  python3 digest.py week --out ~/Comfy-Output/_digests/

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REGISTRY = Path.home() / ".comfy-jobs.json"
DEFAULT_OUT = Path.home() / "Comfy-Output" / "_digests"


def load_jobs() -> list[dict[str, Any]]:
    if not REGISTRY.is_file():
        return []
    try:
        data = json.loads(REGISTRY.read_text())
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def parse_iso(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def filter_window(jobs: list[dict[str, Any]], period: str,
                  month_override: str | None) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    if period == "all":
        return jobs
    if period == "week":
        cutoff = now - timedelta(days=7)
        return [j for j in jobs if (d := parse_iso(j.get("started_at", ""))) and d >= cutoff]
    if period == "month":
        if month_override:
            return [j for j in jobs if (j.get("started_at") or "").startswith(month_override)]
        month_prefix = now.strftime("%Y-%m")
        return [j for j in jobs if (j.get("started_at") or "").startswith(month_prefix)]
    return jobs


def render_sparkline(values: list[float], width: int = 30) -> str:
    """Simple ASCII sparkline."""
    if not values or all(v == 0 for v in values):
        return "▁" * min(width, len(values) or 1)
    blocks = "▁▂▃▄▅▆▇█"
    vmax = max(values)
    bins = [int((v / vmax) * (len(blocks) - 1)) for v in values]
    return "".join(blocks[b] for b in bins)


def extract_keywords(prompts: list[str], top_n: int = 10) -> list[tuple[str, int]]:
    """Extract recurring meaningful keywords from prompts."""
    stop_words = {"the", "a", "an", "of", "in", "on", "at", "to", "for", "with",
                  "and", "or", "but", "by", "as", "is", "are", "was", "were", "be",
                  "from", "that", "this", "it", "its", "his", "her", "their",
                  "into", "over", "through", "across", "between"}
    counter: Counter[str] = Counter()
    for p in prompts:
        words = re.findall(r"\b[a-z]{4,}\b", (p or "").lower())
        for w in words:
            if w not in stop_words:
                counter[w] += 1
    return counter.most_common(top_n)


def compute_avg_latency(jobs: list[dict[str, Any]]) -> str:
    deltas = []
    for j in jobs:
        if j.get("status") != "completed":
            continue
        s = parse_iso(j.get("started_at", ""))
        c = parse_iso(j.get("completed_at", ""))
        if s and c:
            deltas.append((c - s).total_seconds())
    if not deltas:
        return "n/a"
    avg = sum(deltas) / len(deltas)
    if avg < 60:
        return f"{avg:.1f}s"
    if avg < 3600:
        return f"{avg / 60:.1f}m"
    return f"{avg / 3600:.1f}h"


def build_digest(jobs: list[dict[str, Any]], period: str) -> str:
    if not jobs:
        return f"# Comfy Digest — {period}\n\n(no jobs in this window)\n"

    total_cost = sum(j.get("cost_usd") or 0.0 for j in jobs)
    by_model: Counter[str] = Counter()
    cost_by_model: dict[str, float] = {}
    for j in jobs:
        m = j.get("model", "unknown")
        by_model[m] += 1
        cost_by_model[m] = cost_by_model.get(m, 0.0) + (j.get("cost_usd") or 0.0)

    statuses = Counter(j.get("status", "?") for j in jobs)
    completed = statuses.get("completed", 0)
    failed = statuses.get("failed", 0)
    pending = statuses.get("pending", 0)
    total = len(jobs)
    fail_rate = (failed / total * 100) if total else 0

    # Daily breakdown for sparkline
    daily: dict[str, float] = {}
    for j in jobs:
        d = (j.get("started_at") or "")[:10]
        if d:
            daily[d] = daily.get(d, 0.0) + (j.get("cost_usd") or 0.0)

    sorted_days = sorted(daily.keys())
    sparkline = render_sparkline([daily[d] for d in sorted_days])

    keywords = extract_keywords([j.get("prompt", "") for j in jobs])
    avg_lat = compute_avg_latency(jobs)

    lines = [
        f"# Comfy Digest — {period}",
        f"",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Window: {sorted_days[0] if sorted_days else 'n/a'} → {sorted_days[-1] if sorted_days else 'n/a'}",
        f"",
        f"## Summary",
        f"",
        f"- **Total jobs**: {total}",
        f"- **Total spend**: ${total_cost:.4f}",
        f"- **Avg cost/job**: ${(total_cost / total if total else 0):.4f}",
        f"- **Avg latency**: {avg_lat}",
        f"- **Status**: {completed} completed · {pending} pending · {failed} failed",
        f"- **Fail rate**: {fail_rate:.1f}%",
        f"",
        f"## Daily spend",
        f"",
        f"```",
        f"{sparkline}",
        f"```",
        f"",
        f"## Top models by spend",
        f"",
    ]
    for m, _cost in sorted(cost_by_model.items(), key=lambda x: -x[1])[:5]:
        cnt = by_model[m]
        lines.append(f"- `{m}` — ${_cost:.4f} ({cnt} jobs)")

    lines.extend([
        f"",
        f"## Top models by count",
        f"",
    ])
    for m, cnt in by_model.most_common(5):
        lines.append(f"- `{m}` — {cnt} jobs (${cost_by_model[m]:.4f})")

    if keywords:
        lines.extend([
            f"",
            f"## Prompt theme keywords",
            f"",
        ])
        for kw, cnt in keywords:
            lines.append(f"- `{kw}` ({cnt})")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Generate Comfy usage digest")
    p.add_argument("period", choices=["week", "month", "all"])
    p.add_argument("--month", metavar="YYYY-MM",
                   help="Override target month (only with --period month)")
    p.add_argument("--out", type=Path, help="Output directory (default: ~/Comfy-Output/_digests/)")
    p.add_argument("--stdout", action="store_true", help="Print to stdout, don't save file")
    args = p.parse_args()

    jobs = load_jobs()
    filtered = filter_window(jobs, args.period, args.month)
    digest = build_digest(filtered, args.period if not args.month else args.month)

    if args.stdout:
        print(digest)
        return 0

    out_dir = args.out or DEFAULT_OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    label = args.month if args.month else f"{args.period}-{datetime.now().strftime('%Y-%m-%d')}"
    out_file = out_dir / f"digest_{label}.md"
    out_file.write_text(digest)
    print(f"digest: {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
