import asyncio
from datetime import datetime
from core.models import Ticker
from core.engine import Engine


class FakeDataSource:
    def __init__(self):
        self.tickers = {
            "binance": {
                "BTC/USDT": Ticker("binance", "BTC/USDT", 50500, 50600, 10, 10, datetime.now()),
                "ETH/USDT": Ticker("binance", "ETH/USDT", 3000, 3001, 10, 10, datetime.now()),
                "ETH/BTC": Ticker("binance", "ETH/BTC", 0.06, 0.0601, 10, 10, datetime.now()),
            },
            "coinbase": {
                "BTC/USDT": Ticker("coinbase", "BTC/USDT", 50000, 50050, 10, 10, datetime.now()),
            },
        }

    async def connect(self):
        pass

    async def fetch_tickers(self, symbols):
        return self.tickers

    async def get_exchange_names(self):
        return ["binance", "coinbase"]

    async def close(self):
        pass


def test_e2e_detects_cross_exchange():
    source = FakeDataSource()
    collected = []

    class Collector:
        def update(self, opps, portfolio):
            collected.extend(opps)

    config = {
        "poll_interval": 0.01,
        "min_profit_pct": 0.01,
        "fees": {"default": 0.001},
        "starting_balance": {"USDT": 10000},
        "symbols": ["BTC/USDT", "ETH/USDT", "ETH/BTC"],
    }
    engine = Engine(config, source, [Collector()])
    asyncio.get_event_loop().run_until_complete(engine.run_once())

    cross = [o for o in collected if o.arb_type.value == "cross_exchange"]
    assert len(cross) >= 1
