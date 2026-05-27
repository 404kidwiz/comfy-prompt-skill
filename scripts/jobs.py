#!/usr/bin/env python3
"""
jobs.py — Async Comfy Cloud job tracker with cost accounting.

Logs every async generation so we can poll/list without hunting through shell history.
Tracks estimated spend per job and reports running totals.

Storage: ~/.comfy-jobs.json

Usage:
  python3 jobs.py log <model> <job_id> [--prompt "..."] [--note "..."] [--cost FLOAT]
  python3 jobs.py list [--status pending|completed|failed|all]
  python3 jobs.py pending
  python3 jobs.py status <job_id>
  python3 jobs.py complete <job_id> [--output PATH] [--cost FLOAT]
  python3 jobs.py fail <job_id> [--error "..."]
  python3 jobs.py budget [--model MODEL] [--since YYYY-MM]
  python3 jobs.py purge [--days N]   # remove completed older than N days (default 30)

Storage format (JSON):
  [
    {
      "id": "<job_id>",
      "model": "seedance",
      "prompt": "...",
      "status": "pending" | "completed" | "failed",
      "started_at": "ISO8601",
      "completed_at": "ISO8601" | null,
      "output_path": "..." | null,
      "error": "..." | null,
      "note": "..." | null,
      "cost_usd": float | null
    }, ...
  ]

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REGISTRY = Path.home() / ".comfy-jobs.json"

# Cost tier estimates in USD per generation.
# Premium-first tier philosophy:
#   S — best-in-class quality (premium default)
#   A — strong premium (~70% S quality, ~50% S cost)
#   B — solid mid (reliable, fast)
#   C — bargain (drafts, iteration)
# Source: comfy-prompt/model-guide.md
COST_TIERS: dict[str, float] = {
    # ── Tier C: $0.01–0.03 (cheap, draft work) ────────────────────────
    "nano-banana": 0.01,                  # gemini-2.5-flash-image default
    "recraft": 0.03,
    "recraft-rmbg": 0.02,
    "recraft-vectorize": 0.03,
    "recraft-upscale": 0.02,
    "stability-sd3": 0.03,

    # ── Tier B: $0.03–0.08 (solid mid) ────────────────────────────────
    "flux-2": 0.06,                       # BFL Flux 2 Pro
    "flux-pro": 0.04,                     # BFL Flux Pro 1.1
    "recraft-i2i": 0.04,
    "ideogram": 0.04,
    "ideogram-edit": 0.05,
    "ideogram-bg": 0.04,
    "ideogram-reframe": 0.04,
    "ideogram-remix": 0.05,
    "stability-upscale-fast": 0.05,
    "flux-canny": 0.06,
    "flux-depth": 0.06,
    "flux-fill": 0.06,
    "flux-expand": 0.06,
    "recraft-inpaint": 0.07,
    "recraft-replace-bg": 0.07,
    "dalle": 0.08,
    "stability-upscale": 0.08,
    "flux-kontext": 0.08,

    # ── Tier A: $0.10–0.15 (high premium) ─────────────────────────────
    "flux-ultra": 0.10,                   # BFL Flux Pro 1.1 Ultra
    "stability-ultra": 0.10,
    "reve": 0.10,
    "dalle-edit": 0.10,
    "grok": 0.12,
    "flux-kontext-max": 0.12,
    "reve-edit": 0.12,
    "grok-edit": 0.15,
    "nano-banana:gemini-3-pro-image-preview": 0.15,  # Gemini 3 Pro premium variant
    "stability-upscale-creative": 0.15,
    "recraft-upscale-creative": 0.15,

    # ── Tier B video: $0.20–0.30 (entry video) ────────────────────────
    "kling": 0.20,                        # kling-v1 baseline
    "kling-v1": 0.20,
    "kling-v1-5": 0.25,
    "kling-v1-6": 0.30,
    "vidu": 0.30,
    "vidu-extend": 0.25,
    "pika": 0.30,
    "hailuo": 0.30,

    # ── Tier A video: $0.30–0.45 (cinematic) ──────────────────────────
    "runway": 0.35,
    "vidu-i2v": 0.40,
    "moonvalley-t2v": 0.40,
    "moonvalley-i2v": 0.40,
    "pika-i2v": 0.40,
    "luma": 0.40,
    "luma-i2v": 0.45,
    "runway-i2v": 0.45,
    "kling-v2-master": 0.45,
    "kling-v2-1": 0.45,
    "kling-v2-1-master": 0.50,
    "kling-v2-5-turbo": 0.40,
    "kling-v2-6": 0.55,
    "kling-lipsync": 0.50,
    "kling-extend": 0.30,
    "kling-i2v": 0.45,

    # ── Tier S video: $0.50–0.75 (top-shelf) ──────────────────────────
    "grok-video": 0.50,
    "seedance": 0.60,                     # ByteDance Seedance
    "kling-v3": 0.60,                     # Kling v3 (latest)
}

DEFAULT_COST = 0.05  # fallback if model not in table


def estimate_cost(model: str) -> float:
    """Return cost estimate for a model, using COST_TIERS."""
    return COST_TIERS.get(model.lower(), DEFAULT_COST)


def load_registry() -> list[dict[str, Any]]:
    if not REGISTRY.is_file():
        return []
    try:
        data = json.loads(REGISTRY.read_text())
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_registry(jobs: list[dict[str, Any]]) -> None:
    REGISTRY.write_text(json.dumps(jobs, indent=2))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def find_job(jobs: list[dict[str, Any]], job_id: str) -> dict[str, Any] | None:
    for j in jobs:
        if j.get("id") == job_id:
            return j
    return None


def cmd_log(args: argparse.Namespace) -> int:
    jobs = load_registry()
    if find_job(jobs, args.job_id):
        print(f"warning: job_id already logged: {args.job_id}", file=sys.stderr)
        return 1
    cost = args.cost if args.cost is not None else estimate_cost(args.model)
    jobs.append({
        "id": args.job_id,
        "model": args.model,
        "prompt": args.prompt,
        "status": "pending",
        "started_at": now_iso(),
        "completed_at": None,
        "output_path": None,
        "error": None,
        "note": args.note,
        "cost_usd": cost,
    })
    save_registry(jobs)
    print(f"logged: {args.model} / {args.job_id}  (est. ${cost:.3f})")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    jobs = load_registry()
    status_filter = args.status or "all"
    filtered = jobs if status_filter == "all" else [j for j in jobs if j.get("status") == status_filter]
    if not filtered:
        print("(no jobs)" if status_filter == "all" else f"(no {status_filter} jobs)")
        return 0
    # Sort newest first
    filtered.sort(key=lambda j: j.get("started_at", ""), reverse=True)
    for j in filtered:
        status = j.get("status", "?")
        model = j.get("model", "?")
        jid = j.get("id", "?")
        started = j.get("started_at", "")
        prompt = (j.get("prompt") or "")[:50]
        cost_str = f"${j['cost_usd']:.3f}" if j.get("cost_usd") is not None else "     "
        suffix = ""
        if status == "completed" and j.get("output_path"):
            suffix = f" → {j['output_path']}"
        if status == "failed" and j.get("error"):
            suffix = f" ✗ {j['error'][:50]}"
        print(f"[{status:9}] {cost_str:6}  {model:20} {jid[:24]:24} {started}  {prompt!r}{suffix}")
    return 0


def cmd_pending(args: argparse.Namespace) -> int:
    args.status = "pending"
    return cmd_list(args)


def cmd_status(args: argparse.Namespace) -> int:
    jobs = load_registry()
    j = find_job(jobs, args.job_id)
    if not j:
        print(f"not found: {args.job_id}", file=sys.stderr)
        return 1
    print(json.dumps(j, indent=2))
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    jobs = load_registry()
    j = find_job(jobs, args.job_id)
    if not j:
        print(f"not found: {args.job_id}", file=sys.stderr)
        return 1
    j["status"] = "completed"
    j["completed_at"] = now_iso()
    if args.output:
        j["output_path"] = args.output
    if args.cost is not None:
        j["cost_usd"] = args.cost
    save_registry(jobs)
    cost_str = f" (${j.get('cost_usd', 0):.3f})" if j.get("cost_usd") is not None else ""
    print(f"completed: {args.job_id}{cost_str}" + (f" → {args.output}" if args.output else ""))
    return 0


def cmd_fail(args: argparse.Namespace) -> int:
    jobs = load_registry()
    j = find_job(jobs, args.job_id)
    if not j:
        print(f"not found: {args.job_id}", file=sys.stderr)
        return 1
    j["status"] = "failed"
    j["completed_at"] = now_iso()
    if args.error:
        j["error"] = args.error
    # Failed jobs don't count toward spend — zero cost
    j["cost_usd"] = 0.0
    save_registry(jobs)
    print(f"failed: {args.job_id}")
    return 0


def cmd_budget(args: argparse.Namespace) -> int:
    """Show spending summary: total, by model, by month."""
    jobs = load_registry()

    # Optional filters
    since_month = args.since or ""
    model_filter = (args.model or "").lower()

    eligible = []
    for j in jobs:
        if j.get("status") == "failed":
            continue
        if model_filter and j.get("model", "").lower() != model_filter:
            continue
        started = j.get("started_at", "")
        if since_month and started < since_month:
            continue
        eligible.append(j)

    if not eligible:
        print("no jobs match filters")
        return 0

    total = sum(j.get("cost_usd") or 0.0 for j in eligible)
    pending_cost = sum(j.get("cost_usd") or 0.0 for j in eligible if j.get("status") == "pending")
    completed_cost = sum(j.get("cost_usd") or 0.0 for j in eligible if j.get("status") == "completed")

    # By model
    by_model: dict[str, tuple[int, float]] = {}
    for j in eligible:
        m = j.get("model", "unknown")
        cnt, cost = by_model.get(m, (0, 0.0))
        by_model[m] = (cnt + 1, cost + (j.get("cost_usd") or 0.0))

    # By month
    by_month: dict[str, tuple[int, float]] = {}
    for j in eligible:
        mo = (j.get("started_at") or "")[:7]  # YYYY-MM
        cnt, cost = by_month.get(mo, (0, 0.0))
        by_month[mo] = (cnt + 1, cost + (j.get("cost_usd") or 0.0))

    print(f"{'─'*50}")
    print(f"  BUDGET SUMMARY{f'  (model: {model_filter})' if model_filter else ''}{f'  (since: {since_month})' if since_month else ''}")
    print(f"{'─'*50}")
    print(f"  Total jobs  : {len(eligible)}")
    print(f"  Completed   : ${completed_cost:.4f}")
    print(f"  Pending est : ${pending_cost:.4f}")
    print(f"  Grand total : ${total:.4f}")
    print()
    print("  By model:")
    for m, (cnt, cost) in sorted(by_model.items(), key=lambda x: -x[1][1]):
        print(f"    {m:25}  {cnt:3} jobs  ${cost:.4f}")
    print()
    print("  By month:")
    for mo, (cnt, cost) in sorted(by_month.items()):
        print(f"    {mo}   {cnt:3} jobs  ${cost:.4f}")
    print(f"{'─'*50}")
    return 0


def cmd_purge(args: argparse.Namespace) -> int:
    jobs = load_registry()
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    kept = []
    purged = 0
    for j in jobs:
        if j.get("status") != "completed":
            kept.append(j)
            continue
        ts = j.get("completed_at") or j.get("started_at") or ""
        try:
            jt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if jt < cutoff:
                purged += 1
                continue
        except ValueError:
            pass
        kept.append(j)
    save_registry(kept)
    print(f"purged {purged} completed job(s) older than {args.days} days")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Comfy Cloud async job tracker with cost accounting")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="Log a new async job")
    p_log.add_argument("model")
    p_log.add_argument("job_id")
    p_log.add_argument("--prompt", default="")
    p_log.add_argument("--note", default=None)
    p_log.add_argument("--cost", type=float, default=None,
                        help="Actual cost in USD (default: estimated from model tier)")
    p_log.set_defaults(func=cmd_log)

    p_list = sub.add_parser("list", help="List jobs")
    p_list.add_argument("--status", choices=["pending", "completed", "failed", "all"])
    p_list.set_defaults(func=cmd_list)

    p_pending = sub.add_parser("pending", help="List pending jobs")
    p_pending.set_defaults(func=cmd_pending)

    p_status = sub.add_parser("status", help="Show one job")
    p_status.add_argument("job_id")
    p_status.set_defaults(func=cmd_status)

    p_complete = sub.add_parser("complete", help="Mark job completed")
    p_complete.add_argument("job_id")
    p_complete.add_argument("--output", help="Output file path")
    p_complete.add_argument("--cost", type=float, default=None,
                             help="Actual cost if different from estimate")
    p_complete.set_defaults(func=cmd_complete)

    p_fail = sub.add_parser("fail", help="Mark job failed")
    p_fail.add_argument("job_id")
    p_fail.add_argument("--error", help="Error message")
    p_fail.set_defaults(func=cmd_fail)

    p_budget = sub.add_parser("budget", help="Show spending summary")
    p_budget.add_argument("--model", help="Filter by model name")
    p_budget.add_argument("--since", metavar="YYYY-MM",
                           help="Only include jobs started in this month or later")
    p_budget.set_defaults(func=cmd_budget)

    p_purge = sub.add_parser("purge", help="Remove old completed jobs")
    p_purge.add_argument("--days", type=int, default=30)
    p_purge.set_defaults(func=cmd_purge)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
