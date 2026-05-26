"""Tests for dedup.py — content-hash dedup."""

import pytest
from pathlib import Path


@pytest.fixture
def isolated_dedup(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    import dedup
    import importlib
    importlib.reload(dedup)
    return tmp_path


def test_hash_deterministic():
    from dedup import compute_hash
    h1 = compute_hash("test prompt", "flux-pro", None, None, "16:9")
    h2 = compute_hash("test prompt", "flux-pro", None, None, "16:9")
    assert h1 == h2


def test_hash_changes_with_prompt():
    from dedup import compute_hash
    h1 = compute_hash("prompt A", "flux-pro", None, None, None)
    h2 = compute_hash("prompt B", "flux-pro", None, None, None)
    assert h1 != h2


def test_hash_changes_with_model():
    from dedup import compute_hash
    h1 = compute_hash("same prompt", "flux-pro", None, None, None)
    h2 = compute_hash("same prompt", "seedance", None, None, None)
    assert h1 != h2


def test_hash_changes_with_seed():
    from dedup import compute_hash
    h1 = compute_hash("p", "flux-pro", "42", None, None)
    h2 = compute_hash("p", "flux-pro", "43", None, None)
    assert h1 != h2


def test_register_then_check(isolated_dedup, tmp_path):
    from dedup import compute_hash, save_registry, load_registry
    import dedup
    # Point REGISTRY at temp
    dedup.REGISTRY = isolated_dedup / "dedup.json"

    # Create a fake output file
    out = tmp_path / "out.png"
    out.write_bytes(b"fake png")

    h = compute_hash("test", "flux-pro", None, None, None)
    save_registry({h: {
        "output": str(out),
        "prompt": "test",
        "model": "flux-pro",
        "timestamp": "2026-05-26T10:00:00+00:00",
    }})

    reg = load_registry()
    assert h in reg
    assert reg[h]["output"] == str(out)
