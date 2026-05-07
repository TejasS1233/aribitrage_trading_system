from datetime import datetime
from core.models import Ticker
from plugins.websocket.ws_manager import WebSocketManager


def test_cache_read_write():
    manager = WebSocketManager.__new__(WebSocketManager)
    manager._cache = {}
    manager._lock = __import__("threading").Lock()
    manager._running = False

    ticker = Ticker("binance", "BTC/USDT", 50000, 50100, 10, 10, datetime.now())
    manager.update_cache("binance", "BTC/USDT", ticker)

    result = manager.get_tickers(["BTC/USDT"])
    assert "binance" in result
    assert "BTC/USDT" in result["binance"]
    assert result["binance"]["BTC/USDT"].bid == 50000


def test_cache_returns_only_requested_symbols():
    manager = WebSocketManager.__new__(WebSocketManager)
    manager._cache = {}
    manager._lock = __import__("threading").Lock()
    manager._running = False

    manager.update_cache("binance", "BTC/USDT", Ticker("binance", "BTC/USDT", 50000, 50100, 10, 10, datetime.now()))
    manager.update_cache("binance", "ETH/USDT", Ticker("binance", "ETH/USDT", 3000, 3100, 10, 10, datetime.now()))

    result = manager.get_tickers(["BTC/USDT"])
    assert "BTC/USDT" in result["binance"]
    assert "ETH/USDT" not in result["binance"]


def test_empty_cache_returns_empty():
    manager = WebSocketManager.__new__(WebSocketManager)
    manager._cache = {}
    manager._lock = __import__("threading").Lock()
    manager._running = False

    result = manager.get_tickers(["BTC/USDT"])
    assert result == {}
