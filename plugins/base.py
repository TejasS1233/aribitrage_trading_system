from abc import ABC, abstractmethod
from core.models import Ticker

class DataSource(ABC):
    """Abstract interface for all data sources (CEX, DEX)."""

    @abstractmethod
    async def connect(self) -> None:
        """Initialize connections and load markets."""

    @abstractmethod
    async def fetch_tickers(self, symbols: list[str]) -> dict[str, dict[str, Ticker]]:
        """Fetch tickers for all symbols.
        Returns: {"binance": {"BTC/USDT": Ticker(...), ...}, ...}
        """

    @abstractmethod
    async def get_exchange_names(self) -> list[str]:
        """Return list of exchange names this adapter covers."""

    @abstractmethod
    async def close(self) -> None:
        """Clean up connections."""
