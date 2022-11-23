"""
technical exercise for ~REDACTED~

~REDACTED~
"""


import json
import logging
import math
import typing as T
from io import TextIOWrapper
from xmlrpc.client import Boolean

from utils import date_string_to_timestamp, sort_multiple


class StockPrices:
    def __init__(self, prices_path: str):
        """Class that implements stock prices

        Args:
            prices_path (str): Path to the file with the stock data
        """
        self.file_path = prices_path


    def get_prices_single(
        self,
        symbol: str,
        start_date: T.Optional[str] = None,
        end_date: T.Optional[str] = None,
    ) -> dict[T.Any, T.Any]:
        """Parses file for a single stock quote.

        Args:
            symbol (str): Stock quote symbol
            start_date (T.Optional[str], optional): Takes a start date in the MM/DD/YYYY format, None to accept all values.
            end_date (T.Optional[str], optional): Takes an end date in the MM/DD/YYYY format, None to accept all values.

        Raises:
            Exception: Raises exception in case there's no quote in file.

        Returns:
            dict[T.Any, T.Any]: Dictionary as specified in the text.
        """
        start_timestamp: float = (
            0.0 if start_date is None else date_string_to_timestamp(start_date)
        )
        end_timestamp: float = (
            math.inf if end_date is None else date_string_to_timestamp(end_date)
        )

        file: TextIOWrapper = open(self.file_path)
        lines = file.readlines()

        dates: list[str] = []  # contains dates
        timestamps: list[float] = []  # contains timestamps for the previous dates
        prices: list[T.Optional[float]] = []  # list of prices
        used: Boolean = False  # check if symbol exists on file

        for line in lines:
            tick: dict[str, float] = {}
            timestamp = 0.0
            date = ""

            prices_obj = json.loads(line)

            for key, value in prices_obj.items():
                if key == "date":
                    date = value
                    timestamp = date_string_to_timestamp(value)
                    # ignore dates outside the start and end dates
                    if timestamp > end_timestamp or timestamp < start_timestamp:
                        continue
                else:
                    tick[key] = value
                    if key == symbol:
                        used = True

            if timestamp == 0.0:
                logging.info("Line does not contain date")
                continue

            prices.append(tick.get(symbol, None))  # add price or None
            timestamps.append(timestamp)
            dates.append(date)

        if not used:
            raise Exception(f"{symbol} not in file")

        sort_multiple(timestamps, dates, prices)

        return {"dates": dates, "prices": prices}


    def get_prices_multiple(
        self,
        symbols: list[str],
        start_date: T.Optional[str] = None,
        end_date: T.Optional[str] = None,
    ) -> dict[T.Any, T.Any]:
        """Parses file for a multiple stock quotes.

        Args:
            symbol (str): Stock quote symbol list.
            start_date (T.Optional[str], optional): Takes a start date in the MM/DD/YYYY format, None to accept all values.
            end_date (T.Optional[str], optional): Takes an end date in the MM/DD/YYYY format, None to accept all values.

        Raises:
            Exception: Raises exception in case there's a missing quote in the file.

        Returns:
            dict[T.Any, T.Any]: Dictionary as specified in the text.
        """

        start_timestamp: float = (
            0.0 if start_date is None else date_string_to_timestamp(start_date)
        )
        end_timestamp: float = (
            math.inf if end_date is None else date_string_to_timestamp(end_date)
        )

        file: TextIOWrapper = open(self.file_path)
        lines = file.readlines()

        dates: list[str] = []  # contains dates
        timestamps: list[float] = []  # contains timestamps for the previous dates
        prices: dict[str, list[T.Optional[float]]] = {}  # contains lists of prices
        used_symbols: T.List[str] = []  # contains the symbols present on the file

        # create a list of prices per symbol
        for symbol in symbols:
            prices[symbol] = []

        for line in lines:
            tick: dict[str, float] = {}
            timestamp = 0.0
            date = ""

            prices_obj = json.loads(line)

            for key, value in prices_obj.items():
                if key == "date":
                    date = value
                    timestamp = date_string_to_timestamp(value)
                    # ignore dates outside the start and end dates
                    if timestamp > end_timestamp or timestamp < start_timestamp:
                        continue
                else:
                    tick[key] = value
                    if key not in used_symbols:
                        used_symbols.append(key)

            if timestamp == 0.0:
                logging.info("Line does not contain date")
                continue

            for symbol in symbols:
                prices[symbol].append(tick.get(symbol, None))  # add price or None

            timestamps.append(timestamp)
            dates.append(date)

        for symbol in symbols:
            if symbol not in used_symbols:
                raise Exception(f"{symbol} not in file")

        sort_multiple(timestamps, dates, *(prices.values()))

        return {"dates": dates, "prices": prices}
