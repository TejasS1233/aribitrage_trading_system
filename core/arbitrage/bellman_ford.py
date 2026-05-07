import math
from datetime import datetime
from core.models import Ticker, Opportunity, ArbType


def find_bellman_ford_opportunities(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    fees: dict[str, float] | None = None,
    min_profit_pct: float = 0.0,
    max_hops: int = 4,
) -> list[Opportunity]:
    """Find multi-hop arbitrage using Bellman-Ford negative cycle detection."""
    if fees is None:
        fees = {"default": 0.001}
    default_fee = fees.get("default", 0.001)

    edges = []
    for exchange, tickers in tickers_by_exchange.items():
        fee = fees.get(exchange, default_fee)
        for ticker in tickers.values():
            base, quote = ticker.symbol.split("/")
            if ticker.bid > 0:
                rate = ticker.bid * (1 - fee)
                weight = -math.log(rate)
                edges.append((base, quote, exchange, weight, ticker.symbol, ticker.bid))
            if ticker.ask > 0:
                rate = (1 - fee) / ticker.ask
                weight = -math.log(rate)
                edges.append((quote, base, exchange, weight, ticker.symbol, ticker.ask))

    if not edges:
        return []

    currencies = set()
    for from_c, to_c, _, _, _, _ in edges:
        currencies.add(from_c)
        currencies.add(to_c)

    currencies = sorted(currencies)
    if not currencies:
        return []

    dist = {c: 0.0 for c in currencies}
    pred = {c: None for c in currencies}

    for _ in range(len(currencies) - 1):
        for from_c, to_c, exchange, weight, symbol, price in edges:
            if dist[from_c] + weight < dist[to_c]:
                dist[to_c] = dist[from_c] + weight
                pred[to_c] = (from_c, exchange, symbol, price)

    opportunities = []
    for from_c, to_c, exchange, weight, symbol, price in edges:
        if dist[from_c] + weight < dist[to_c]:
            cycle = _retrace_cycle(to_c, pred, max_hops)
            if cycle and len(cycle) <= max_hops + 1:
                profit_pct = _calculate_profit(cycle, tickers_by_exchange, fees, default_fee)
                if profit_pct >= min_profit_pct:
                    path = [c for c, _, _ in cycle]
                    exchanges = list({e for _, e, _ in cycle})
                    opportunities.append(Opportunity(
                        arb_type=ArbType.BELLMAN_FORD,
                        exchanges=exchanges,
                        path=path,
                        profit_pct=round(profit_pct, 4),
                        profit_amount=0.0,
                        volume=1.0,
                    ))

    seen = set()
    unique = []
    for opp in opportunities:
        key = tuple(opp.path)
        if key not in seen:
            seen.add(key)
            unique.append(opp)

    return sorted(unique, key=lambda o: -o.profit_pct)


def _retrace_cycle(
    start: str,
    pred: dict,
    max_hops: int,
) -> list[tuple[str, str, str]] | None:
    visited = {}
    current = start
    for _ in range(max_hops + 2):
        if current in visited:
            cycle_start = visited[current]
            path = []
            node = current
            for _ in range(cycle_start, len(visited)):
                if pred[node] is None:
                    return None
                prev, exchange, symbol = pred[node][0], pred[node][1], pred[node][2]
                path.append((node, exchange, symbol))
                node = prev
            path.reverse()
            return path
        visited[current] = len(visited)
        if pred[current] is None:
            return None
        current = pred[current][0]
    return None


def _calculate_profit(
    cycle: list[tuple[str, str, str]],
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    fees: dict[str, float],
    default_fee: float,
) -> float:
    if len(cycle) < 2:
        return 0.0

    product = 1.0
    for i in range(len(cycle)):
        from_c = cycle[i][0]
        to_c = cycle[(i + 1) % len(cycle)][0]
        exchange = cycle[i][1]

        ticker = _find_ticker(tickers_by_exchange, exchange, from_c, to_c)
        if ticker is None:
            return 0.0

        fee = fees.get(exchange, default_fee)
        if from_c == ticker.symbol.split("/")[0]:
            rate = ticker.bid * (1 - fee)
        else:
            rate = (1 - fee) / ticker.ask

        product *= rate

    return (product - 1.0) * 100 if product > 1.0 else 0.0


def _find_ticker(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    exchange: str,
    from_c: str,
    to_c: str,
) -> Ticker | None:
    tickers = tickers_by_exchange.get(exchange, {})
    for ticker in tickers.values():
        base, quote = ticker.symbol.split("/")
        if (base == from_c and quote == to_c) or (base == to_c and quote == from_c):
            return ticker
    return None
