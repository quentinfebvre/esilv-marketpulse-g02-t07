def index_by_date(prices):
    raise NotImplementedError


def align_series(instrument_prices, benchmark_prices):
    instrument_by_date = index_by_date(instrument_prices)
    benchmark_by_date = index_by_date(benchmark_prices)

    common_dates = sorted(set(instrument_by_date.keys()) & set(benchmark_by_date.keys()))

    aligned_instrument = [instrument_by_date[d] for d in common_dates]
    aligned_benchmark = [benchmark_by_date[d] for d in common_dates]

    return aligned_instrument, aligned_benchmark


def calculate_period_return(prices):
    raise NotImplementedError


def calculate_base_100(prices):
    raise NotImplementedError


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError