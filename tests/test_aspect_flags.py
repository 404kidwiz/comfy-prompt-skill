"""Tests for aspect_flags.py — schema translator."""

import os
import pytest


def test_flux_pro_width_height(mocked_comfy_cli, monkeypatch):
    """flux-pro should get --width / --height with /32-rounded values."""
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")  # use hardcoded path for determinism
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("flux-pro", "16:9")
    assert "--width" in flags
    assert "--height" in flags
    # Find width value
    w = int(flags[flags.index("--width") + 1])
    h = int(flags[flags.index("--height") + 1])
    assert w % 32 == 0, f"width {w} not multiple of 32"
    assert h % 32 == 0, f"height {h} not multiple of 32"


def test_seedance_ratio_plus_resolution(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("seedance", "9:16")
    assert "--ratio" in flags
    assert "9:16" in flags
    assert "--resolution" in flags
    assert "1080p" in flags


def test_pika_camelcase_float(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("pika", "9:16")
    assert "--aspectRatio" in flags
    # Value is a float string
    val = float(flags[flags.index("--aspectRatio") + 1])
    assert 0.5 < val < 0.6, f"9:16 should be ~0.5625, got {val}"


def test_nano_banana_no_flags(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("nano-banana", "1:1")
    assert flags == [], "nano-banana should return empty flag list"


def test_dalle_size_string(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("dalle", "16:9")
    assert "--size" in flags
    size = flags[flags.index("--size") + 1]
    assert "x" in size
    w, h = map(int, size.split("x"))
    assert w > h, "16:9 should be wider than tall"


def test_stability_aspect_ratio_str(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("stability-ultra", "9:16")
    assert flags == ["--aspect_ratio", "9:16"]


def test_unknown_model_fallback(monkeypatch, capsys):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from aspect_flags import aspect_flags_for
    flags = aspect_flags_for("nonexistent-model-xyz", "16:9")
    # Should emit warning + try --aspect_ratio
    captured = capsys.readouterr()
    assert "warning" in captured.err.lower() or "unknown" in captured.err.lower()
    assert "--aspect_ratio" in flags or flags == []


def test_runtime_introspection_flux_pro(mocked_comfy_cli, tmp_path, monkeypatch):
    """When introspection works, flux-pro should still get width/height."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("COMFY_NO_INTROSPECT", raising=False)
    # Re-import to clear module cache
    import importlib
    import aspect_flags
    importlib.reload(aspect_flags)
    flags = aspect_flags.aspect_flags_for("flux-pro", "1:1")
    assert "--width" in flags
    assert "--height" in flags
