"""Spot price resolution logic extracted from og_download.py."""

from loguru import logger as log
from typing import Any


class SpotPriceResolver:
    """Resolves spot prices from Yahoo Finance info dictionaries."""

    def resolve_price_and_state(self, info: dict[str, Any]) -> tuple[float, str]:
        """Resolve spot price and reason from info dict, prioritizing by market state and price availability.

        Args:
            info: Yahoo Finance ticker info dictionary

        Returns:
            Tuple of (price, reason) where reason is "{key} - {marketState}"

        Raises:
            ValueError: If no usable price fields found
        """
        state = info.get("marketState", "UNKNOWN")
        tried_keys = []

        # Try market-state specific prices first
        for key, cond in [
            ("preMarketPrice", state and state.startswith("PRE")),
            ("postMarketPrice", state and state.startswith("POST")),
            ("regularMarketPrice", True),
            ("currentPrice", True),
        ]:
            tried_keys.append(key)
            v = info.get(key)
            if isinstance(v, (int, float)) and v and v > 0 and cond:
                reason = f"{key} - {state}"
                log.debug(f"Using {key}={v} for spot price (marketState={state})")
                return v, reason

        # Try bid/ask midpoint
        bid, ask = info.get("bid"), info.get("ask")
        tried_keys.extend(["bid", "ask"])
        if all(isinstance(x, (int, float)) and x > 0 for x in (bid, ask)):
            midpoint = (bid + ask) / 2  # type: ignore
            reason = f"bid/ask midpoint - {state}"
            log.debug(f"Using bid/ask midpoint={midpoint} for spot price (bid={bid}, ask={ask})")
            return midpoint, reason

        # Fallback to previous close or open
        for key in ("regularMarketPreviousClose", "previousClose", "open"):
            tried_keys.append(key)
            v = info.get(key)
            if isinstance(v, (int, float)) and v and v > 0:
                reason = f"{key} - {state}"
                log.debug(f"Using fallback {key}={v} for spot price")
                return v, reason

        # Show what we tried and their values
        tried_values = {k: info.get(k) for k in tried_keys}
        raise ValueError(f"No usable price fields found. Tried keys: {tried_values}")

    def resolve_spot(self, info: dict[str, Any]) -> float:
        """Resolve spot price from info dict, prioritizing by market state and price availability.

        Args:
            info: Yahoo Finance ticker info dictionary

        Returns:
            Current spot price as float

        Raises:
            ValueError: If no usable price fields found
        """
        price, _ = self.resolve_price_and_state(info)
        return price

    def resolve_currency(self, info: dict[str, Any]) -> str:
        """Resolve currency from info dict.

        Args:
            info: Yahoo Finance ticker info dictionary

        Returns:
            Currency string

        Raises:
            ValueError: If no usable currency fields found
        """
        currency = info.get("currency")
        if isinstance(currency, str) and currency:
            log.debug(f"Using currency={currency} from info")
            return currency

        raise ValueError("No usable currency fields found.")
