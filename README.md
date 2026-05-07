# crypto-arbitrage-detector

> **Disclaimer:** This project is for educational and research purposes only. It is not financial advice. Do not use this for actual trading or investment. Crypto markets are extremely competitive - real arbitrage opportunities are captured by HFT firms with sub-millisecond infrastructure. This tool will not make you money.

Arbitrage monitoring system that detects price discrepancies across 100+ crypto exchanges and paper-trades them.

## What it does

- **Cross-exchange arbitrage** - buys BTC cheap on Coinbase, sells expensive on Binance
- **Triangular arbitrage** - cycles through 3 currencies on one exchange (e.g. BTC->ETH->USDT->BTC)
- **Bellman-Ford multi-hop detection** - finds negative-weight cycles across exchange rate graphs
- **Symbol auto-discovery** - automatically finds tradeable pairs across connected exchanges
- **Stale data filtering** - discards tickers older than a configurable threshold
- **WebSocket streaming** - real-time price updates via ccxt.pro (when enabled)
- **DEX monitoring** - reads Uniswap V2 on-chain reserves for cross-DEX arb detection
- **Polymarket adapter** - detects under-par binary outcome tokens (YES+NO < $1)
- **Optimal trade size** - calculates best volume based on order book depth
- **Paper trading** - simulates trades with fake money, tracks PnL, win rate, fees
- **Live terminal dashboard** - Rich-powered display of opportunities and portfolio
- **SQLite history** - logs every opportunity and trade to a local database

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
  default: 0.0001          # Uses MAKER fees (0.01%) - realistic for high-volume traders
  binance: 0.0001        # See fee tiers: https://www.binance.com/en/fee/schedule
  coinbase: 0.0005

poll_interval: 1.0       # seconds between checks
min_profit_pct: 0.05      # minimum profit % to log
starting_balance:
  USDT: 10000

auto_discover:
  enabled: false           # auto-find tradeable symbols
  min_volume_24h: 100000

websocket:
  enabled: false           # requires ccxt-pro

stale_filter:
  enabled: true
  max_age_seconds: 10.0

dex:
  enabled: false           # requires Ethereum RPC
  rpc_url: "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"

polymarket:
  enabled: false
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
│   ├── engine.py              # main loop - fetch -> detect -> paper trade -> display
│   ├── stale_filter.py        # discard old tickers
│   ├── symbol_discovery.py    # auto-find tradeable symbols
│   └── arbitrage/
│       ├── cross_exchange.py  # buy low on A, sell high on B
│       ├── triangular.py      # A->B->C->A cycle detection
│       ├── bellman_ford.py    # negative-weight cycle detection
│       └── optimal_size.py    # trade size calculator
├── plugins/
│   ├── base.py                # abstract DataSource interface
│   ├── cex/
│   │   └── ccxt_adapter.py    # ccxt implementation for 100+ exchanges
│   ├── dex/
│   │   └── uniswap_v2.py      # on-chain reserve monitoring
│   ├── polymarket/
│   │   └── polymarket_adapter.py  # binary outcome arb
│   └── websocket/
│       └── ws_manager.py      # real-time WebSocket streaming
├── output/
│   ├── terminal.py            # Rich dashboard
│   └── database.py            # SQLite persistence
└── tests/
```

## Learning the concepts

If you want to understand how arbitrage actually works - AMM math, graph theory, flash loans, MEV, order books, Bellman-Ford for cycle detection, and 200+ other concepts - see [MASTERY-CONCEPTS.md](MASTERY-CONCEPTS.md).

It's a textbook-length reference compiled from 13 open-source arbitrage repos, organized into 10 chapters covering everything from blockchain fundamentals to trading system architecture.

## Fee Note

This bot uses **maker fees** (0.01%) by default. To get these rates:
- Trade $100k+/month on Binance → 0.02% maker
- Trade $1M+/month → 0.01% maker
- Most retail traders pay 0.1% (taker fees)

The bot will find MORE opportunities with lower fees. Adjust `fees.default` in config.yaml based on your volume tier.
