import time
from core.models import PaperPortfolio, PaperTrade, Opportunity
from core.arbitrage.triangular import find_triangular_opportunities
from core.arbitrage.cross_exchange import find_cross_exchange_opportunities
from core.arbitrage.bellman_ford import find_bellman_ford_opportunities
from core.stale_filter import filter_stale_tickers
from plugins.base import DataSource


class Engine:
    def __init__(self, config: dict, data_source: DataSource, outputs: list, ws_manager=None):
        self.config = config
        self.source = data_source
        self.outputs = outputs
        self.ws_manager = ws_manager
        self.portfolio = PaperPortfolio(
            balance=dict(config.get("starting_balance", {"USDT": 10000}))
        )
        self.min_profit = config.get("min_profit_pct", 0.05)
        self.fees = config.get("fees", {"default": 0.001})
        self.poll_interval = config.get("poll_interval", 1.0)
        self.symbols = config.get("symbols", [])
        self.stale_max_age = config.get("stale_filter", {}).get("max_age_seconds", 5.0)

    def run_once(self):
        if self.ws_manager and self.ws_manager.is_connected():
            tickers = self.ws_manager.get_tickers(self.symbols)
        else:
            tickers = self.source.fetch_tickers(self.symbols)

        if not tickers:
            return

        tickers = filter_stale_tickers(tickers, self.stale_max_age)
        if not tickers:
            return

        opportunities = []
        opportunities += find_triangular_opportunities(tickers, self.fees, self.min_profit)
        opportunities += find_cross_exchange_opportunities(tickers, self.fees, self.min_profit)
        opportunities += find_bellman_ford_opportunities(tickers, self.fees, self.min_profit)

        for opp in opportunities:
            if opp.profit_pct >= self.min_profit:
                trade = self._paper_trade(opp)
                self.portfolio.total_trades += 1
                if trade.realized_pnl > 0:
                    self.portfolio.wins += 1
                else:
                    self.portfolio.losses += 1
                self.portfolio.total_pnl += trade.realized_pnl

        for output in self.outputs:
            output.update(opportunities, self.portfolio)

    def _paper_trade(self, opp: Opportunity) -> PaperTrade:
        default_fee = self.fees.get("default", 0.001)
        fee_rate = default_fee
        total_fees = opp.volume * (opp.profit_pct / 100) * fee_rate * len(opp.path)
        realized_pnl = opp.profit_amount - total_fees

        return PaperTrade(
            opportunity=opp,
            entry_prices={},
            exit_prices={},
            volume=opp.volume,
            realized_pnl=round(realized_pnl, 4),
            fees_paid=round(total_fees, 4),
        )

    def run(self):
        self.source.connect()
        try:
            while True:
                self.run_once()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            pass
        finally:
            self.source.close()
