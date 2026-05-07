import os
import yaml
import logging
from dotenv import load_dotenv
load_dotenv()
from core.engine import Engine
from core.symbol_discovery import SymbolDiscovery
from plugins.cex.ccxt_adapter import CCXTAdapter
from plugins.websocket.ws_manager import WebSocketManager
from output.terminal import format_opportunities, format_portfolio, clear_screen
from output.database import Database
from core.ai_advice import generate_ai_advice
from flask import Flask, send_from_directory
import json
import threading
import time


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    debug_enabled = bool(config.get("debug")) or os.getenv("ARB_DEBUG") == "1"
    if debug_enabled:
        logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
        logging.getLogger("urllib3").setLevel(logging.WARNING)
    print("Arbitrage Monitor starting...", flush=True)

    source = CCXTAdapter(config["exchanges"])
    if debug_enabled:
        source.set_debug(True)
    source.connect()
    print(f"Connected to {len(config['exchanges'])} exchanges", flush=True)

    symbols = config.get("symbols", [])
    if config.get("auto_discover", {}).get("enabled", False):
        print("Auto-discovering symbols...", flush=True)
        discovery = SymbolDiscovery(
            source.exchanges,
            min_volume=config["auto_discover"].get("min_volume_24h", 100000),
        )
        discovery.discover()
        discovered = discovery.get_all_symbols()
        if discovered:
            symbols = discovered
            print(f"  Found {len(symbols)} symbols", flush=True)
        else:
            print("  No symbols discovered, using config", flush=True)

    ws_manager = None
    if config.get("websocket", {}).get("enabled", False):
        print("Starting WebSocket manager...", flush=True)
        ws_manager = WebSocketManager(source.exchange_names, symbols)
        ws_manager.start()

    db = Database(config.get("database", {}).get("path", "data/trades.db"))
    db.connect()

    cycle_count = [0]

    class TerminalOutput:
        def update(self, opportunities, portfolio):
            cycle_count[0] += 1
            clear_screen()
            format_opportunities(opportunities, config.get("terminal", {}).get("max_rows", 10))
            format_ai_advice(opportunities, config)
            format_portfolio(portfolio)
            for opp in opportunities:
                if opp.profit_pct >= config.get("min_profit_pct", 0.05):
                    db.save_opportunity(opp)
            db.save_portfolio(portfolio)

config["symbols"] = symbols

    WEB_STATE = {
        "portfolio": {"balance": 10000, "trades": 0, "wins": 0, "losses": 0},
        "opportunities": [],
        "exchanges": config["exchanges"],
        "ai_advice": None
    }

    engine = Engine(config, source, [TerminalOutput()], ws_manager=ws_manager)
    print(f"Monitoring {len(symbols)} symbols", flush=True)

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return send_from_directory("templates", "dashboard.html")

@app.route("/api/status")
def api_status():
    return {
        "portfolio": WEB_STATE["portfolio"],
        "opportunities": [
            {
                "path": o.path,
                "exchanges": o.exchanges,
                "profit": o.profit_pct,
                "type": o.arb_type.value
            }
            for o in WEB_STATE["opportunities"]
        ],
        "exchanges": WEB_STATE["exchanges"],
        "ai_advice": WEB_STATE["ai_advice"]
    }

def run_flask():
    app.run(port=5000, debug=False)

def main():
    config = load_config()
    debug_enabled = bool(config.get("debug")) or os.getenv("ARB_DEBUG") == "1"
    if debug_enabled:
        logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
        logging.getLogger("urllib3").setLevel(logging.WARNING)
    print("Arbitrage Monitor starting...", flush=True)

    source = CCXTAdapter(config["exchanges"])
    if debug_enabled:
        source.set_debug(True)
    source.connect()
    Web_STATE["exchanges"] = config["exchanges"]

    print(f"Connected to {len(config['exchanges'])} exchanges", flush=True)

    symbols = config.get("symbols", [])

    ws_manager = None

    class TerminalOutput:
        def update(self, opportunities, portfolio):
            WEB_STATE["opportunities"] = opportunities
            WEB_STATE["portfolio"] = {
                "balance": portfolio.total_value_usd,
                "trades": portfolio.total_trades,
                "wins": portfolio.wins,
                "losses": portfolio.losses
            }
            clear_screen()
            format_opportunities(opportunities, config.get("terminal", {}).get("max_rows", 10))
            if opportunities:
                WEB_STATE["ai_advice"] = generate_ai_advice(opportunities, config)
            format_portfolio(portfolio)
            for opp in opportunities:
                if opp.profit_pct >= config.get("min_profit_pct", 0.05):
                    db.save_opportunity(opp)
            db.save_portfolio(portfolio)

    config["symbols"] = symbols
    config["debug"] = debug_enabled

    engine = Engine(config, source, [TerminalOutput()], ws_manager=ws_manager)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print(f"Monitoring {len(symbols)} symbols", flush=True)
    print(f"Dashboard: http://localhost:5000", flush=True)
    print(f"Poll interval: {config['poll_interval']}s", flush=True)
    print(f"Min profit: {config['min_profit_pct']}%", flush=True)
    print("\nPress Ctrl+C to stop\n", flush=True)

    try:
        engine.run()
    finally:
        if ws_manager:
            ws_manager.stop()
        db.close()
        source.close()


if __name__ == "__main__":
    main()
