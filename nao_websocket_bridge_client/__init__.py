"""Laptop client for the NAO WebSocket bridge."""

from nao_websocket_bridge_client.reconnect import (
    RECONNECT_BASE_SECS,
    RECONNECT_STABLE_SECS,
    next_reconnect_delay,
    tcp_accepts,
    wait_until_tcp_accepts,
)
from nao_websocket_bridge_client.stream import iter_bridge_messages
from nao_websocket_bridge_protocol import (
    CHANNELS,
    SAMPLE_RATE,
    SAMPLE_WIDTH_BYTES,
    validate_audio_format,
    websocket_url,
)

__all__ = [
    "CHANNELS",
    "SAMPLE_RATE",
    "SAMPLE_WIDTH_BYTES",
    "RECONNECT_BASE_SECS",
    "RECONNECT_STABLE_SECS",
    "iter_bridge_messages",
    "next_reconnect_delay",
    "tcp_accepts",
    "validate_audio_format",
    "wait_until_tcp_accepts",
    "websocket_url",
]
