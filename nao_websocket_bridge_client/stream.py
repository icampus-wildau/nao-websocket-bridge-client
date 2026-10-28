"""Read format, status, and PCM frames from a bridge WebSocket."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

import websockets

from nao_websocket_bridge_protocol import validate_audio_format


async def iter_bridge_messages(url: str) -> AsyncIterator[tuple[str, object]]:
    """Yield ``("format", dict)``, ``("text", dict)``, and ``("pcm", bytes)``.

    The first frame must be the audio format announcement. Later text frames
    are status or other JSON. Binary frames are PCM S16LE.
    """
    async with websockets.connect(url, max_size=None) as websocket:
        first = await websocket.recv()
        if not isinstance(first, str):
            raise RuntimeError("Expected audio format JSON as first WebSocket frame")
        yield ("format", validate_audio_format(json.loads(first)))

        async for message in websocket:
            if isinstance(message, str):
                yield ("text", json.loads(message))
                continue
            payload = bytes(message)
            if len(payload) % 2:
                raise RuntimeError("PCM S16LE frame has an odd byte count")
            yield ("pcm", payload)
