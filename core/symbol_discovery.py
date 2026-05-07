from datetime import datetime
import ccxt


class SymbolDiscovery:
    def __init__(self, exchanges: dict[str, ccxt.Exchange], min_volume: float = 0):
        self.exchanges = exchanges
        self.min_volume = min_volume
        self.cross_symbols: set[str] = set()
        self.triangular_symbols: set[str] = set()
        self.last_update = datetime.min
        self.update_interval = 300

    def discover(self):
        """Run discovery if cache is stale."""
        elapsed = (datetime.now() - self.last_update).total_seconds()
        if elapsed < self.update_interval:
            return
        self._discover()
        self.last_update = datetime.now()

    def _discover(self):
        """Fetch markets from all exchanges and find shared symbols."""
        all_markets: dict[str, dict[str, dict]] = {}
        for name, exchange in self.exchanges.items():
            try:
                all_markets[name] = exchange.markets or {}
            except Exception:
                all_markets[name] = {}

        self.cross_symbols = self._find_cross_symbols(all_markets)
        self.triangular_symbols = self._find_triangular_symbols(all_markets)

    def _find_cross_symbols(self, all_markets: dict[str, dict[str, dict]]) -> set[str]:
        """Find symbols that exist on 2+ exchanges."""
        symbol_counts: dict[str, int] = {}
        for markets in all_markets.values():
            for symbol in markets:
                symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        return {s for s, count in symbol_counts.items() if count >= 2}

    def _find_triangular_symbols(self, all_markets: dict[str, dict[str, dict]]) -> set[str]:
        """Find symbols that form triangles on any exchange."""
        triangular = set()
        for markets in all_markets.values():
            graph = self._build_currency_graph(markets)
            for base in graph:
                for mid in graph[base]:
                    for target in graph[mid]:
                        if target in graph.get(base, {}):
                            triangular.update([
                                self._find_symbol(markets, base, mid),
                                self._find_symbol(markets, mid, target),
                                self._find_symbol(markets, target, base),
                            ])
        triangular.discard(None)
        return triangular

    def _build_currency_graph(self, markets: dict[str, dict]) -> dict[str, set[str]]:
        """Build adjacency list of currencies from markets."""
        graph: dict[str, set[str]] = {}
        for market in markets.values():
            base = market.get("base", "")
            quote = market.get("quote", "")
            if base and quote:
                graph.setdefault(base, set()).add(quote)
                graph.setdefault(quote, set()).add(base)
        return graph

    def _find_symbol(self, markets: dict[str, dict], base: str, quote: str) -> str | None:
        """Find the symbol string for a base/quote pair."""
        for symbol, market in markets.items():
            if market.get("base") == base and market.get("quote") == quote:
                return symbol
            if market.get("base") == quote and market.get("quote") == base:
                return symbol
        return None

    def get_all_symbols(self) -> list[str]:
        """Return union of cross and triangular symbols."""
        elapsed = (datetime.now() - self.last_update).total_seconds()
        if elapsed >= self.update_interval:
            self.discover()
        return sorted(self.cross_symbols | self.triangular_symbols)
