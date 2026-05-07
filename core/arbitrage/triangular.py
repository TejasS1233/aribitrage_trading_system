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
        ticker_map = _get_ticker_for_leg(tickers)
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
                            vol = _get_min_volume(ticker_map, a, b, c)
                            profit_dollars = vol * profit_pct / 100
                            opportunities.append(Opportunity(
                                arb_type=ArbType.TRIANGULAR,
                                exchanges=[exchange],
                                path=[a, b, c, a],
                                profit_pct=round(profit_pct, 4),
                                profit_amount=round(profit_dollars, 4),
                                volume=round(vol, 2),
                            ))
    return sorted(opportunities, key=lambda o: -o.profit_pct)


def _get_ticker_for_leg(tickers: dict[str, Ticker]) -> dict[tuple, Ticker]:
    """Map (base, quote) -> Ticker for quick lookup."""
    result = {}
    for t in tickers.values():
        if "/" in t.symbol:
            base, quote = t.symbol.split("/")
            result[(base, quote)] = t
    return result


def _get_min_volume(ticker_map: dict[tuple, Ticker], a: str, b: str, c: str) -> float:
    """Get minimum volume across all 3 legs of triangular arb."""
    vols = []
    if (a, b) in ticker_map:
        v = ticker_map[(a, b)].ask_volume
        if v > 0:
            vols.append(v)
    if (b, c) in ticker_map:
        v = ticker_map[(b, c)].ask_volume
        if v > 0:
            vols.append(v)
    if (c, a) in ticker_map:
        v = ticker_map[(c, a)].ask_volume
        if v > 0:
            vols.append(v)
    
    if not vols:
        return 100  # Default $100 if no volume data
    return min(vols)

def _build_graph(tickers: dict[str, Ticker], fee: float) -> dict[str, dict[str, float]]:
    """Build directed graph of exchange rates from tickers."""
    graph: dict[str, dict[str, float]] = {}
    for ticker in tickers.values():
        base, quote = ticker.symbol.split("/")
        graph.setdefault(base, {})[quote] = ticker.bid * (1 - fee)
        graph.setdefault(quote, {})[base] = (1 - fee) / ticker.ask
    return graph
