# Multi-Strategy Arbitrage Platform - Design Spec

## Goal

Build a multi-strategy arbitrage detection platform with a modern live web dashboard that actually detects real opportunities. The platform combines Binance WebSocket real-time triangular arbitrage, Polymarket binary outcome arbitrage, and REST cross-exchange arbitrage.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                Engine (main loop)                │
│  Runs detectors, collects results, sends to UI  │
└────────┬──────────┬──────────┬──────────────────┘
         │          │          │
    ┌────▼────┐ ┌───▼───┐ ┌───▼──────────┐
    │ Binance │ │Poly-  │ │ REST Cross-  │
    │WebSocket│ │market │ │ Exchange     │
    │ (100ms) │ │(poll) │ │ (2s poll)    │
    └────┬────┘ └───┬───┘ └───┬──────────┘
         │          │          │
    ┌────▼──────────▼──────────▼──────────┐
    │         Detection Results           │
    └────────┬──────────┬─────────────────┘
             │          │
    ┌────────▼──┐ ┌─────▼──────┐
    │ Terminal  │ │ Web        │
    │ Dashboard │ │ Dashboard  │
    │ (Rich)    │ │ (Flask+WS) │
    └───────────┘ └────────────┘
```

## Component 1: Binance WebSocket Real-Time Triangular Arb

### What it does
Connects to Binance free WebSocket API for real-time order book depth updates. Maintains local order book cache. Detects triangular arbitrage opportunities (A->B->C->A) using real depth data updated every 100ms.

### How it works
1. Discover all valid triangles from Binance exchange info (same algorithm as binance-triangle-arbitrage)
2. Subscribe to `depth@100ms` WebSocket streams for all symbols in triangles
3. Maintain local order book cache: `{symbol: {bids: [[price, qty], ...], asks: [[price, qty], ...]}}`
4. On every depth update, recalculate all triangles involving that symbol
5. For each triangle A->B->C->A:
   - Trade 1: Sell A for B (walk asks of A/B order book)
   - Trade 2: Sell B for C (walk asks of B/C order book)
   - Trade 3: Sell C for A (walk bids of C/A order book)
   - Profit = A_out - A_in
6. Report opportunities with profit > threshold

### WebSocket protocol
```
wss://stream.binance.com:9443/stream?streams=btcusdt@depth100ms/ethusdt@depth100ms/...
```

Combined stream format:
```json
{
  "stream": "btcusdt@depth100ms",
  "data": {
    "lastUpdateId": 123456,
    "bids": [["50000.00", "1.5"], ...],
    "asks": [["50001.00", "2.0"], ...]
  }
}
```

### Triangle discovery algorithm
```python
# Get all symbols from Binance
symbols = exchange.load_markets()

# Find all base/quote assets
assets = set()
for symbol in symbols:
    base, quote = symbol.split('/')
    assets.add(base)
    assets.add(quote)

# Generate all triangles starting from configured bases
triangles = []
for a in bases:
    for b in assets:
        for c in assets:
            # Check if all three markets exist
            if has_market(a, b) and has_market(b, c) and has_market(c, a):
                triangles.append((a, b, c))
```

### Files
- `plugins/binance_ws/binance_websocket.py` - WebSocket connection and depth cache
- `plugins/binance_ws/triangle_finder.py` - Triangle discovery and profit calculation
- `plugins/binance_ws/order_book.py` - Local order book maintenance

---

## Component 2: Polymarket Binary Outcome Arb

### What it does
Polls Polymarket API for prediction markets where YES + NO token prices < $1.00, indicating an arbitrage opportunity.

### How it works
1. Fetch active markets from `https://gamma-api.polymarket.com`
2. For each market, get YES and NO token prices
3. Calculate `total_cost = yes_price + no_price`
4. If `total_cost < 1.00`, profit = `1.00 - total_cost`
5. Report as POLYMARKET arbitrage opportunity

### API endpoints
- Markets: `GET https://gamma-api.polymarket.com/markets`
- Prices: embedded in market response (outcomePrices field)

### Files
- `plugins/polymarket/polymarket_adapter.py` - Already exists, just needs integration

---

## Component 3: REST Cross-Exchange (Keep Existing)

### What it does
Keep the existing REST polling cross-exchange and Bellman-Ford detection. Unlikely to find opportunities on major pairs but provides completeness.

### No changes needed
Existing code works, just keep it running alongside the new components.

---

## Component 4: Live Web Dashboard

### Design principles
- **Dark theme** - professional, easy on eyes, looks modern
- **Real-time updates** - WebSocket from backend to browser
- **Minimal, clean** - no clutter, focus on data
- **Responsive** - works on desktop and mobile
- **Inspired by:** TradingView dark theme, Bloomberg Terminal aesthetic, Vercel dashboard simplicity

### Tech stack
- **Backend:** Flask + Flask-SocketIO (simple, no build step)
- **Frontend:** Single HTML file, vanilla JS, Tailwind CSS (CDN), Chart.js (CDN)
- **Real-time:** Socket.IO for backend->browser updates
- **No build step** - just `python main.py` and open browser

### Dashboard layout

```
┌──────────────────────────────────────────────────────────┐
│  ARBITRAGE DETECTOR                           [Live] ●   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Total    │ │ Active   │ │ Best     │ │ Detection│   │
│  │ Opps     │ │ Strategies│ │ Profit   │ │ Latency  │   │
│  │ 1,247    │ │ 3        │ │ 0.42%    │ │ 12ms     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                          │
│  ┌──────────────────────────┐ ┌────────────────────────┐ │
│  │  Opportunities Over Time │ │  Profit Distribution   │ │
│  │  [line chart]            │ │  [histogram]           │ │
│  │                          │ │                        │ │
│  └──────────────────────────┘ └────────────────────────┘ │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  LIVE OPPORTUNITIES                              │   │
│  │  ┌─────────────────────────────────────────────┐ │   │
│  │  │ Type    │ Path              │ Profit │ Time │ │   │
│  │  │─────────┼───────────────────┼────────┼──────│ │   │
│  │  │ TRI     │ BTC->ETH->USDT   │ 0.32%  │ 12ms │ │   │
│  │  │ POLY    │ Election 2024     │ 0.15%  │ 45ms │ │   │
│  │  │ CROSS   │ BTC binance/coin  │ 0.08%  │ 23ms │ │   │
│  │  └─────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────┐ ┌────────────────────────┐ │
│  │  Detection Latency       │ │  Opportunities/Min     │ │
│  │  [histogram]             │ │  [bar chart]           │ │
│  └──────────────────────────┘ └────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Color scheme (dark theme)
- Background: #0a0a0f (near black)
- Cards: #12121a (dark gray)
- Accent: #10b981 (green for profit)
- Warning: #f59e0b (amber)
- Text: #e5e7eb (light gray)
- Muted: #6b7280 (gray)
- Chart lines: #3b82f6 (blue), #10b981 (green), #f59e0b (amber)

### Typography
- Font: Inter (Google Fonts) or system-ui
- Monospace for numbers: JetBrains Mono or monospace

### Stats cards
- Total opportunities detected (all time)
- Active strategies (how many are running)
- Best profit % seen
- Average detection latency

### Charts (Chart.js)
1. **Opportunities over time** - Line chart, x=minutes, y=opportunities detected
2. **Profit distribution** - Histogram, x=profit%, y=count
3. **Detection latency** - Histogram, x=ms, y=count
4. **Opportunities per minute** - Bar chart, grouped by strategy type

### Live opportunity table
- Newest at top
- Color-coded by type (green=triangular, blue=poly, orange=cross)
- Shows: type, path, profit%, detection latency, timestamp
- Auto-scrolls, keeps last 100

### Files
- `output/web_dashboard.py` - Flask + SocketIO server
- `output/templates/dashboard.html` - Single-page dashboard (all HTML/CSS/JS inline)
- `output/static/` - Empty (everything inline for simplicity)

---

## Component 5: Historical Analytics

### What gets tracked
Every detected opportunity stores:
- timestamp (ISO format)
- arb_type (TRIANGULAR, POLYMARKET, CROSS_EXCHANGE, BELLMAN_FORD)
- path (e.g., "BTC->ETH->USDT->BTC" or "Election 2024 YES+NO")
- profit_pct
- volume (if available)
- detection_latency_ms
- exchange(s)

### Aggregates (computed in-memory, displayed on dashboard)
- Total opportunities (all time, last hour, last minute)
- Average profit by strategy
- Detection latency p50, p95, p99
- Opportunities per minute by strategy

### Files
- `core/analytics.py` - In-memory analytics tracker
- `output/database.py` - Already exists, add new tables

---

## Updated Engine Flow

```
Startup:
  1. Load config
  2. Connect to Binance REST (for market info)
  3. Start Binance WebSocket (depth streams)
  4. Start Polymarket poller (if enabled)
  5. Start REST cross-exchange poller (if enabled)
  6. Start web dashboard (Flask + SocketIO)
  7. Start terminal dashboard (Rich)

Main loop (runs forever):
  1. Binance WS delivers depth update -> recalculate affected triangles
  2. Polymarket poller delivers markets -> check for under-par
  3. REST poller delivers tickers -> check cross-exchange + Bellman-Ford
  4. All opportunities -> analytics tracker -> database -> web dashboard -> terminal
```

### Threading model
- Main thread: Engine coordination
- Thread 1: Binance WebSocket (asyncio or threading)
- Thread 2: Polymarket poller (REST, sleep between polls)
- Thread 3: REST cross-exchange poller (existing)
- Thread 4: Flask web server (Flask-SocketIO handles its own threading)

### Files modified
- `core/engine.py` - Add Binance WS and Polymarket as data sources
- `main.py` - Wire everything together, start web dashboard
- `config.yaml` - Add binance_ws section, web_dashboard section

---

## Config additions

```yaml
binance_ws:
  enabled: true
  base_assets:
    - BTC
    - ETH
    - BNB
    - SOL
  min_profit_pct: 0.1
  max_triangles: 1000

web_dashboard:
  enabled: true
  host: "127.0.0.1"
  port: 8080

polymarket:
  enabled: true
  poll_interval: 30
```

---

## Dependencies to add

```
flask>=3.0
flask-socketio>=5.3
python-socketio>=5.10
websockets>=12.0
```

---

## Testing strategy

1. Unit tests for triangle discovery algorithm
2. Unit tests for order book depth walking
3. Unit tests for Polymarket under-par detection
4. Unit tests for analytics aggregation
5. Integration test: mock WebSocket messages -> verify opportunities detected
6. Integration test: mock Polymarket API -> verify opportunities detected
7. E2E test: start engine with mock data -> verify dashboard receives updates
