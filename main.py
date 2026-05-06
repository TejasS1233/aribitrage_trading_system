import yaml
from core.engine import Engine
from plugins.cex.ccxt_adapter import CCXTAdapter
from output.terminal import format_opportunities, format_portfolio, clear_screen
from output.database import Database


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    print("Arbitrage Monitor starting...")

    source = CCXTAdapter(config["exchanges"])
    source.connect()
    print(f"Connected to {len(config['exchanges'])} exchanges")

    db = Database(config.get("database", {}).get("path", "data/trades.db"))
    db.connect()

    class TerminalOutput:
        def update(self, opportunities, portfolio):
            clear_screen()
            format_opportunities(opportunities, config.get("terminal", {}).get("max_rows", 10))
            format_portfolio(portfolio)
            for opp in opportunities:
                if opp.profit_pct >= config.get("min_profit_pct", 0.05):
                    db.save_opportunity(opp)
            db.save_portfolio(portfolio)

    engine = Engine(config, source, [TerminalOutput()])
    print(f"Monitoring {len(config['symbols'])} symbols")
    print(f"Poll interval: {config['poll_interval']}s")
    print(f"Min profit: {config['min_profit_pct']}%")
    print("\nPress Ctrl+C to stop\n")

    try:
        engine.run()
    finally:
        db.close()
        source.close()


if __name__ == "__main__":
    main()
