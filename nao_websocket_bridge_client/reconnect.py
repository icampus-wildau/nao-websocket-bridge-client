"""TCP probe and reconnect delay for the bridge socket."""

from __future__ import annotations

import asyncio
import time

_PROBE_INTERVAL_SECS = 0.5
_PROBE_TIMEOUT_SECS = 0.3

RECONNECT_BASE_SECS = 0.5
RECONNECT_MAX_SECS = 8.0
RECONNECT_STABLE_SECS = 2.0


def next_reconnect_delay(previous: float, held_secs: float) -> float:
    """Back off when the bridge socket dies as soon as it connects.

    A stable drop retries quickly. A socket that lived only a moment is the
    other side of a replace-and-reconnect fight, so the wait doubles.
    """
    if held_secs >= RECONNECT_STABLE_SECS:
        return RECONNECT_BASE_SECS
    return min(max(previous, RECONNECT_BASE_SECS) * 2.0, RECONNECT_MAX_SECS)


async def tcp_accepts(
    host: str,
    port: int,
    timeout: float = _PROBE_TIMEOUT_SECS,
) -> bool:
    """True when ``host:port`` accepts a TCP connection."""
    try:
        _reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )
    except Exception:
        return False
    writer.close()
    try:
        await writer.wait_closed()
    except Exception:
        pass
    return True


async def wait_until_tcp_accepts(host: str, port: int, delay: float) -> None:
    """Wait up to ``delay`` seconds, returning early once the port accepts."""
    if delay <= 0:
        return
    deadline = time.monotonic() + delay
    while True:
        if await tcp_accepts(host, port):
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return
        await asyncio.sleep(min(_PROBE_INTERVAL_SECS, remaining))
