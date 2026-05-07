import os
import time
import logging
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
        self.debug = bool(config.get("debug")) or os.getenv("ARB_DEBUG") == "1"
        self.logger = logging.getLogger(self.__class__.__name__)
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
            source_label = "websocket"
        else:
            tickers = self.source.fetch_tickers(self.symbols)
            source_label = "polling"

        if not tickers:
            if self.debug:
                self.logger.info("No tickers returned (source=%s)", source_label)
            return

        if self.debug:
            total_symbols = sum(len(ex) for ex in tickers.values())
            self.logger.info(
                "Tickers fetched (source=%s exchanges=%d symbols=%d min_profit=%.4f)",
                source_label,
                len(tickers),
                total_symbols,
                self.min_profit,
            )

        tickers = filter_stale_tickers(tickers, self.stale_max_age)
        if not tickers:
            if self.debug:
                self.logger.info("All tickers filtered as stale (max_age=%.2fs)", self.stale_max_age)
            return

        if self.debug:
            total_symbols = sum(len(ex) for ex in tickers.values())
            self.logger.info(
                "Tickers after stale filter (exchanges=%d symbols=%d)",
                len(tickers),
                total_symbols,
            )

        opportunities = []
        opportunities += find_triangular_opportunities(tickers, self.fees, self.min_profit)
        opportunities += find_cross_exchange_opportunities(tickers, self.fees, self.min_profit)
        opportunities += find_bellman_ford_opportunities(tickers, self.fees, self.min_profit)

        if self.debug:
            self.logger.info(
                "Opportunities found (triangular=%d cross=%d bellman=%d total=%d)",
                sum(1 for o in opportunities if o.arb_type.value == "triangular"),
                sum(1 for o in opportunities if o.arb_type.value == "cross_exchange"),
                sum(1 for o in opportunities if o.arb_type.value == "bellman_ford"),
                len(opportunities),
            )

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
