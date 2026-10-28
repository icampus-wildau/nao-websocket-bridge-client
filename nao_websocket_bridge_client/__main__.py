"""Print RMS for each PCM chunk from a NAO bridge.

Example:
    uv run python -m nao_websocket_bridge_client --url ws://192.168.2.50:8765
"""

from __future__ import annotations

import argparse
import asyncio
import math
import sys
from array import array

from nao_websocket_bridge_client.stream import iter_bridge_messages

PCM16_FULL_SCALE = 32768.0


def calculate_rms(pcm: bytes) -> tuple[float, float]:
    if not pcm:
        return 0.0, -math.inf
    samples = array("h")
    samples.frombytes(pcm)
    if sys.byteorder != "little":
        samples.byteswap()
    mean_square = sum(sample * sample for sample in samples) / len(samples)
    rms = math.sqrt(mean_square)
    normalized_rms = rms / PCM16_FULL_SCALE
    dbfs = 20.0 * math.log10(max(normalized_rms, 1e-12))
    return rms, dbfs


async def stream_audio(url: str) -> None:
    print(f"Connecting to {url} ...")
    async for kind, payload in iter_bridge_messages(url):
        if kind == "format":
            audio_format = payload
            assert isinstance(audio_format, dict)
            print(
                "Connected: "
                f"{audio_format['sample_rate']} Hz, "
                f"{audio_format['channels']} channel, "
                f"{audio_format['encoding']}"
            )
            continue
        if kind == "text":
            print(f"Control message: {payload}")
            continue
        assert isinstance(payload, bytes)
        rms, dbfs = calculate_rms(payload)
        normalized_rms = rms / PCM16_FULL_SCALE
        print(
            f"RMS: {rms:8.1f} | "
            f"normalized: {normalized_rms:.4f} | "
            f"dBFS: {dbfs:6.1f} | "
            f"bytes: {len(payload)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Listen to the NAO WebSocket bridge")
    parser.add_argument(
        "--url",
        default="ws://192.168.2.50:8765",
        help="Bridge WebSocket URL (default: ws://192.168.2.50:8765)",
    )
    args = parser.parse_args()
    try:
        asyncio.run(stream_audio(args.url))
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as exc:
        print(f"Audio bridge client failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
