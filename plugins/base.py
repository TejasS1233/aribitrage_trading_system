from abc import ABC, abstractmethod
from core.models import Ticker


class DataSource(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def fetch_tickers(self, symbols: list[str]) -> dict[str, dict[str, Ticker]]:
        pass

    @abstractmethod
    def get_exchange_names(self) -> list[str]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
