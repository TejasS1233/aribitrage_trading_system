"""Arbitrage Monitor — Paper Trading System"""
import asyncio
import yaml

def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)

async def main():
    config = load_config()
    print("Arbitrage Monitor starting...")
    print(f"Exchanges: {config['exchanges']}")
    print(f"Symbols: {config['symbols']}")

if __name__ == "__main__":
    asyncio.run(main())
