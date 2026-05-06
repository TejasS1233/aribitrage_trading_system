import sqlite3
import json
from datetime import datetime
from core.models import Opportunity, PaperTrade, PaperPortfolio

class Database:
    def __init__(self, path: str = "data/trades.db"):
        self.path = path
        self.conn = None

    def connect(self):
        import os
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                arb_type TEXT,
                exchanges TEXT,
                path TEXT,
                profit_pct REAL,
                profit_amount REAL,
                volume REAL
            );
            CREATE TABLE IF NOT EXISTS paper_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                arb_type TEXT,
                exchanges TEXT,
                path TEXT,
                volume REAL,
                realized_pnl REAL,
                fees_paid REAL
            );
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                balance TEXT,
                total_value_usd REAL,
                total_trades INTEGER,
                wins INTEGER,
                losses INTEGER,
                total_pnl REAL
            );
        """)

    def save_opportunity(self, opp: Opportunity):
        self.conn.execute(
            "INSERT INTO opportunities (timestamp, arb_type, exchanges, path, profit_pct, profit_amount, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (opp.timestamp.isoformat(), opp.arb_type.value, json.dumps(opp.exchanges), json.dumps(opp.path), opp.profit_pct, opp.profit_amount, opp.volume)
        )
        self.conn.commit()

    def save_trade(self, trade: PaperTrade):
        self.conn.execute(
            "INSERT INTO paper_trades (timestamp, arb_type, exchanges, path, volume, realized_pnl, fees_paid) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (trade.timestamp.isoformat(), trade.opportunity.arb_type.value, json.dumps(trade.opportunity.exchanges), json.dumps(trade.opportunity.path), trade.volume, trade.realized_pnl, trade.fees_paid)
        )
        self.conn.commit()

    def save_portfolio(self, portfolio: PaperPortfolio):
        self.conn.execute(
            "INSERT INTO portfolio_snapshots (timestamp, balance, total_value_usd, total_trades, wins, losses, total_pnl) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), json.dumps(portfolio.balance), portfolio.total_value_usd, portfolio.total_trades, portfolio.wins, portfolio.losses, portfolio.total_pnl)
        )
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
