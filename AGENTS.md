# Bridge client

This package reads microphone WebSocket messages, not NAOqi controls. Public usage
and the message contract are linked from [README.md](README.md).

`nao-websocket-bridge-protocol` is a PyPI dependency. To test sibling changes,
temporarily use `uv add --editable ../nao-websocket-bridge-protocol`, then restore
the pre-overlay dependency declarations and lockfile if created. The committed
diff must use the registry dependency, without a local-path source; preserve
unrelated dependency changes.

Changes to message handling should be checked against the shared protocol and
robot bridge. CI runs `python -m unittest discover -s tests -v` after installing
this package.
