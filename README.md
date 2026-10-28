# nao-websocket-bridge-client

Laptop client for the process that runs on the NAO. It speaks `nao-websocket-bridge-protocol`: a format announcement, binary PCM, and periodic status.

This package does not talk to NAOqi and does not know about Pipecat. Speech, motion, and buttons stay on port 9559 through `naoqi-control`. The bridge is the realtime stream.

```python
from nao_websocket_bridge_client import iter_bridge_messages, websocket_url

url = websocket_url("192.168.2.50", 8765, token="")
async for kind, payload in iter_bridge_messages(url):
    ...
```

`tcp_accepts` and `wait_until_tcp_accepts` probe the bridge port. `next_reconnect_delay` is the backoff for a socket that drops as soon as it connects.

`python -m nao_websocket_bridge_client --url ws://ROBOT:8765` prints RMS for each PCM chunk.

## Local development

From the other project, with the checkouts side by side:

```bash
uv add --editable ../nao-websocket-bridge-client
```

Restore that project's `pyproject.toml` and lockfile before committing. The committed dependency stays the PyPI release.
