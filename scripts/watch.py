#!/usr/bin/env python3
"""
watch.py — Background daemon for pending async Comfy jobs.

Polls jobs.py registry every interval, attempts to resume + download each
pending job. When the cloud reports the job as ready, downloads it and
marks the job completed in the registry.

Usage:
  python3 watch.py                        # one-shot poll all pending
  python3 watch.py --loop                 # continuous polling (every 60s default)
  python3 watch.py --loop --interval 30
  python3 watch.py --max-jobs 5           # max concurrent resumes

Stdlib only. Uses subprocess to call `comfy generate resume`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRY = Path.home() / ".comfy-jobs.json"
OUTPUT_ROOT = Path(os.environ.get("COMFY_OUTPUT_ROOT", str(Path.home() / "Comfy-Output")))


def load_jobs() -> list[dict[str, Any]]:
    if not REGISTRY.is_file():
        return []
    try:
        return json.loads(REGISTRY.read_text())
    except (OSError, json.JSONDecodeError):
        return []


def save_jobs(jobs: list[dict[str, Any]]) -> None:
    REGISTRY.write_text(json.dumps(jobs, indent=2))


def update_job(jobs: list[dict[str, Any]], job_id: str, **updates) -> None:
    for j in jobs:
        if j.get("id") == job_id:
            j.update(updates)
            j["completed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            return


def determine_output_path(job: dict[str, Any]) -> Path:
    """Build organized output path for resumed job."""
    model = job.get("model", "comfy")
    note = job.get("note", "")
    tag = "watched"
    # Try to extract tag hint from note
    if note and "recipe" in note:
        tag = note.split()[0].replace("-recipe", "")

    is_video = any(v in model for v in ["seedance", "pika", "runway", "vidu", "video"])
    ext = "mp4" if is_video else "png"

    month = datetime.now().strftime("%Y-%m")
    target_dir = OUTPUT_ROOT / month / tag
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"{model}_{job.get('id', 'unknown')[:12]}.{ext}"


def try_resume(job: dict[str, Any], dry_run: bool = False) -> tuple[bool, str]:
    """
    Attempt to resume an async job. Returns (success, message).
    """
    model = job.get("model")
    job_id = job.get("id")
    if not model or not job_id:
        return False, "missing model or job_id"

    out_path = determine_output_path(job)

    if dry_run:
        return True, f"would resume → {out_path}"

    cmd = ["comfy", "generate", "resume", model, job_id, "--download", str(out_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            return True, str(out_path)
        # The cloud might say "still running" — that's not a failure
        err = (result.stderr or result.stdout or "").lower()
        if "still" in err or "pending" in err or "queued" in err or "processing" in err:
            return False, "still-running"
        if "not found" in err or "expired" in err:
            return False, f"expired:{result.stderr.strip()[:120]}"
        return False, result.stderr.strip()[:200]
    except subprocess.TimeoutExpired:
        return False, "resume call timed out"
    except FileNotFoundError:
        return False, "comfy CLI not found in PATH"


def poll_once(max_jobs: int, dry_run: bool, verbose: bool) -> tuple[int, int, int]:
    """One pass over all pending jobs. Returns (resumed, still_running, expired)."""
    jobs = load_jobs()
    pending = [j for j in jobs if j.get("status") == "pending"]
    if not pending:
        if verbose:
            print(f"  no pending jobs")
        return (0, 0, 0)

    resumed = still_running = expired = 0
    pending = pending[:max_jobs]

    for j in pending:
        jid = j.get("id", "?")
        model = j.get("model", "?")
        ok, msg = try_resume(j, dry_run=dry_run)
        if ok:
            resumed += 1
            update_job(jobs, jid, status="completed", output_path=msg)
            print(f"  ✓ {model} / {jid[:16]} → {msg}")
        elif msg == "still-running":
            still_running += 1
            if verbose:
                print(f"  ⏳ {model} / {jid[:16]} — still running")
        elif msg.startswith("expired"):
            expired += 1
            update_job(jobs, jid, status="failed", error="expired")
            print(f"  ✗ {model} / {jid[:16]} — expired")
        else:
            if verbose:
                print(f"  ? {model} / {jid[:16]} — {msg}")

    if not dry_run:
        save_jobs(jobs)
    return (resumed, still_running, expired)


def main() -> int:
    p = argparse.ArgumentParser(description="Watch and auto-resume async Comfy jobs")
    p.add_argument("--loop", action="store_true", help="Continuous polling")
    p.add_argument("--interval", type=int, default=60, help="Seconds between polls")
    p.add_argument("--max-jobs", type=int, default=10, help="Max jobs per poll cycle")
    p.add_argument("--dry-run", action="store_true", help="Don't actually call comfy resume")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    if not args.loop:
        print(f"[{datetime.now().isoformat(timespec='seconds')}] poll once")
        r, s, e = poll_once(args.max_jobs, args.dry_run, args.verbose)
        print(f"summary: {r} resumed · {s} still running · {e} expired")
        return 0

    print(f"watch loop — interval {args.interval}s")
    try:
        while True:
            ts = datetime.now().isoformat(timespec="seconds")
            print(f"\n[{ts}] poll")
            r, s, e = poll_once(args.max_jobs, args.dry_run, args.verbose)
            if r or e:
                print(f"  ({r} resumed, {e} expired)")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nstopped")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
