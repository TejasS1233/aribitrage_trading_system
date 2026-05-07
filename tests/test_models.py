from datetime import datetime
from core.models import Ticker, Opportunity, ArbType, PaperTrade, PaperPortfolio

def test_ticker_creation():
    t = Ticker(exchange="binance", symbol="BTC/USDT", bid=50000, ask=50001, bid_volume=1.5, ask_volume=2.0, timestamp=datetime.now())
    assert t.exchange == "binance"
    assert t.bid == 50000

def test_opportunity_profit():
    opp = Opportunity(
        arb_type=ArbType.TRIANGULAR,
        exchanges=["binance"],
        path=["BTC/USDT", "ETH/BTC", "USDT/ETH"],
        profit_pct=0.23,
        profit_amount=0.0023,
        volume=1.0,
    )
    assert opp.profit_pct > 0

def test_paper_portfolio_initial():
    p = PaperPortfolio(balance={"USDT": 10000})
    assert p.total_trades == 0
    assert p.total_pnl == 0.0

def test_new_arb_types():
    assert ArbType.BELLMAN_FORD.value == "bellman_ford"
    assert ArbType.DEX_CROSS.value == "dex_cross"
    assert ArbType.POLYMARKET.value == "polymarket"
    assert len(ArbType) >= 8
