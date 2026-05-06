import ccxt.async_support as ccxt
import asyncio
from datetime import datetime
from core.models import Ticker
from plugins.base import DataSource


class CCXTAdapter(DataSource):
    def __init__(self, exchanges: list[str], rate_limit: bool = True):
        self.exchange_names = exchanges
        self.exchanges: dict[str, ccxt.Exchange] = {}
        for name in exchanges:
            exchange_class = getattr(ccxt, name, None)
            if exchange_class is None:
                raise ValueError(f"Exchange '{name}' not supported by ccxt")
            self.exchanges[name] = exchange_class({"enableRateLimit": rate_limit})

    async def connect(self):
        await asyncio.gather(
            *[ex.load_markets() for ex in self.exchanges.values()],
            return_exceptions=True
        )

    async def fetch_tickers(self, symbols: list[str]) -> dict[str, dict[str, Ticker]]:
        result = {}
        tasks = {
            name: self._safe_fetch(ex, symbols)
            for name, ex in self.exchanges.items()
        }
        responses = await asyncio.gather(*tasks.values())
        for name, tickers in zip(tasks.keys(), responses):
            if tickers:
                result[name] = tickers
        return result

    async def _safe_fetch(self, exchange, symbols) -> dict[str, Ticker]:
        try:
            raw = await exchange.fetch_tickers(symbols)
            return {
                symbol: Ticker(
                    exchange=exchange.id,
                    symbol=symbol,
                    bid=t.get("bid") or 0,
                    ask=t.get("ask") or 0,
                    bid_volume=t.get("bidVolume") or 0,
                    ask_volume=t.get("askVolume") or 0,
                    timestamp=datetime.now(),
                )
                for symbol, t in raw.items()
                if t.get("bid") and t.get("ask")
            }
        except Exception:
            return {}

    async def get_exchange_names(self) -> list[str]:
        return self.exchange_names

    async def close(self):
        await asyncio.gather(
            *[ex.close() for ex in self.exchanges.values()],
            return_exceptions=True
        )
