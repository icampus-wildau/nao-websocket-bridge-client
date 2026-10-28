# nao-websocket-bridge-client

Async laptop client for the microphone WebSocket on a NAO. It reads the format announcement, PCM frames, and status messages from [nao-websocket-bridge-protocol](https://github.com/icampus-wildau/nao-websocket-bridge-protocol).

Speech, motion, and buttons are [naoqi-control](https://github.com/icampus-wildau/naoqi-control) on ports 9559 and 9561. The process that sends audio is [nao-websocket-bridge](https://github.com/icampus-wildau/nao-websocket-bridge), on port 8765.

Requires Python 3.10+.

```bash
uv add nao-websocket-bridge-client
```

## Read the microphone

The first frame must be the audio format. `iter_bridge_messages` checks it, then yields `("format", dict)`, `("pcm", bytes)`, and `("text", dict)` for status and any other JSON.

```python
import asyncio
from nao_websocket_bridge_client import iter_bridge_messages, websocket_url

async def main() -> None:
    url = websocket_url("192.168.2.50", 8765, token="")
    async for kind, payload in iter_bridge_messages(url):
        if kind == "pcm":
            print(len(payload))

asyncio.run(main())
```

With a bridge token, pass it to `websocket_url` or use `ws://192.168.2.50:8765/choose-a-secret`.

A terminal check prints RMS for each PCM chunk:

```bash
python -m nao_websocket_bridge_client --url ws://192.168.2.50:8765
```

## Probing and reconnecting

`tcp_accepts(host, port)` is true when port 8765 accepts a TCP connection. `wait_until_tcp_accepts(host, port, delay)` returns as soon as it does, or after `delay` seconds. `next_reconnect_delay(previous, held_secs)` is the wait before another attempt: a socket that stayed up at least 2 seconds retries after 0.5 seconds; one that dies immediately doubles the wait, up to 8 seconds.

## Local development

With this checkout next to the app:

```bash
uv add --editable ../nao-websocket-bridge-client
```

Restore that project's `pyproject.toml` and lockfile before committing. The committed dependency stays the PyPI release.
