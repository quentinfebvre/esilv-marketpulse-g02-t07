from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BLOOMBERG_IDENTIFIERS: dict[str, str] = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

REQUIRED_OBSERVATION_FIELDS: frozenset[str] = frozenset(
    {
        "observation_date",
        "open_value",
        "high_value",
        "low_value",
        "close_value",
        "volume_value",
    }
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_PATHS: tuple[Path, ...] = (
    Path("data/sample/bloomberg_reference_sample.json"),
    Path("../data/sample/bloomberg_reference_sample.json"),
    _REPO_ROOT / "data/sample/bloomberg_reference_sample.json",
)


def get_reference_sample_path() -> Path:
    for candidate in CANDIDATE_PATHS:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Approved Bloomberg reference sample not found in candidate paths: "
        + ", ".join(str(p) for p in CANDIDATE_PATHS)
    )


def load_bloomberg_reference_sample(path: Path | None = None) -> dict[str, Any]:
    sample_path = path if path is not None else get_reference_sample_path()
    with sample_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_reference_series(
    payload: dict[str, Any],
    provider_identifier: str,
) -> dict[str, Any]:
    for series in payload.get("series", []):
        if series.get("provider_identifier") == provider_identifier:
            return series
    raise ValueError(
        f"Approved Bloomberg series not found: {provider_identifier}"
    )


def validate_reference_series(series: dict[str, Any]) -> None:
    if not isinstance(series, dict):
        raise ValueError("Series payload must be a dictionary.")

    canonical_ticker = series.get("canonical_ticker")
    if not isinstance(canonical_ticker, str) or not canonical_ticker.strip():
        raise ValueError(
            "Series must contain a non-empty 'canonical_ticker'."
        )

    observations = series.get("observations")
    if not isinstance(observations, list) or len(observations) == 0:
        raise ValueError(
            f"Series '{canonical_ticker}' must contain a non-empty 'observations' list."
        )

    seen_dates: set[str] = set()
    for index, obs in enumerate(observations):
        if not isinstance(obs, dict):
            raise ValueError(
                f"Observation at index {index} in series '{canonical_ticker}' must be a dictionary."
            )

        missing = REQUIRED_OBSERVATION_FIELDS - set(obs.keys())
        if missing:
            raise ValueError(
                f"Observation at index {index} in series '{canonical_ticker}' is missing fields: "
                + ", ".join(sorted(missing))
            )

        obs_date = obs["observation_date"]
        if not isinstance(obs_date, str) or not obs_date.strip():
            raise ValueError(
                f"Observation at index {index} in series '{canonical_ticker}' has an invalid 'observation_date'."
            )

        if obs_date in seen_dates:
            raise ValueError(
                f"Duplicate observation_date '{obs_date}' found in series '{canonical_ticker}'."
            )
        seen_dates.add(obs_date)


def normalize_reference_series(series: dict[str, Any]) -> list[dict[str, Any]]:
    validate_reference_series(series)
    ticker = series["canonical_ticker"]
    rows: list[dict[str, Any]] = []
    for obs in series["observations"]:
        rows.append(
            {
                "date": str(obs["observation_date"]),
                "ticker": ticker,
                "open": float(obs["open_value"]),
                "high": float(obs["high_value"]),
                "low": float(obs["low_value"]),
                "close": float(obs["close_value"]),
                "volume": int(obs["volume_value"]),
            }
        )
    return rows


def fetch_approved_sample_prices(
    provider_identifier: str,
    sample_path: Path | None = None,
) -> list[dict[str, Any]]:
    payload = load_bloomberg_reference_sample(path=sample_path)
    series = find_reference_series(payload, provider_identifier)
    return normalize_reference_series(series)


def fetch_raw_bloomberg_history(provider_identifier: str) -> list[dict[str, Any]]:
    raise NotImplementedError(
        f"Live Bloomberg Terminal access is not active for '{provider_identifier}'."
    )


def fetch_bloomberg_prices(
    ticker: str,
    mode: str = "APPROVED_SAMPLE",
    sample_path: Path | None = None,
) -> list[dict[str, Any]]:
    if ticker not in BLOOMBERG_IDENTIFIERS:
        supported = ", ".join(sorted(BLOOMBERG_IDENTIFIERS))
        raise ValueError(
            f"Unknown ticker '{ticker}'. Supported tickers: {supported}."
        )

    provider_id = BLOOMBERG_IDENTIFIERS[ticker]

    if mode == "APPROVED_SAMPLE":
        return fetch_approved_sample_prices(provider_id, sample_path=sample_path)
    if mode == "LIVE":
        _raw = fetch_raw_bloomberg_history(provider_id)
        raise NotImplementedError("Live mode not currently active.")
    raise ValueError(f"Unrecognized Bloomberg mode: {mode}")
