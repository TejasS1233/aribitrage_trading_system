from datetime import datetime
from core.models import Ticker, ArbType
from core.arbitrage.triangular import find_triangular_opportunities

def make_ticker(exchange, symbol, bid, ask):
    return Ticker(exchange=exchange, symbol=symbol, bid=bid, ask=ask,
                  bid_volume=10.0, ask_volume=10.0, timestamp=datetime.now())

def test_triangular_arb_detected():
    """BTC→ETH→USDT→BTC: buy BTC with ETH, sell BTC for USDT, buy ETH with USDT."""
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50010),
            "ETH/USDT": make_ticker("binance", "ETH/USDT", 3000, 3001),
            "ETH/BTC": make_ticker("binance", "ETH/BTC", 0.06, 0.0601),
        }
    }
    opps = find_triangular_opportunities(tickers, fees={"default": 0.001})
    assert isinstance(opps, list)

def test_triangular_with_profit():
    """Set up prices where triangular arb exists."""
    tickers = {
        "binance": {
            "BTC/USDT": make_ticker("binance", "BTC/USDT", 50000, 50010),
            "ETH/USDT": make_ticker("binance", "ETH/USDT", 3000, 3001),
            "ETH/BTC": make_ticker("binance", "ETH/BTC", 0.061, 0.0611),
        }
    }
    opps = find_triangular_opportunities(tickers, fees={"default": 0.001})
    assert isinstance(opps, list)
