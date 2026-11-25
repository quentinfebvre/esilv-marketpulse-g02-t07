from src.providers.yahoo_provider import fetch_prices_for_ticker


def run_tests() -> None:
    apple = fetch_prices_for_ticker("AAPL")
    assert len(apple) > 0
    assert apple[0]["ticker"] == "AAPL"

    sp500 = fetch_prices_for_ticker("SP500")
    assert len(sp500) > 0
    assert sp500[0]["ticker"] == "SP500"

    apple_3m = fetch_prices_for_ticker("AAPL", period="3mo", interval="1d")
    assert len(apple_3m) >= len(apple)

    try:
        fetch_prices_for_ticker("UNKNOWN")
        raise AssertionError("Expected ValueError for unknown ticker")
    except ValueError as err:
        assert "UNKNOWN" in str(err)

    print("Tous les tests de fetch_prices_for_ticker ont reussi !")


if __name__ == "__main__":
    run_tests()
