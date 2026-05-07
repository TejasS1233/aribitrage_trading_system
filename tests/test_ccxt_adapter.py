from datetime import datetime

from core.models import Ticker
from plugins.cex.ccxt_adapter import CCXTAdapter


class FakeExchange:
    def __init__(self, markets):
        self.id = "fake"
        self.markets = {symbol: {} for symbol in markets}
        self.last_symbols = None

    def fetch_tickers(self, symbols):
        self.last_symbols = list(symbols)
        invalid = [symbol for symbol in symbols if symbol not in self.markets]
        if invalid:
            raise ValueError(f"Invalid symbols: {invalid}")
        return {
            symbol: {
                "bid": 100.0,
                "ask": 101.0,
                "bidVolume": 1.0,
                "askVolume": 1.0,
            }
            for symbol in symbols
        }


def test_ccxt_adapter_filters_invalid_symbols():
    adapter = CCXTAdapter([])
    adapter.exchange_names = ["fake"]
    adapter.exchanges = {"fake": FakeExchange(["BTC/USDT", "ETH/USDT"])}

    tickers = adapter.fetch_tickers(["BTC/USDT", "ETH/USDT", "XRP/BTC"])

    assert "fake" in tickers
    assert set(tickers["fake"].keys()) == {"BTC/USDT", "ETH/USDT"}
    assert adapter.exchanges["fake"].last_symbols == ["BTC/USDT", "ETH/USDT"]
