# crypto-arbitrage-detector

Crypto arbitrage detection system that monitors price discrepancies across 100+ exchanges and paper-trades them.

## Features

- **Cross-exchange arbitrage** — buy low on one exchange, sell high on another
- **Triangular arbitrage** — cycle through 3 pairs on one exchange
- **Bellman-Ford detection** — find complex multi-hop opportunities
- **Paper trading** — test strategies with fake money, tracks PnL, win rate, fees
- **Slippage simulation** — 30% of profit lost to market impact and timing
- **Live terminal** — see opportunities in real-time

Works with Binance, Coinbase, Kraken, and 100+ other exchanges.
## Quick start

```bash
uv venv
uv pip install -r requirements.txt
python main.py
```

## Configuration

Edit `config.yaml`:

```yaml
exchanges:
  - binance
  - coinbase
  - kraken

symbols:
  - BTC/USDT
  - ETH/USDT
  - ETH/BTC

fees:
  default: 0.0001
  binance: 0.0001
  coinbase: 0.0005

poll_interval: 1.0
min_profit_pct: 0.05
min_volume: 100
starting_balance:
  USDT: 10000
```

## Running tests

```bash
python -m pytest tests/ -v
```

## Project structure

```
├── main.py              # entry point
├── config.yaml        # settings
├── core/
│   ├── engine.py     # main loop
│   ├── models.py    # data structures
│   └── arbitrage/  # detection algorithms
├── plugins/
│   ├── cex/ccxt_adapter.py    # exchange connectivity
│   ├── dex/uniswap_v2.py      # on-chain data
│   └── polymarket/           # prediction markets
└── tests/            # test suite
```

## Learning

Want to understand arbitrage? See [MASTERY-CONCEPTS.md](MASTERY-CONCEPTS.md) — covers AMM math, graph theory, flash loans, MEV, and 200+ other concepts.

## Fee Note

This bot uses **maker fees** (0.01%) by default. To get these rates:
- Trade $100k+/month on Binance → 0.02% maker
- Trade $1M+/month → 0.01% maker
- Most retail traders pay 0.1% (taker fees)

The bot will find MORE opportunities with lower fees. Adjust `fees.default` in config.yaml based on your volume tier.

---

> **Disclaimer:** This project is for educational purposes only. Not financial advice.