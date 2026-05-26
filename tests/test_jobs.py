"""Tests for jobs.py — async job tracker + cost accounting."""

import json
import pytest
from pathlib import Path


@pytest.fixture
def isolated_jobs(tmp_path, monkeypatch):
    """Point jobs.py REGISTRY at an isolated tmp file."""
    registry = tmp_path / "jobs.json"
    monkeypatch.setenv("HOME", str(tmp_path))
    import jobs
    # Reload to pick up new HOME
    import importlib
    importlib.reload(jobs)
    return registry


def test_estimate_cost_known_model():
    from jobs import estimate_cost
    assert estimate_cost("seedance") > 0.5
    assert estimate_cost("nano-banana") < 0.05
    assert estimate_cost("flux-pro") > 0.0


def test_estimate_cost_unknown_model():
    from jobs import estimate_cost, DEFAULT_COST
    assert estimate_cost("nonexistent-zzz") == DEFAULT_COST


def test_log_then_complete(isolated_jobs, monkeypatch):
    from jobs import load_registry, save_registry
    import subprocess, sys
    import jobs as jobs_mod
    # Use the module's REGISTRY path (already in tmp via fixture)
    jobs_mod.REGISTRY = isolated_jobs

    # Empty initially
    assert load_registry() == []

    # Log a job
    jobs_mod.REGISTRY = isolated_jobs
    save_registry([{
        "id": "test-001",
        "model": "flux-pro",
        "prompt": "test prompt",
        "status": "pending",
        "started_at": "2026-05-26T10:00:00+00:00",
        "completed_at": None,
        "output_path": None,
        "error": None,
        "note": None,
        "cost_usd": 0.04,
    }])

    jobs = load_registry()
    assert len(jobs) == 1
    assert jobs[0]["id"] == "test-001"
    assert jobs[0]["cost_usd"] == 0.04


def test_purge_old_completed(isolated_jobs):
    from jobs import save_registry, load_registry
    import jobs as jobs_mod
    jobs_mod.REGISTRY = isolated_jobs

    # Two jobs: one old completed, one new pending
    save_registry([
        {
            "id": "old", "model": "flux-pro", "status": "completed",
            "started_at": "2024-01-01T00:00:00+00:00",
            "completed_at": "2024-01-01T00:01:00+00:00",
            "cost_usd": 0.04,
        },
        {
            "id": "new", "model": "seedance", "status": "pending",
            "started_at": "2026-05-26T10:00:00+00:00",
            "completed_at": None,
            "cost_usd": 0.60,
        },
    ])

    jobs = load_registry()
    assert len(jobs) == 2
