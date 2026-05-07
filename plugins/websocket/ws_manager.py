import asyncio
import threading
from datetime import datetime
from core.models import Ticker


class WebSocketManager:
    def __init__(self, exchanges: dict, symbols: list[str]):
        self._exchanges = exchanges
        self._symbols = symbols
        self._cache: dict[str, dict[str, Ticker]] = {}
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _run_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._connect_and_stream())
        except Exception:
            pass
        finally:
            loop.close()

    async def _connect_and_stream(self):
        try:
            import ccxt.pro as ccxtpro
        except ImportError:
            return

        active_exchanges = {}
        for name in self._exchanges:
            try:
                exchange_class = getattr(ccxtpro, name, None)
                if exchange_class:
                    active_exchanges[name] = exchange_class({"enableRateLimit": True})
            except Exception:
                pass

        if not active_exchanges:
            return

        try:
            while self._running:
                for name, exchange in active_exchanges.items():
                    try:
                        tickers = await exchange.fetch_tickers(self._symbols)
                        for symbol, t in tickers.items():
                            if t.get("bid") and t.get("ask"):
                                ticker = Ticker(
                                    exchange=name,
                                    symbol=symbol,
                                    bid=t["bid"],
                                    ask=t["ask"],
                                    bid_volume=t.get("bidVolume") or 0,
                                    ask_volume=t.get("askVolume") or 0,
                                    timestamp=datetime.now(),
                                )
                                self.update_cache(name, symbol, ticker)
                    except Exception:
                        pass
                await asyncio.sleep(0.1)
        finally:
            for exchange in active_exchanges.values():
                try:
                    await exchange.close()
                except Exception:
                    pass

    def update_cache(self, exchange: str, symbol: str, ticker: Ticker):
        with self._lock:
            if exchange not in self._cache:
                self._cache[exchange] = {}
            self._cache[exchange][symbol] = ticker

    def get_tickers(self, symbols: list[str] | None = None) -> dict[str, dict[str, Ticker]]:
        with self._lock:
            if symbols is None:
                return dict(self._cache)
            result = {}
            for exchange, tickers in self._cache.items():
                filtered = {s: t for s, t in tickers.items() if s in symbols}
                if filtered:
                    result[exchange] = filtered
            return result

    def is_connected(self) -> bool:
        return self._running
