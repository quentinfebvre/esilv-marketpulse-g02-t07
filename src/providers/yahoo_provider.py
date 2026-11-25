from __future__ import annotations

import yfinance as yf

YAHOO_SYMBOL_MAPPING: dict[str, str] = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(
    symbol: str,
    canonical_ticker: str,
    period: str = "1mo",
    interval: str = "1d",
) -> list[dict]:
    history = yf.Ticker(symbol).history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )
    if history.empty:
        raise ValueError(f"No Yahoo Finance data returned for symbol {symbol}.")

    rows: list[dict] = []
    for timestamp, row in history.iterrows():
        rows.append(
            {
                "date": timestamp.strftime("%Y-%m-%d"),
                "ticker": canonical_ticker,
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
        )
    return rows


def fetch_prices_for_ticker(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
) -> list[dict]:
    if ticker not in YAHOO_SYMBOL_MAPPING:
        supported = ", ".join(sorted(YAHOO_SYMBOL_MAPPING))
        raise ValueError(
            f"Unknown ticker '{ticker}'. Supported tickers: {supported}."
        )
    yahoo_symbol = YAHOO_SYMBOL_MAPPING[ticker]
    return fetch_yahoo_prices(
        yahoo_symbol,
        ticker,
        period=period,
        interval=interval,
    )

