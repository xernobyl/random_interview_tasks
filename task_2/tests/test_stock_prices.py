"""Tests for the class
For the purpose of brevity the test may not cover all the code.

This was mostly used for debugging and it's unfinished.
"""

from stock_prices import StockPrices


def test_single():
    """Tests the get_prices_single method.
    """

    stock = StockPrices("prices.jsonl")
    _result = stock.get_prices_single("AAPL")

    # TODO: finish this...

    assert True


def test_multiple():
    """Tests the get_prices_multiple method.
    """

    stock = StockPrices("prices.jsonl")
    _result = stock.get_prices_multiple(["AAPL", "MSFT"])

    # TODO: finish this...

    assert True
