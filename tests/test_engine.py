import asyncio
from datetime import datetime
from core.models import Ticker, PaperPortfolio
from core.engine import Engine


class MockDataSource:
    def __init__(self, tickers):
        self._tickers = tickers

    async def connect(self):
        pass

    async def fetch_tickers(self, symbols):
        return self._tickers

    async def get_exchange_names(self):
        return list(self._tickers.keys())

    async def close(self):
        pass


class MockOutput:
    def __init__(self):
        self.calls = []

    def update(self, opportunities, portfolio):
        self.calls.append((opportunities, portfolio))


def make_ticker(exchange, symbol, bid, ask):
    return Ticker(
        exchange=exchange,
        symbol=symbol,
        bid=bid,
        ask=ask,
        bid_volume=10.0,
        ask_volume=10.0,
        timestamp=datetime.now(),
    )


def test_engine_runs_one_cycle():
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50100, 50200)
        },
        "coinbase": {
            "BTC/USDT": make_ticker("coinbase", "BTC/USDT", 50000, 50050)
        },
    }
    source = MockDataSource(tickers)
    output = MockOutput()
    config = {
        "poll_interval": 0.01,
        "min_profit_pct": 0.01,
        "fees": {"default": 0.001},
        "starting_balance": {"USDT": 10000},
    }
    engine = Engine(config, source, [output])
    asyncio.get_event_loop().run_until_complete(engine.run_once())
    assert len(output.calls) == 1
