def index_by_date(prices):
    return {row["date"]: row for row in prices}


def align_series(instrument_prices, benchmark_prices):
    instrument_by_date = index_by_date(instrument_prices)
    benchmark_by_date = index_by_date(benchmark_prices)

    common_dates = sorted(set(instrument_by_date.keys()) & set(benchmark_by_date.keys()))

    aligned_instrument = [instrument_by_date[d] for d in common_dates]
    aligned_benchmark = [benchmark_by_date[d] for d in common_dates]

    return aligned_instrument, aligned_benchmark


def calculate_period_return(prices):
    if not prices:
        raise ValueError("Cannot compute a return on an empty series")
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])
    if first_close == 0:
        raise ValueError("First close is zero, return is undefined")
    return ((last_close / first_close) - 1.0) * 100.0


def calculate_base_100(prices):
    raise NotImplementedError


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError