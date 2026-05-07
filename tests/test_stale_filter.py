from datetime import datetime, timedelta

from core.models import Ticker
from core.stale_filter import filter_stale_tickers


def make_ticker(exchange, symbol, bid, ask, age_seconds=0):
    return Ticker(
        exchange=exchange,
        symbol=symbol,
        bid=bid,
        ask=ask,
        bid_volume=10.0,
        ask_volume=10.0,
        timestamp=datetime.now() - timedelta(seconds=age_seconds),
    )


def test_fresh_tickers_pass():
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50100, age_seconds=1),
        }
    }
    result = filter_stale_tickers(tickers, max_age_seconds=5.0)
    assert "binance" in result
    assert "BTC/USDT" in result["binance"]


def test_stale_tickers_filtered():
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50100, age_seconds=10),
            "ETH/USDT": make_ticker("binance", "ETH/USDT", 3000, 3100, age_seconds=1),
        }
    }
    result = filter_stale_tickers(tickers, max_age_seconds=5.0)
    assert "BTC/USDT" not in result["binance"]
    assert "ETH/USDT" in result["binance"]


def test_empty_exchange_removed():
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50100, age_seconds=10),
        }
    }
    result = filter_stale_tickers(tickers, max_age_seconds=5.0)
    assert "binance" not in result
