# Dependency source

`nao-websocket-bridge-protocol` comes from PyPI (`>=1.0.0`).

While editing the sibling checkout, overlay it for the session:

```bash
uv add --editable ../nao-websocket-bridge-protocol
```

Restore `pyproject.toml` before committing. The commit is done when `[tool.uv.sources]` is absent.
