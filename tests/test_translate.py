"""Tests for translate.py — cross-model prompt adapter."""


def test_flux_to_dalle_adds_photograph_prefix():
    from translate import translate, model_family
    result = translate("MCU portrait of a detective", "flux", "openai")
    # Should add "a photograph of" or rewrite MCU
    assert "photograph" in result.lower() or "medium" in result.lower()


def test_video_target_adds_motion_verb():
    from translate import translate
    result = translate("a still scene", "flux", "video", duration=10)
    # Should add a motion verb
    motion_verbs = ["dolly", "pan", "tilt", "track", "push", "pull", "drift"]
    assert any(v in result.lower() for v in motion_verbs)


def test_video_target_adds_duration_cue():
    from translate import translate
    result = translate("subject moves through frame", "flux", "video", duration=10)
    assert "10" in result or "second" in result.lower()


def test_model_family_detection():
    from translate import model_family
    assert model_family("flux-pro") == "flux"
    assert model_family("dalle") == "openai"
    assert model_family("seedance") == "video"
    assert model_family("nano-banana") == "google"
    assert model_family("unknown-zzz") == "unknown"
