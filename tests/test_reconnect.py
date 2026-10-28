from __future__ import annotations

import unittest

from nao_websocket_bridge_client import next_reconnect_delay, websocket_url


class ReconnectTests(unittest.TestCase):
    def test_stable_drop_retries_quickly(self) -> None:
        self.assertEqual(next_reconnect_delay(0.5, 10.0), 0.5)

    def test_instant_drop_backs_off(self) -> None:
        self.assertEqual(next_reconnect_delay(0.5, 0.02), 1.0)
        self.assertEqual(next_reconnect_delay(4.0, 0.02), 8.0)

    def test_url_comes_from_the_protocol(self) -> None:
        self.assertEqual(
            websocket_url("10.0.0.5", 8765, "booth-secret"),
            "ws://10.0.0.5:8765/booth-secret",
        )


if __name__ == "__main__":
    unittest.main()
