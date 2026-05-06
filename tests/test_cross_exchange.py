from datetime import datetime
from core.models import Ticker, ArbType
from core.arbitrage.cross_exchange import find_cross_exchange_opportunities


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


def test_inverted_spread_detected():
    tickers = {
        "binance": {"BTC/USDT": make_ticker("binance", "BTC/USDT", 50500, 50600)},
        "coinbase": {"BTC/USDT": make_ticker("coinbase", "BTC/USDT", 50000, 50050)},
    }
    opps = find_cross_exchange_opportunities(tickers, fees={"default": 0.001})
    assert len(opps) == 1
    assert opps[0].arb_type == ArbType.CROSS_EXCHANGE
    assert "binance" in opps[0].exchanges
    assert "coinbase" in opps[0].exchanges


def test_no_opportunity_when_no_spread():
    tickers = {
        "binance": {"BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50100)},
        "coinbase": {"BTC/USDT": make_ticker("coinbase", "BTC/USDT", 49900, 50050)},
    }
    opps = find_cross_exchange_opportunities(tickers, fees={"default": 0.001})
    assert len(opps) == 0


def test_profit_calculation():
    tickers = {
        "binance": {"BTC/USDT": make_ticker("binance", "BTC/USDT", 50200, 50300)},
        "coinbase": {"BTC/USDT": make_ticker("coinbase", "BTC/USDT", 50000, 50050)},
    }
    opps = find_cross_exchange_opportunities(tickers, fees={"default": 0.001})
    assert len(opps) == 1
    assert opps[0].profit_pct > 0
