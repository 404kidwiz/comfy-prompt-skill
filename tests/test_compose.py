"""Tests for compose.py — template + vertical + style merger."""


def test_compose_with_template():
    from compose import compose_prompt
    result = compose_prompt(
        subject="matte black mug",
        template_id="product",
        vertical_id=None,
        style_id=None,
    )
    assert "matte black mug" in result["subject"]
    assert result["full"]  # non-empty composed prompt
    assert "matte black mug" in result["full"]


def test_compose_with_all_three_layers():
    from compose import compose_prompt
    result = compose_prompt(
        subject="cyberpunk detective",
        template_id="portrait",
        vertical_id="viral-hook",
        style_id="cyberpunk-blade-runner",
    )
    assert result["full"]
    assert "cyberpunk detective" in result["full"]


def test_compose_unknown_template():
    from compose import compose_prompt
    result = compose_prompt(
        subject="x",
        template_id="nonexistent-template-zzz",
        vertical_id=None,
        style_id=None,
    )
    # Should return empty/default result
    assert result["subject"] == "x"


def test_template_map_complete():
    from compose import TEMPLATE_MAP, VERTICAL_MAP, STYLE_MAP
    assert len(TEMPLATE_MAP) == 10
    assert len(VERTICAL_MAP) == 10
    assert len(STYLE_MAP) == 7
