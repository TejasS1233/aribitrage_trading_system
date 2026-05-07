# modular-arbitrage-engine

Modular arbitrage execution engine with plugin-based exchange integration, paper trading, and configurable slippage models.

## Features

- **Plugin-based architecture** - add new exchanges, DEXs, or data sources easily
- Cross-exchange arbitrage across 100+ exchanges via CCXT + custom plugin adapters
- Triangular arbitrage within single exchanges
- Bellman-Ford graph-based arbitrage detection
- Paper trading with PnL tracking and win rate analytics
- Configurable slippage simulation (conservative default: 30%)
- Live terminal + web dashboard for real-time opportunity monitoring
  
Unlike typical trading bots, this project is designed as a modular research and execution framework for arbitrage systems.
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
## Live Arbitrage Detection Output (real-time scan)
Live output from the arbitrage engine scanning multiple markets in real time:

<img width="647" height="112" alt="Screenshot 2026-05-07 222503" src="https://github.com/user-attachments/assets/681704e1-2df3-4603-b740-834cc82fa073" />


<img width="647" height="65" alt="Screenshot 2026-05-07 222444" src="https://github.com/user-attachments/assets/0891defa-0728-4319-ac14-d1013f578fa6" />

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

## Learning Resources

Want to understand arbitrage? See [MASTERY-CONCEPTS.md](MASTERY-CONCEPTS.md) — covers AMM math, graph theory, flash loans, MEV and arbitrage market structure.
## Fee Note

Default maker fee: 0.01% (configurable per exchange)

Lower fee tiers significantly impact detected arbitrage opportunities.

All fees can be adjusted in `config.yaml` based on your trading volume tier.

## Notes

This project is experimental and focused on modeling realistic arbitrage conditions rather than guaranteed profitability.

Feedback, improvements, and contributions are welcome.

> **Disclaimer:** This project is for educational purposes only. Not financial advice.
