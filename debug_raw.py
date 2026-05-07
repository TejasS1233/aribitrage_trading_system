import ccxt

binance = ccxt.binance({'enableRateLimit': True})
kucoin = ccxt.kucoin({'enableRateLimit': True})
binance.load_markets()
kucoin.load_markets()

b = binance.fetch_ticker('BTC/USDT')
k = kucoin.fetch_ticker('BTC/USDT')

print("=== BINANCE API Response ===")
print(f"  ask: {b.get('ask')}")
print(f"  bid: {b.get('bid')}")
print()
print("=== KUCOIN API Response ===")
print(f"  ask: {k.get('ask')}")
print(f"  bid: {k.get('bid')}")
print()
print("=== MY CALCULATION ===")
print(f"Buy on Binance (ask): ${b['ask']}")
print(f"Sell on KuCoin (bid): ${k['bid']}")
spread = k['bid'] - b['ask']
print(f"Spread: ${spread:.2f}")
print()
print("=== FEE CALCULATION ===")
default_fee = 0.001
buy_fee = b['ask'] * default_fee
sell_fee = k['bid'] * default_fee
total_fee = buy_fee + sell_fee
print(f"Buy fee (0.1%): ${buy_fee:.2f}")
print(f"Sell fee (0.1%): ${sell_fee:.2f}")
print(f"Total fees: ${total_fee:.2f}")
print()
net = spread - total_fee
print("=== NET PROFIT ===")
print(f"Spread: ${spread:.2f}")
print(f"- Fees: ${total_fee:.2f}")
print(f"= Net: ${net:.2f}")