from __future__ import annotations

import json
from pathlib import Path
import unittest

from src.providers.bloomberg_provider import (
    fetch_bloomberg_prices,
    normalize_reference_series,
)


class TestBloombergProvider(unittest.TestCase):
    def test_valid_single_observation_normalization(self) -> None:
        fake_series = {
            "canonical_ticker": "AAPL",
            "observations": [
                {
                    "observation_date": "2026-11-18",
                    "open_value": "100.0",
                    "high_value": "112.0",
                    "low_value": "99.0",
                    "close_value": "110.0",
                    "volume_value": "1500",
                }
            ],
        }
        rows = normalize_reference_series(fake_series)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            set(row.keys()),
            {"date", "ticker", "open", "high", "low", "close", "volume"},
        )
        self.assertEqual(row["date"], "2026-11-18")
        self.assertEqual(row["ticker"], "AAPL")
        self.assertEqual(row["open"], 100.0)
        self.assertEqual(row["high"], 112.0)
        self.assertEqual(row["low"], 99.0)
        self.assertEqual(row["close"], 110.0)
        self.assertEqual(row["volume"], 1500)
        self.assertIsInstance(row["close"], float)
        self.assertIsInstance(row["volume"], int)

    def test_empty_observations_raises_value_error(self) -> None:
        bad_series = {"canonical_ticker": "AAPL", "observations": []}
        with self.assertRaises(ValueError):
            normalize_reference_series(bad_series)

    def test_missing_close_value_raises_value_error(self) -> None:
        bad_series = {
            "canonical_ticker": "AAPL",
            "observations": [
                {
                    "observation_date": "2026-11-18",
                    "open_value": 100.0,
                    "high_value": 112.0,
                    "low_value": 99.0,
                    "volume_value": 1500,
                }
            ],
        }
        with self.assertRaises(ValueError):
            normalize_reference_series(bad_series)

    def test_duplicate_dates_raises_value_error(self) -> None:
        bad_series = {
            "canonical_ticker": "AAPL",
            "observations": [
                {
                    "observation_date": "2026-11-18",
                    "open_value": 100.0,
                    "high_value": 112.0,
                    "low_value": 99.0,
                    "close_value": 110.0,
                    "volume_value": 1500,
                },
                {
                    "observation_date": "2026-11-18",
                    "open_value": 101.0,
                    "high_value": 113.0,
                    "low_value": 100.0,
                    "close_value": 111.0,
                    "volume_value": 1600,
                },
            ],
        }
        with self.assertRaises(ValueError):
            normalize_reference_series(bad_series)

    def test_live_mode_raises_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            fetch_bloomberg_prices("AAPL", mode="LIVE")

    def test_unknown_ticker_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            fetch_bloomberg_prices("MSFT", mode="APPROVED_SAMPLE")

    def test_approved_sample_matches_expected_json(self) -> None:
        aapl = fetch_bloomberg_prices("AAPL", mode="APPROVED_SAMPLE")
        sp500 = fetch_bloomberg_prices("SP500", mode="APPROVED_SAMPLE")

        self.assertGreater(len(aapl), 0)
        self.assertGreater(len(sp500), 0)
        self.assertTrue(all(row["ticker"] == "AAPL" for row in aapl))
        self.assertTrue(all(row["ticker"] == "SP500" for row in sp500))

        expected_path = Path("data/sample/bloomberg_reference_expected.json")
        with expected_path.open("r", encoding="utf-8") as handle:
            expected_payload = json.load(handle)

        self.assertEqual(aapl + sp500, expected_payload["rows"])


if __name__ == "__main__":
    unittest.main()
