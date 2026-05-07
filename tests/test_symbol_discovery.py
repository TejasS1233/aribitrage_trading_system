from datetime import datetime

from core.models import Ticker
from core.symbol_discovery import SymbolDiscovery


def make_ticker(exchange, symbol, bid, ask):
    return Ticker(exchange, symbol, bid, ask, 10.0, 10.0, datetime.now())


class MockExchange:
    def __init__(self, markets):
        self.markets = markets
        self.id = "mock"


def test_find_cross_symbols():
    """Symbols on 2+ exchanges should be in cross_symbols."""
    # Simulate two exchanges with overlapping markets
    markets_a = {
        "BTC/USDT": {"symbol": "BTC/USDT", "base": "BTC", "quote": "USDT"},
        "ETH/USDT": {"symbol": "ETH/USDT", "base": "ETH", "quote": "USDT"},
    }
    markets_b = {
        "BTC/USDT": {"symbol": "BTC/USDT", "base": "BTC", "quote": "USDT"},
        "SOL/USDT": {"symbol": "SOL/USDT", "base": "SOL", "quote": "USDT"},
    }

    discovery = SymbolDiscovery.__new__(SymbolDiscovery)
    discovery.exchanges = {"a": MockExchange(markets_a), "b": MockExchange(markets_b)}
    discovery.min_volume = 0
    discovery.cross_symbols = set()
    discovery.triangular_symbols = set()

    discovery._discover()

    assert "BTC/USDT" in discovery.cross_symbols
    assert "ETH/USDT" not in discovery.cross_symbols  # only on A
    assert "SOL/USDT" not in discovery.cross_symbols  # only on B


def test_find_triangular_symbols():
    """Currencies forming triangles should be in triangular_symbols."""
    markets = {
        "BTC/USDT": {"symbol": "BTC/USDT", "base": "BTC", "quote": "USDT"},
        "ETH/USDT": {"symbol": "ETH/USDT", "base": "ETH", "quote": "USDT"},
        "ETH/BTC": {"symbol": "ETH/BTC", "base": "ETH", "quote": "BTC"},
    }

    discovery = SymbolDiscovery.__new__(SymbolDiscovery)
    discovery.exchanges = {"mock": MockExchange(markets)}
    discovery.min_volume = 0
    discovery.cross_symbols = set()
    discovery.triangular_symbols = set()

    discovery._discover()

    # BTC/USDT, ETH/USDT, ETH/BTC form a triangle
    assert "BTC/USDT" in discovery.triangular_symbols
    assert "ETH/USDT" in discovery.triangular_symbols
    assert "ETH/BTC" in discovery.triangular_symbols


def test_get_all_symbols():
    """get_all_symbols returns union of cross and triangular."""
    discovery = SymbolDiscovery.__new__(SymbolDiscovery)
    discovery.cross_symbols = {"BTC/USDT", "ETH/USDT"}
    discovery.triangular_symbols = {"BTC/USDT", "ETH/BTC"}
    discovery.last_update = datetime.now()
    discovery.update_interval = 300

    result = discovery.get_all_symbols()
    assert set(result) == {"BTC/USDT", "ETH/USDT", "ETH/BTC"}
