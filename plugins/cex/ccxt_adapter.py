import ccxt
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
            self.exchanges[name] = exchange_class({
                "enableRateLimit": rate_limit,
            })

    def connect(self):
        for name, ex in self.exchanges.items():
            try:
                ex.load_markets()
                print(f"  {name}: loaded {len(ex.markets)} markets")
            except Exception as e:
                print(f"  {name}: failed ({e})")

    def fetch_tickers(self, symbols: list[str]) -> dict[str, dict[str, Ticker]]:
        result = {}
        for name, ex in self.exchanges.items():
            try:
                raw = ex.fetch_tickers(symbols)
                tickers = {}
                for symbol, t in raw.items():
                    if t.get("bid") and t.get("ask"):
                        tickers[symbol] = Ticker(
                            exchange=ex.id,
                            symbol=symbol,
                            bid=t["bid"],
                            ask=t["ask"],
                            bid_volume=t.get("bidVolume") or 0,
                            ask_volume=t.get("askVolume") or 0,
                            timestamp=datetime.now(),
                        )
                if tickers:
                    result[name] = tickers
            except Exception:
                pass
        return result

    def get_exchange_names(self) -> list[str]:
        return self.exchange_names

    def close(self):
        for ex in self.exchanges.values():
            try:
                ex.close()
            except Exception:
                pass
