"""Tests for schema_introspect.py — runtime schema parsing."""

import pytest


def test_parse_flux_pro_schema(sample_schemas):
    from schema_introspect import parse_schema, detect_aspect_family
    parsed = parse_schema(sample_schemas["flux-pro"])
    assert parsed["model"] == "flux-pro"
    assert "width" in parsed["flags"]
    assert "height" in parsed["flags"]
    assert parsed["flags"]["width"]["required"] is True
    assert detect_aspect_family(parsed) == "width_height"


def test_parse_seedance_schema(sample_schemas):
    from schema_introspect import parse_schema, detect_aspect_family
    parsed = parse_schema(sample_schemas["seedance"])
    assert "ratio" in parsed["flags"]
    assert "resolution" in parsed["flags"]
    assert parsed["flags"]["ratio"]["enum"] is not None
    assert "16:9" in parsed["flags"]["ratio"]["enum"]
    assert detect_aspect_family(parsed) == "ratio_plus_resolution"


def test_parse_pika_aspectRatio(sample_schemas):
    from schema_introspect import parse_schema, detect_aspect_family
    parsed = parse_schema(sample_schemas["pika"])
    assert "aspectRatio" in parsed["flags"]
    assert detect_aspect_family(parsed) == "pika_aspect_float"


def test_parse_nano_banana_no_aspect(sample_schemas):
    from schema_introspect import parse_schema, detect_aspect_family
    parsed = parse_schema(sample_schemas["nano-banana"])
    assert detect_aspect_family(parsed) == "none"


def test_parse_dalle_size_string(sample_schemas):
    from schema_introspect import parse_schema, detect_aspect_family
    parsed = parse_schema(sample_schemas["dalle"])
    assert "size" in parsed["flags"]
    assert detect_aspect_family(parsed) == "size_string"


def test_constraints_flux_pro(sample_schemas):
    from schema_introspect import parse_schema, detect_dimension_constraints
    parsed = parse_schema(sample_schemas["flux-pro"])
    constraints = detect_dimension_constraints(parsed)
    assert constraints["multiple_of"] == 32


def test_constraints_seedance_none(sample_schemas):
    from schema_introspect import parse_schema, detect_dimension_constraints
    parsed = parse_schema(sample_schemas["seedance"])
    constraints = detect_dimension_constraints(parsed)
    assert constraints["multiple_of"] is None
