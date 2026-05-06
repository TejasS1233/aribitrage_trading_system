from datetime import datetime
from core.models import Ticker, Opportunity, ArbType, PaperPortfolio
from output.terminal import format_opportunities, format_portfolio

def test_format_opportunities():
    opps = [
        Opportunity(
            arb_type=ArbType.TRIANGULAR,
            exchanges=["binance"],
            path=["BTC", "ETH", "USDT", "BTC"],
            profit_pct=0.23,
            profit_amount=0.0023,
            volume=1.0,
        )
    ]
    table = format_opportunities(opps)
    assert "TRIANGULAR" in table
    assert "0.23" in table

def test_format_portfolio():
    p = PaperPortfolio(balance={"USDT": 10000}, total_trades=5, wins=3, losses=2, total_pnl=45.0)
    text = format_portfolio(p)
    assert "10,000" in text
    assert "45" in text
