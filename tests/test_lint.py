"""Tests for lint.py — prompt validation."""

import pytest


def test_known_model_passes(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from lint import lint_prompt
    errors, warnings = lint_prompt(
        "MCU eye-level cinematic portrait, soft window light, slight dolly in",
        model="flux-pro", gen_type="image", aspect="16:9",
    )
    assert not errors, f"clean prompt should have no errors: {errors}"


def test_unknown_model_errors(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from lint import lint_prompt
    errors, _ = lint_prompt(
        "any prompt",
        model="totally-fake-model-9000", gen_type="image", aspect=None,
    )
    assert any("unknown model" in e.lower() for e in errors)


def test_oversized_prompt(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from lint import lint_prompt
    long_prompt = "word " * 250
    errors, _ = lint_prompt(long_prompt, model="flux-pro", gen_type="image", aspect=None)
    assert any("200" in e or "words" in e.lower() for e in errors)


def test_video_missing_camera_warns(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from lint import lint_prompt
    _, warnings = lint_prompt(
        "a man stands in a room",
        model="seedance", gen_type="video", aspect="16:9",
    )
    # Should warn about missing camera vocab and weak action
    assert any("camera" in w.lower() or "action" in w.lower() for w in warnings)


def test_red_flag_phrases_warn(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from lint import lint_prompt
    _, warnings = lint_prompt(
        "epic 8k masterpiece, amazing detailed scene with great quality",
        model="flux-pro", gen_type="image", aspect=None,
    )
    assert any("weak" in w.lower() or "cliche" in w.lower() for w in warnings)


def test_empty_prompt_errors(monkeypatch):
    monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")
    from lint import lint_prompt
    errors, _ = lint_prompt(
        "x",  # 1 word
        model="flux-pro", gen_type="image", aspect=None,
    )
    assert any("vague" in e.lower() or "too" in e.lower() for e in errors)
