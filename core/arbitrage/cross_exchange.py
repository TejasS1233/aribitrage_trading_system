from core.models import Ticker, Opportunity, ArbType


def find_cross_exchange_opportunities(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    fees: dict[str, float] | None = None,
    min_profit_pct: float = 0.0,
) -> list[Opportunity]:
    """Find cross-exchange arbitrage: buy low on A, sell high on B."""
    if fees is None:
        fees = {"default": 0.001}
    default_fee = fees.get("default", 0.001)

    # Group tickers by symbol
    by_symbol: dict[str, list[Ticker]] = {}
    for exchange_tickers in tickers_by_exchange.values():
        for ticker in exchange_tickers.values():
            by_symbol.setdefault(ticker.symbol, []).append(ticker)

    opportunities = []
    for symbol, tickers in by_symbol.items():
        if len(tickers) < 2:
            continue

        best_ask_ticker = min(tickers, key=lambda t: t.ask)
        best_bid_ticker = max(tickers, key=lambda t: t.bid)

        if best_ask_ticker.exchange == best_bid_ticker.exchange:
            continue

        spread = best_bid_ticker.bid - best_ask_ticker.ask
        if spread <= 0:
            continue

        buy_fee = fees.get(best_ask_ticker.exchange, default_fee)
        sell_fee = fees.get(best_bid_ticker.exchange, default_fee)
        fee_cost = best_ask_ticker.ask * buy_fee + best_bid_ticker.bid * sell_fee
        net_profit = spread - fee_cost
        profit_pct = (net_profit / best_ask_ticker.ask) * 100

        if profit_pct < min_profit_pct:
            continue

        volume = min(best_bid_ticker.bid_volume, best_ask_ticker.ask_volume)

        opportunities.append(
            Opportunity(
                arb_type=ArbType.CROSS_EXCHANGE,
                exchanges=[best_ask_ticker.exchange, best_bid_ticker.exchange],
                path=[symbol],
                profit_pct=round(profit_pct, 4),
                profit_amount=round(net_profit * volume, 4),
                volume=round(volume, 4),
            )
        )

    return sorted(opportunities, key=lambda o: -o.profit_pct)
