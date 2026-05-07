from core.models import Ticker, Opportunity, ArbType


STABLECOIN_PAIRS = [
    ("USDT", "USDC"),
    ("USDT", "DAI"),
    ("USDT", "BUSD"),
    ("USDC", "DAI"),
]


def find_stablecoin_depeg_opportunities(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    min_depeg_pct: float = 0.5,
) -> list[Opportunity]:
    """Find stablecoin depeg opportunities.
    
    When stablecoins deviate from $1.00 (like USDC vs USDT),
    you can profit by exchanging one for another.
    """
    opportunities = []
    
    for exchange_tickers in tickers_by_exchange.values():
        for base, quote in STABLECOIN_PAIRS:
            symbol = f"{base}/{quote}"
            if symbol in exchange_tickers:
                ticker = exchange_tickers[symbol]
                deviation = abs(ticker.bid - 1.0)
                if deviation >= min_depeg_pct / 100:
                    opportunities.append(
                        Opportunity(
                            arb_type=ArbType.STABLECOIN_DEPEG,
                            exchanges=[ticker.exchange],
                            path=[symbol],
                            profit_pct=round(deviation * 100, 4),
                            profit_amount=round(deviation * ticker.bid_volume, 4),
                            volume=round(ticker.bid_volume, 4),
                        )
                    )
    
    return sorted(opportunities, key=lambda o: -o.profit_pct)


def find_funding_rate_opportunities(
    tickers_by_exchange: dict[str, dict[str, Ticker]],
    funding_rates: dict[str, dict],
    min_profit_pct: float = 0.1,
) -> list[Opportunity]:
    """Find funding rate arbitrage opportunities.
    
    Compare funding rates across exchanges - borrow low, lend high.
    """
    opportunities = []
    
    for symbol, rate_data in funding_rates.items():
        rate = rate_data.get("fundingRate", 0)
        if rate and abs(rate) >= min_profit_pct / 100:
            opportunities.append(
                Opportunity(
                    arb_type=ArbType.FUNDING_RATE,
                    exchanges=["futures"],
                    path=[symbol],
                    profit_pct=round(rate * 100, 4),
                    profit_amount=0,
                    volume=0,
                )
            )
    
    return sorted(opportunities, key=lambda o: -o.profit_pct)