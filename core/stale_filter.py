from datetime import datetime, timedelta
from core.models import Ticker


def filter_stale_tickers(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    max_age_seconds: float = 5.0,
) -> dict[str, dict[str, Ticker]]:
    """Remove tickers older than max_age_seconds."""
    cutoff = datetime.now() - timedelta(seconds=max_age_seconds)
    result = {}
    for exchange, tickers in tickers_by_exchange.items():
        fresh = {
            symbol: t for symbol, t in tickers.items()
            if t.timestamp >= cutoff
        }
        if fresh:
            result[exchange] = fresh
    return result
