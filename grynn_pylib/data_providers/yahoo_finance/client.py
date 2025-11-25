"""Yahoo Finance client for API interactions."""

from datetime import datetime
from datetime import timedelta
from loguru import logger as log
from typing import Any

import inflection
import pandas as pd
import pytz
import yfinance as yf

from .spot_resolver import SpotPriceResolver


# Module-level spot resolver instance
_spot_resolver = SpotPriceResolver()


def get_spot_price(ticker: str | yf.Ticker) -> tuple[float, datetime, str, str]:
    """Get spot price information for a ticker.

    Args:
        ticker: Ticker symbol as string or yfinance.Ticker object

    Returns:
        Tuple of (price, timestamp, currency, kind) where:
        - price: Current spot price as float
        - timestamp: Time when price was recorded
        - currency: Currency code (e.g., "USD")
        - kind: Price type (e.g., "regularMarketPrice", "postMarketPrice", "previousClose")

    Example:
        >>> price, ts, currency, kind = get_spot_price("AAPL")
        >>> print(f"{price} {currency} ({kind})")
        150.25 USD (regularMarketPrice)
    """
    # Convert string to Ticker object if needed
    if isinstance(ticker, str):
        ticker = yf.Ticker(ticker)

    info = ticker.info

    # Get price and reason (format: "key - marketState")
    price, reason = _spot_resolver.resolve_price_and_state(info)

    # Extract the price kind from reason (before the " - ")
    kind = reason.split(" - ")[0] if " - " in reason else reason

    # Get currency
    currency = _spot_resolver.resolve_currency(info)

    # Get timestamp - try different fields
    timestamp = None
    for ts_key in ("regularMarketTime", "postMarketTime", "preMarketTime"):
        if ts_key in info and info[ts_key]:
            timestamp = datetime.fromtimestamp(info[ts_key])
            break

    # Fallback to current time if no timestamp found
    if timestamp is None:
        log.warning(f"No timestamp found in info for {info.get('symbol')}, using current time")
        timestamp = datetime.now()

    log.debug(f"Resolved spot price for {info.get('symbol')}: {price} {currency} ({kind}) at {timestamp}")

    return price, timestamp, currency, kind


def get_ticker_info(ticker_str: str) -> dict[str, Any]:
    """Get basic ticker information.

    Args:
        ticker_str: Ticker symbol (e.g., 'AAPL')

    Returns:
        Dictionary containing ticker info
    """
    ticker = yf.Ticker(ticker_str)
    return ticker.info


def get_available_dates(ticker_str: str) -> list[str]:
    """Get available option expiration dates for a ticker.

    Args:
        ticker_str: Ticker symbol (e.g., 'AAPL')

    Returns:
        List of date strings in YYYY-MM-DD format

    Raises:
        Exception: If no options data available
    """
    ticker = yf.Ticker(ticker_str)
    try:
        available_dates = ticker.options
        if not available_dates:
            raise ValueError(f"No options data available for {ticker_str}")
        return list(available_dates)
    except Exception as e:
        log.error(f"Failed to retrieve option chains for {ticker_str}: {e}")
        raise


def get_option_chain(
    ticker_str: str, date_str: str, tz: pytz.BaseTzInfo = pytz.timezone("US/Central")
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Download option chain for a given date and enhance it with additional data.

    Args:
        ticker_str: Ticker symbol (e.g., 'AAPL')
        date_str: Expiration date in YYYY-MM-DD format
        tz: Timezone for calculations (default: US/Central)

    Returns:
        Tuple of (calls_df, puts_df, info_dict)
    """
    ticker = yf.Ticker(ticker_str)
    log.info(f"Retrieving option chain for {ticker_str} on {date_str}")

    calls, puts, info = ticker.option_chain(date_str)

    # Resolve spot price
    spot = _spot_resolver.resolve_spot(info)
    assert spot > 0, "Could not get spot price from currentPrice || regularMarketPrice || previousClose"

    # Compute days to expiry (DTE)
    # Default option expiry is 3pm CST (index options are 3:15pm CST/CDT)
    date_expiry = tz.localize(datetime.strptime(date_str, "%Y-%m-%d") + timedelta(hours=15))
    current_timestamp_tz = datetime.now(tz)

    # Settlement happens one day after expiry
    # So an option expiring today is settled tomorrow
    dte = (date_expiry - current_timestamp_tz).days + 1

    # info dict names are not converted to snake_case here

    # Add common fields to both dataframes
    for df in [calls, puts]:
        df["dte"] = dte
        df["expiry"] = date_expiry
        df["spot"] = spot
        df["ul_fifty_two_week_low"] = info.get("fiftyTwoWeekLow")
        df["ul_fifty_two_week_high"] = info.get("fiftyTwoWeekHigh")
        df["synced_at"] = current_timestamp_tz
        df["underlying_symbol"] = info.get("symbol")

        # Convert column names to snake_case
        df.columns = [inflection.underscore(col) for col in df.columns]

        # Convert 'in_the_money' to boolean
        df["in_the_money"] = df["in_the_money"].map({"True": True, "False": False}).astype(bool)

        # Set contract_symbol as index (verify_integrity => ensure no duplicates)
        df.set_index("contract_symbol", inplace=True, verify_integrity=True)

        # Rename columns - making them easier to work with
        df.rename(columns={"last_price": "last", "implied_volatility": "iv"}, inplace=True)

    return calls, puts, info
