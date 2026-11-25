"""Validation script for src/analytics.py (TD07 exercise)."""

from src.analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


def make_series(ticker, dates, closes):
    return [
        {"date": date, "ticker": ticker, "close": str(close)}
        for date, close in zip(dates, closes)
    ]


# Fictitious series: instrument 100 -> 110, benchmark 200 -> 210
dates = ["2026-01-01", "2026-01-02", "2026-01-03"]
instrument = make_series("TEST", dates, [100, 105, 110])
benchmark = make_series("BENCH", dates, [200, 204, 210])

# 1. Period return
instrument_return = calculate_period_return(instrument)
benchmark_return = calculate_period_return(benchmark)
assert abs(instrument_return - 10.0) < 1e-9
assert abs(benchmark_return - 5.0) < 1e-9

# 2. Base 100
base_100 = calculate_base_100(benchmark)
assert base_100[0]["value"] == 100.0
assert abs(base_100[-1]["value"] - 105.0) < 1e-9
assert base_100[-1]["date"] == "2026-01-03"
assert base_100[-1]["ticker"] == "BENCH"

# 3. Relative performance
relative = calculate_relative_performance(instrument_return, benchmark_return)
assert abs(relative - 5.0) < 1e-9

# 4. Alignment with different dates (benchmark has no 2026-01-03)
instrument_dates = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
benchmark_dates = ["2026-01-01", "2026-01-02", "2026-01-04"]
aligned_instrument, aligned_benchmark = align_series(
    make_series("TEST", instrument_dates, [100, 101, 102, 103]),
    make_series("BENCH", benchmark_dates, [200, 201, 203]),
)
expected_dates = ["2026-01-01", "2026-01-02", "2026-01-04"]
assert [row["date"] for row in aligned_instrument] == expected_dates
assert [row["date"] for row in aligned_benchmark] == expected_dates

# 5. Empty series must raise ValueError
try:
    calculate_period_return([])
except ValueError:
    pass
else:
    raise AssertionError("calculate_period_return([]) should raise ValueError")

print("All analytics validation tests passed.")