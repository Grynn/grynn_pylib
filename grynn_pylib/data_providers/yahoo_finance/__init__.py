"""Yahoo Finance integration module.

This module provides clean interfaces for interacting with Yahoo Finance data,
including option chains, ticker information, and spot price resolution.

TODO:
- export functions:
    get_options_expiry_dates(ticker)
        => returns: list[str] (YYYY-MM-DD format)
    get_options_chain(ticker, date | dateRange="3m", enhance=True)
        => returns: tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]

Usage example:
import grynn_pylib.yahoo_finance as yfo

yfo.get_options_chain(ticker, dateRange = "3m")
    => tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] (calls, puts, info)

calls = calls.sort_values(by=["ar", "volume"], ascending=[False, False])

"""

from .client import get_spot_price, get_ticker_info, get_available_dates, get_option_chain
from .spot_resolver import SpotPriceResolver

__all__ = [
    "SpotPriceResolver",
    "get_spot_price",
    "get_ticker_info",
    "get_available_dates",
    "get_option_chain",
]
