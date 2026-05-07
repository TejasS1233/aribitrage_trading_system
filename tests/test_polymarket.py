from plugins.polymarket.polymarket_adapter import find_polymarket_opportunities


def test_detects_under_par():
    markets = [
        {"id": "m1", "question": "Will BTC hit 100k?", "yes_price": 0.45, "no_price": 0.50},
    ]
    opps = find_polymarket_opportunities(markets, min_spread=0.01)
    assert len(opps) == 1
    assert opps[0].profit_pct > 0


def test_no_opportunity_when_at_par():
    markets = [
        {"id": "m2", "question": "Will ETH hit 5k?", "yes_price": 0.50, "no_price": 0.50},
    ]
    opps = find_polymarket_opportunities(markets, min_spread=0.01)
    assert len(opps) == 0


def test_profit_calculation():
    markets = [
        {"id": "m3", "question": "Test?", "yes_price": 0.40, "no_price": 0.55},
    ]
    opps = find_polymarket_opportunities(markets, min_spread=0.01)
    assert len(opps) == 1
    assert abs(opps[0].profit_pct - 5.0) < 0.1
