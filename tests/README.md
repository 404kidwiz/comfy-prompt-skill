# tests/ — comfy-prompt test suite

Python unit tests + bats integration tests. All mocked — **no API calls during tests**.

## Run

```bash
# Install deps
pip install pytest
brew install bats-core   # macOS
# or: sudo apt install bats   # Linux

# Run Python tests
cd ~/.claude/skills/comfy-prompt
pytest tests/ -v

# Run bats recipe tests (dry-run mode, no spend)
bats tests/test_recipes.bats

# Run everything
pytest tests/ && bats tests/test_recipes.bats
```

## Coverage

| File | Tests |
|------|-------|
| `test_aspect_flags.py` | 8 — flux-pro /32 dims, seedance ratio+resolution, pika float, nano-banana none, dalle size, stability aspect_ratio, unknown fallback, runtime introspection |
| `test_lint.py` | 6 — known/unknown models, oversized prompt, video camera vocab, red-flag phrases, empty prompt |
| `test_jobs.py` | 4 — cost estimation, log+complete, purge, registry |
| `test_dedup.py` | 5 — hash determinism, hash sensitivity, register/check roundtrip |
| `test_translate.py` | 4 — flux→dalle, video motion adds, duration cues, family detection |
| `test_schema_introspect.py` | 7 — parse 5 schemas, detect 6 families, dimension constraints |
| `test_compose.py` | 4 — template only, all 3 layers, unknown template, map completeness |
| `test_recipes.bats` | 9 — all 8 recipes pass --dry-run, no inline --aspect_ratio remains |

## Fixtures (`conftest.py`)

- `sample_schemas` — canned schema responses for 6 model families
- `tmp_cache` — isolated cache dir for runs
- `mocked_comfy_cli` — replaces `subprocess.run` for `comfy` calls
- `isolated_registry` — isolated jobs.py / dedup.py registry per test

## CI integration

Add to `.github/workflows/test.yml`:

```yaml
name: tests
on: [push, pull_request]
jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pytest
      - run: pytest tests/ -v
  bats:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y bats
      - run: bats tests/test_recipes.bats
```

## Adding tests

1. Drop a `test_X.py` in `tests/`
2. Use the `sample_schemas` / `mocked_comfy_cli` / `isolated_registry` fixtures from conftest.py
3. Set `monkeypatch.setenv("COMFY_NO_INTROSPECT", "1")` if you need deterministic hardcoded family lookup
