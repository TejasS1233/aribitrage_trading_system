from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ArbType(Enum):
    TRIANGULAR = "triangular"
    CROSS_EXCHANGE = "cross_exchange"
    CIRCULAR = "circular"

@dataclass
class Ticker:
    exchange: str
    symbol: str
    bid: float
    ask: float
    bid_volume: float
    ask_volume: float
    timestamp: datetime

@dataclass
class Opportunity:
    arb_type: ArbType
    exchanges: list[str]
    path: list[str]
    profit_pct: float
    profit_amount: float
    volume: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PaperTrade:
    opportunity: Opportunity
    entry_prices: dict[str, float]
    exit_prices: dict[str, float]
    volume: float
    realized_pnl: float
    fees_paid: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PaperPortfolio:
    balance: dict[str, float] = field(default_factory=lambda: {"USDT": 10000})
    total_value_usd: float = 10000.0
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    total_pnl: float = 0.0
