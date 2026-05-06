import asyncio
import ccxt.async_support as ccxt

async def main():
    # Force system DNS resolver
    ex = ccxt.binance({"enableRateLimit": True})
    await ex.load_markets()
    print(f"Binance: {len(ex.markets)} markets loaded")

    tickers = await ex.fetch_tickers(["BTC/USDT", "ETH/USDT", "ETH/BTC", "SOL/USDT"])
    for sym, t in tickers.items():
        bid = t.get("bid") or 0
        ask = t.get("ask") or 0
        spread_pct = ((ask - bid) / ask) * 100 if ask else 0
        print(f"  {sym:12s}  bid={bid:<12.2f}  ask={ask:<12.2f}  spread={spread_pct:.4f}%")

    await ex.close()

# Use SelectorEventLoop on Windows (avoids aiodns issues)
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
