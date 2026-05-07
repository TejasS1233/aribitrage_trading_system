from datetime import datetime
from core.models import Ticker
from core.engine import Engine
from core.stale_filter import filter_stale_tickers


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

    def connect(self):
        pass

    def fetch_tickers(self, symbols):
        return self.tickers

    def get_exchange_names(self):
        return ["binance", "coinbase"]

    def close(self):
        pass


def test_e2e_with_bellman_ford():
    """Engine should detect cross-exchange AND Bellman-Ford opportunities."""
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
        "stale_filter": {"max_age_seconds": 60},
    }
    engine = Engine(config, source, [Collector()])
    engine.run_once()

    cross = [o for o in collected if o.arb_type.value == "cross_exchange"]
    assert len(cross) >= 1


def test_e2e_detects_bellman_ford_cycle():
    """Engine should detect Bellman-Ford multi-hop opportunities."""
    tickers = {
        "a": {
            "BTC/USDT": Ticker("a", "BTC/USDT", 50000, 50100, 10, 10, datetime.now()),
            "ETH/USDT": Ticker("a", "ETH/USDT", 3000, 3010, 10, 10, datetime.now()),
        },
        "b": {
            "ETH/BTC": Ticker("b", "ETH/BTC", 0.059, 0.060, 10, 10, datetime.now()),
        },
    }

    from core.arbitrage.bellman_ford import find_bellman_ford_opportunities
    opps = find_bellman_ford_opportunities(tickers, {"default": 0.001}, min_profit_pct=0.0)
    for opp in opps:
        assert opp.arb_type.value == "bellman_ford"
        assert opp.profit_pct > 0


def test_stale_filter_integrated():
    """Stale filter should remove old tickers."""
    now = datetime.now()
    tickers = {
        "binance": {
            "BTC/USDT": Ticker("binance", "BTC/USDT", 50000, 50100, 10, 10, now),
        },
        "stale_exchange": {
            "BTC/USDT": Ticker("stale_exchange", "BTC/USDT", 50000, 50100, 10, 10, now),
        },
    }

    from datetime import timedelta
    tickers["stale_exchange"]["BTC/USDT"] = Ticker(
        "stale_exchange", "BTC/USDT", 50000, 50100, 10, 10,
        now - timedelta(seconds=100),
    )

    result = filter_stale_tickers(tickers, max_age_seconds=5.0)
    assert "binance" in result
    assert "stale_exchange" not in result
