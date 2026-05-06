import math
from core.models import Ticker, Opportunity, ArbType

def find_triangular_opportunities(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    fees: dict[str, float] = None,
    min_profit_pct: float = 0.0,
) -> list[Opportunity]:
    """Find triangular arbitrage: A→B→C→A on each exchange."""
    if fees is None:
        fees = {"default": 0.001}
    default_fee = fees.get("default", 0.001)

    opportunities = []
    for exchange, tickers in tickers_by_exchange.items():
        fee = fees.get(exchange, default_fee)
        graph = _build_graph(tickers, fee)
        currencies = list(graph.keys())
        for a in currencies:
            for b in graph.get(a, {}):
                if b == a:
                    continue
                for c in graph.get(b, {}):
                    if c == a or c == b:
                        continue
                    if a not in graph.get(c, {}):
                        continue
                    rate_ab = graph[a][b]
                    rate_bc = graph[b][c]
                    rate_ca = graph[c][a]
                    product = rate_ab * rate_bc * rate_ca
                    if product > 1.0:
                        profit_pct = (product - 1.0) * 100
                        if profit_pct >= min_profit_pct:
                            opportunities.append(Opportunity(
                                arb_type=ArbType.TRIANGULAR,
                                exchanges=[exchange],
                                path=[a, b, c, a],
                                profit_pct=round(profit_pct, 4),
                                profit_amount=0.0,
                                volume=1.0,
                            ))
    return sorted(opportunities, key=lambda o: -o.profit_pct)

def _build_graph(tickers: dict[str, Ticker], fee: float) -> dict[str, dict[str, float]]:
    """Build directed graph of exchange rates from tickers."""
    graph: dict[str, dict[str, float]] = {}
    for ticker in tickers.values():
        base, quote = ticker.symbol.split("/")
        graph.setdefault(base, {})[quote] = ticker.bid * (1 - fee)
        graph.setdefault(quote, {})[base] = (1 - fee) / ticker.ask
    return graph
