import json
import requests
from datetime import datetime
from core.models import Ticker


UNISWAP_V2_FACTORY = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
SUSHISWAP_FACTORY = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
UNISWAP_V2_PAIR_ABI = json.loads('[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"name":"_reserve0","type":"uint112"},{"name":"_reserve1","type":"uint112"},{"name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]')

TOKEN_DECIMALS = {
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": 18,  # WETH
    "0xdAC17F958D2ee523a2206206994597C13D831ec7": 6,   # USDT
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": 6,   # USDC
    "0x6B175474E89094C44Da98b954EedeAC495271d0F": 18,  # DAI
    "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": 8,   # WBTC
}


class UniswapV2Adapter:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.pairs = {}

    def fetch_reserves(self, pair_address: str) -> tuple[int, int]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_call",
            "params": [{
                "to": pair_address,
                "data": "0x0902f1ac",  # getReserves()
            }, "latest"],
        }
        resp = requests.post(self.rpc_url, json=payload, timeout=10)
        data = resp.json().get("result", "0x" + "0" * 192)
        reserve0 = int(data[2:66], 16)
        reserve1 = int(data[66:130], 16)
        return reserve0, reserve1

    def get_pair_ticker(
        self,
        pair_address: str,
        symbol: str,
        decimals0: int,
        decimals1: int,
    ) -> Ticker | None:
        try:
            reserve0, reserve1 = self.fetch_reserves(pair_address)
            if reserve0 == 0 or reserve1 == 0:
                return None
            price = calculate_price(reserve0, reserve1, decimals0, decimals1)
            return Ticker(
                exchange="uniswap_v2",
                symbol=symbol,
                bid=price * 0.999,
                ask=price * 1.001,
                bid_volume=reserve1 / (10 ** decimals1),
                ask_volume=reserve0 / (10 ** decimals0),
                timestamp=datetime.now(),
            )
        except Exception:
            return None


def calculate_price(
    reserve0: int,
    reserve1: int,
    decimals0: int,
    decimals1: int,
) -> float:
    adj_reserve0 = reserve0 / (10 ** decimals0)
    adj_reserve1 = reserve1 / (10 ** decimals1)
    if adj_reserve0 == 0:
        return 0.0
    return adj_reserve1 / adj_reserve0
