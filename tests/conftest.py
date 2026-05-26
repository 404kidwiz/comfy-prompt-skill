"""
conftest.py — pytest fixtures for comfy-prompt skill tests.

Provides:
  - mocked_comfy_cli: mocks subprocess calls to `comfy` binary
  - tmp_cache: isolated cache dir
  - sample_schemas: canned schema responses
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts/ to path so tests can import modules directly
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))


# ── SAMPLE SCHEMAS ────────────────────────────────────────────────────────────
SAMPLE_SCHEMAS = {
    "flux-pro": """Model: flux-pro  (bfl/flux-pro-1.1/generate)
  Proxy request to BFL Flux Pro 1.1 for image generation
  partner: bfl    style: text-to-image    content-type: application/json
mode: async (bfl)

Parameters (use as `--name value`):
  * --prompt <string>
      The main text prompt for image generation
  * --width <integer>
      Width of the generated image
  * --height <integer>
      Height of the generated image
    --negative_prompt <string>
      Negative prompt
""",
    "seedance": """Model: seedance  (bytedance/seedance/generate)
  partner: bytedance    style: text-to-video    content-type: application/json
mode: async

Parameters:
  * --prompt <string>
    --image <string>
    --resolution <enum=480p|720p|1080p>
    --ratio <enum=21:9|16:9|4:3|1:1|3:4|9:16|9:21|adaptive>
    --duration <integer>
""",
    "nano-banana": """Model: nano-banana  (google/gemini-2.5-flash-image)
  partner: google    mode: sync

Parameters:
  * --prompt <string>
""",
    "pika": """Model: pika  (pika/text-to-video)
  partner: pika    mode: async

Parameters:
  * --prompt <string>
    --resolution <enum=1080p|720p>
    --aspectRatio <number>
""",
    "dalle": """Model: dalle  (openai/dalle-3)
  partner: openai    mode: sync

Parameters:
  * --prompt <string>
    --size <string>
""",
    "stability-ultra": """Model: stability-ultra  (stability/stable-image-ultra)
  partner: stability    mode: sync

Parameters:
  * --prompt <string>
    --aspect_ratio <enum=21:9|16:9|3:2|5:4|1:1|4:5|2:3|9:16|9:21>
""",
}


@pytest.fixture
def sample_schemas():
    return dict(SAMPLE_SCHEMAS)


@pytest.fixture
def tmp_cache(tmp_path, monkeypatch):
    """Isolated cache dir for tests."""
    cache = tmp_path / "schemas"
    cache.mkdir()
    monkeypatch.setenv("HOME", str(tmp_path))
    return cache


@pytest.fixture
def mocked_comfy_cli(monkeypatch, sample_schemas):
    """
    Mock subprocess.run when called with `comfy` binary.
    Returns canned schema responses for known models.
    """
    real_run = __import__("subprocess").run

    def fake_run(args, *posargs, **kwargs):
        if args and args[0] == "comfy" and len(args) >= 3 and args[1] == "generate":
            sub = args[2]
            if sub == "schema" and len(args) >= 4:
                model = args[3]
                if model in sample_schemas:
                    result = MagicMock()
                    result.returncode = 0
                    result.stdout = sample_schemas[model]
                    result.stderr = ""
                    return result
                # Unknown model
                result = MagicMock()
                result.returncode = 1
                result.stdout = ""
                result.stderr = f"unknown model: {model}\n"
                return result
            if sub == "list":
                result = MagicMock()
                result.returncode = 0
                result.stdout = "│ flux-pro │\n│ seedance │\n│ nano-banana │\n"
                result.stderr = ""
                return result
        # Pass through to real subprocess for non-comfy calls
        return real_run(args, *posargs, **kwargs)

    monkeypatch.setattr("subprocess.run", fake_run)
    return fake_run


@pytest.fixture
def isolated_registry(tmp_path, monkeypatch):
    """Isolated jobs.py / dedup.py registry."""
    monkeypatch.setenv("HOME", str(tmp_path))
    return tmp_path
