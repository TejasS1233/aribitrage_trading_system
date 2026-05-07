import ccxt
from core.models import Ticker
from core.arbitrage.cross_exchange import find_cross_exchange_opportunities
from datetime import datetime

binance = ccxt.binance({'enableRateLimit': True})
kucoin = ccxt.kucoin({'enableRateLimit': True})
binance.load_markets()
kucoin.load_markets()

common = [s for s in binance.markets.keys() if s in kucoin.markets][:10]
b = binance.fetch_tickers(common)
k = kucoin.fetch_tickers(common)

tickers = {'binance': {}, 'kucoin': {}}
for sym, t in b.items():
    if t.get('bid') and t.get('ask'):
        tickers['binance'][sym] = Ticker('binance', sym, t['bid'], t['ask'], t.get('bidVolume',0), t.get('askVolume',0), datetime.now())
for sym, t in k.items():
    if t.get('bid') and t.get('ask'):
        tickers['kucoin'][sym] = Ticker('kucoin', sym, t['bid'], t['ask'], t.get('bidVolume',0), t.get('askVolume',0), datetime.now())

# Try different fee thresholds
for fee in [0, 0.00005, 0.0001, 0.0002]:
    fees = {'default': fee, 'binance': fee, 'kucoin': fee}
    opps = find_cross_exchange_opportunities(tickers, fees, 0.0)  # Any positive
    print(f"Fee {fee*100:.3f}%: {len(opps)} opportunities")
    if opps:
        for o in opps[:3]:
            print(f"  {o.path}: {o.profit_pct:.4f}%")