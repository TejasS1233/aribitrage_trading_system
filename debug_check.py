import ccxt
from core.arbitrage.cross_exchange import find_cross_exchange_opportunities
from core.models import Ticker
from datetime import datetime

binance = ccxt.binance({'enableRateLimit': True})
kucoin = ccxt.kucoin({'enableRateLimit': True})
binance.load_markets()
kucoin.load_markets()

common = [s for s in binance.markets.keys() if s in kucoin.markets][:10]
print(f'Fetching: {common}')

b_tickers = binance.fetch_tickers(common)
k_tickers = kucoin.fetch_tickers(common)

tickers = {'binance': {}, 'kucoin': {}}
for sym, t in b_tickers.items():
    if t.get('bid') and t.get('ask'):
        tickers['binance'][sym] = Ticker('binance', sym, t['bid'], t['ask'], t.get('bidVolume',0), t.get('askVolume',0), datetime.now())

for sym, t in k_tickers.items():
    if t.get('bid') and t.get('ask'):
        tickers['kucoin'][sym] = Ticker('kucoin', sym, t['bid'], t['ask'], t.get('bidVolume',0), t.get('askVolume',0), datetime.now())

print(f'Binance tickers: {len(tickers["binance"])}')
print(f'KuCoin tickers: {len(tickers["kucoin"])}')

# Debug: print actual prices
for sym in tickers['binance']:
    if sym in tickers['kucoin']:
        b = tickers['binance'][sym]
        k = tickers['kucoin'][sym]
        spread = k.bid - b.ask
        print(f'{sym}: binance ask={b.ask} bid={b.bid}, kucoin ask={k.ask} bid={k.bid}, spread={spread:.4f}')

opps = find_cross_exchange_opportunities(tickers, {'default': 0.001}, 0.0)
print(f'Opportunities with 0% min: {len(opps)}')
if opps:
    for o in opps[:3]:
        print(f'  {o.path}: {o.profit_pct:.4f}%')
else:
    print('No opportunities found')