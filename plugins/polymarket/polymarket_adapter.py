from datetime import datetime
from core.models import Opportunity, ArbType


def find_polymarket_opportunities(
    markets: list[dict],
    min_spread: float = 0.01,
) -> list[Opportunity]:
    """Find Polymarket binary outcome arbitrage.

    Par relationship: YES + NO = $1.00
    If YES + NO < $1.00, buying both guarantees profit.
    """
    opportunities = []
    for market in markets:
        yes_price = market.get("yes_price", 0)
        no_price = market.get("no_price", 0)
        total = yes_price + no_price

        if total < 1.0:
            profit_pct = (1.0 - total) * 100
            if profit_pct >= min_spread * 100:
                opportunities.append(Opportunity(
                    arb_type=ArbType.POLYMARKET,
                    exchanges=["polymarket"],
                    path=[market.get("question", "unknown")],
                    profit_pct=round(profit_pct, 4),
                    profit_amount=round(1.0 - total, 4),
                    volume=1.0,
                ))

    return sorted(opportunities, key=lambda o: -o.profit_pct)


def fetch_polymarket_markets(api_url: str = "https://clob.polymarket.com") -> list[dict]:
    """Fetch binary outcome markets from Polymarket CLOB API."""
    import requests
    try:
        resp = requests.get(f"{api_url}/markets", timeout=10)
        markets = resp.json()
        result = []
        for market in markets:
            if market.get("active") and not market.get("closed"):
                tokens = market.get("tokens", [])
                if len(tokens) == 2:
                    yes_token = next((t for t in tokens if t.get("outcome") == "Yes"), None)
                    no_token = next((t for t in tokens if t.get("outcome") == "No"), None)
                    if yes_token and no_token:
                        result.append({
                            "id": market.get("id"),
                            "question": market.get("question", ""),
                            "yes_price": float(yes_token.get("price", 0)),
                            "no_price": float(no_token.get("price", 0)),
                        })
        return result
    except Exception:
        return []
