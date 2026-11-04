# nao-websocket-bridge-client

*Async laptop client for the microphone WebSocket on a NAO.*

![PyPI](https://img.shields.io/pypi/v/nao-websocket-bridge-client?style=flat-square)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)
![CI](https://img.shields.io/github/actions/workflow/status/icampus-wildau/nao-websocket-bridge-client/pypi.yml?style=flat-square&label=CI)
![License: Apache 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)

It reads the format announcement, PCM frames, and status messages defined by [nao-websocket-bridge-protocol](https://github.com/icampus-wildau/nao-websocket-bridge-protocol). Speech, motion, and buttons are [naoqi-control](https://github.com/icampus-wildau/naoqi-control) on ports 9559 and 9561. The process that sends audio is [nao-websocket-bridge](https://github.com/icampus-wildau/nao-websocket-bridge), on port 8765.

## Install

Python 3.10+.

```bash
uv add nao-websocket-bridge-client
# or, in an activated environment on Linux or Windows:
python -m pip install nao-websocket-bridge-client
```

The protocol package is installed with it. The robot bridge is a separate install on the NAO.

## Read the microphone

The first frame must be the audio format. Later items are PCM bytes or decoded JSON.

```python
import asyncio
from nao_websocket_bridge_client import iter_bridge_messages, websocket_url

async def main() -> None:
    url = websocket_url("192.168.2.50", 8765, token="")  # or ws://192.168.2.50:8765/choose-a-secret
    async for kind, payload in iter_bridge_messages(url):
        # kind is "format", "pcm", or "text" (status and any other JSON)
        if kind == "pcm":
            print(len(payload))

asyncio.run(main())
```

A terminal check prints RMS for each PCM chunk:

```bash
python -m nao_websocket_bridge_client --url ws://192.168.2.50:8765
```

## Probe and reconnect

```python
from nao_websocket_bridge_client import next_reconnect_delay, tcp_accepts, wait_until_tcp_accepts

open_ = await tcp_accepts("192.168.2.50", 8765)          # True when the port accepts TCP
await wait_until_tcp_accepts("192.168.2.50", 8765, 5)    # returns early, or after 5 seconds

# Held at least 2 seconds: retry after 0.5. Died immediately: double the wait, up to 8.
delay = next_reconnect_delay(previous=0.5, held_secs=0.1)
```

## Local development

```bash
uv add --editable ../nao-websocket-bridge-client
```

Restore that project's `pyproject.toml` and lockfile before committing. The committed dependency stays the PyPI release.
