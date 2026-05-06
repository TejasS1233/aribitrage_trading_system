# arb-lab

Arbitrage monitoring system that detects price discrepancies across 100+ crypto exchanges and paper-trades them.

## What it does

- **Cross-exchange arbitrage** — buys BTC cheap on Coinbase, sells expensive on Binance
- **Triangular arbitrage** — cycles through 3 currencies on one exchange (e.g. BTC→ETH→USDT→BTC)
- **Paper trading** — simulates trades with fake money, tracks PnL, win rate, fees
- **Live terminal dashboard** — Rich-powered display of opportunities and portfolio
- **SQLite history** — logs every opportunity and trade to a local database

Uses ccxt for exchange connectivity, so it works with Binance, Coinbase, Kraken, and 100+ other exchanges out of the box.

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
  default: 0.001
  binance: 0.001
  coinbase: 0.005

poll_interval: 1.0       # seconds between checks
min_profit_pct: 0.05      # minimum profit % to log
starting_balance:
  USDT: 10000
```

## Tests

```bash
python -m pytest tests/ -v
```

## Project structure

```
├── main.py                    # entry point
├── config.yaml                # exchange/symbol/fee settings
├── core/
│   ├── models.py              # Ticker, Opportunity, PaperTrade, PaperPortfolio
│   ├── engine.py              # main loop — fetch → detect → paper trade → display
│   └── arbitrage/
│       ├── cross_exchange.py  # buy low on A, sell high on B
│       └── triangular.py      # A→B→C→A cycle detection
├── plugins/
│   ├── base.py                # abstract DataSource interface
│   └── cex/
│       └── ccxt_adapter.py    # ccxt implementation for 100+ exchanges
├── output/
│   ├── terminal.py            # Rich dashboard
│   └── database.py            # SQLite persistence
└── tests/
```

## Roadmap

### Phase 1: CEX Monitoring (current)
- [x] Cross-exchange arbitrage detection
- [x] Triangular arbitrage detection
- [x] Paper trading with PnL tracking
- [x] Rich terminal dashboard
- [x] SQLite trade history

### Phase 2: More Data Sources
- [ ] DEX monitoring (Uniswap, Raydium, Orca via on-chain RPC)
- [ ] Prediction market arbitrage (Polymarket par relationship)
- [ ] WebSocket streaming (real-time order book updates instead of polling)
- [ ] More symbols — auto-discover all shared trading pairs across exchanges

### Phase 3: Smarter Detection
- [ ] Bellman-Ford negative cycle detection (multi-hop paths beyond 3 currencies)
- [ ] Optimal trade size calculation (account for order book depth / price impact)
- [ ] Fee-aware routing (different fee tiers per exchange, BNB discounts, etc.)
- [ ] Stale data filtering (reject quotes older than N seconds)

### Phase 4: Execution
- [ ] Live trading mode (real orders via ccxt)
- [ ] Flash loan arbitrage on-chain (Solidity smart contract)
- [ ] Jito bundle submission (Solana MEV)
- [ ] Flashbots integration (Ethereum MEV)
- [ ] Risk management (position limits, max exposure, single-leg recovery)

### Phase 5: Production
- [ ] Web dashboard (live portfolio view)
- [ ] Alerting (Telegram/Discord notifications on opportunities)
- [ ] Multi-strategy support (run multiple arb strategies concurrently)
- [ ] Backtesting engine (replay historical data)

## Learning the concepts

If you want to understand how arbitrage actually works — AMM math, graph theory, flash loans, MEV, order books, Bellman-Ford for cycle detection, and 200+ other concepts — see [MASTERY-CONCEPTS.md](MASTERY-CONCEPTS.md).

It's a textbook-length reference compiled from 13 open-source arbitrage repos, organized into 10 chapters covering everything from blockchain fundamentals to trading system architecture.
