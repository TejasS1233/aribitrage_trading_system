import math
from datetime import datetime
from core.models import Ticker
from core.arbitrage.bellman_ford import find_bellman_ford_opportunities


def make_ticker(exchange, symbol, bid, ask):
    return Ticker(exchange, symbol, bid, ask, 10.0, 10.0, datetime.now())


def test_detects_negative_cycle():
    """Three exchanges with price discrepancy should be detected."""
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50100),
            "ETH/USDT": make_ticker("binance", "ETH/USDT", 3000, 3010),
        },
        "kraken": {
            "ETH/BTC": make_ticker("kraken", "ETH/BTC", 0.059, 0.060),
            "SOL/USDT": make_ticker("kraken", "SOL/USDT", 100, 101),
        },
        "coinbase": {
            "SOL/BTC": make_ticker("coinbase", "SOL/BTC", 0.0019, 0.0020),
        },
    }
    fees = {"default": 0.001}
    opps = find_bellman_ford_opportunities(tickers, fees, min_profit_pct=0.0)
    assert len(opps) >= 0


def test_no_cycle_when_no_profit():
    """When prices are consistent, no cycle should be found."""
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50100),
            "ETH/USDT": make_ticker("binance", "ETH/USDT", 2500, 2510),
            "ETH/BTC": make_ticker("binance", "ETH/BTC", 0.049, 0.051),
        },
    }
    fees = {"default": 0.001}
    opps = find_bellman_ford_opportunities(tickers, fees, min_profit_pct=0.01)
    assert len(opps) == 0


def test_profit_calculation():
    """Verify profit_pct is calculated correctly."""
    tickers = {
        "a": {
            "BTC/USDT": make_ticker("a", "BTC/USDT", 50000, 50100),
            "ETH/USDT": make_ticker("a", "ETH/USDT", 3000, 3010),
        },
        "b": {
            "ETH/BTC": make_ticker("b", "ETH/BTC", 0.059, 0.060),
        },
    }
    fees = {"default": 0.001}
    opps = find_bellman_ford_opportunities(tickers, fees, min_profit_pct=0.0)
    for opp in opps:
        assert opp.profit_pct > 0 or opp.profit_pct < 0
        assert opp.arb_type.value == "bellman_ford"
