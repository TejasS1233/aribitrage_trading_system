import ccxt
from datetime import datetime
from core.models import Ticker
from plugins.base import DataSource


class CCXTAdapter(DataSource):
    def __init__(self, exchanges: list[str], rate_limit: bool = True):
        self.exchange_names = exchanges
        self.exchanges: dict[str, ccxt.Exchange] = {}
        self._debug = False
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
                exchange_symbols = symbols
                markets = getattr(ex, "markets", None)
                if markets:
                    exchange_symbols = [symbol for symbol in symbols if symbol in markets]
                if self._debug:
                    print(f"  {name}: requesting {len(exchange_symbols)} symbols")
                if not exchange_symbols:
                    if self._debug:
                        print(f"  {name}: no supported symbols requested")
                    continue
                raw = ex.fetch_tickers(exchange_symbols)
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
                    elif self._debug:
                        print(f"  {name}: missing bid/ask for {symbol}")
                if tickers:
                    if self._debug:
                        print(f"  {name}: returned {len(tickers)} tickers")
                    result[name] = tickers
                elif self._debug:
                    print(f"  {name}: no tickers returned for symbols")
            except Exception as e:
                if self._debug:
                    print(f"  {name}: fetch_tickers failed ({e})")
        return result

    def set_debug(self, enabled: bool) -> None:
        self._debug = enabled

    def get_exchange_names(self) -> list[str]:
        return self.exchange_names

    def fetch_order_book(self, symbol: str, limit: int = 20) -> dict:
        """Fetch order book for a symbol to check depth."""
        for name, ex in self.exchanges.items():
            try:
                if symbol in ex.markets:
                    book = ex.fetch_order_book(symbol, limit)
                    return {
                        "bids": book.get("bids", []),
                        "asks": book.get("asks", []),
                    }
            except Exception:
                continue
        return {"bids": [], "asks": []}
    
    def has_volume(self, symbol: str, amount: float) -> bool:
        """Check if order book has enough volume at price."""
        book = self.fetch_order_book(symbol, 20)
        bids = book.get("bids", [])
        asks = book.get("asks", [])
        
        bid_vol = sum(vol for price, vol in bids[:5]) if bids else 0
        ask_vol = sum(vol for price, vol in asks[:5]) if asks else 0
        
        return bid_vol >= amount and ask_vol >= amount
    
    def close(self):
        for ex in self.exchanges.values():
            try:
                ex.close()
            except Exception:
                pass
        """Fetch funding rates for futures symbols."""
        result = {}
        for name, ex in self.exchanges.items():
            try:
                if hasattr(ex, 'fetchFundingRates'):
                    if symbols:
                        raw = ex.fetchFundingRates(symbols)
                    else:
                        raw = ex.fetchFundingRates()
                    result[name] = raw
                    if self._debug:
                        print(f"  {name}: fetched {len(raw)} funding rates")
            except Exception as e:
                if self._debug:
                    print(f"  {name}: fetch_funding_rates failed ({e})")
        return result
