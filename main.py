import os
import yaml
import logging
import threading
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, send_from_directory
from core.engine import Engine
from core.symbol_discovery import SymbolDiscovery
from plugins.cex.ccxt_adapter import CCXTAdapter
from plugins.websocket.ws_manager import WebSocketManager
from output.terminal import format_opportunities, format_portfolio, clear_screen
from output.database import Database
from core.ai_advice import generate_ai_advice


WEB_STATE = {
    "portfolio": {"balance": 10000, "trades": 0, "wins": 0, "losses": 0, "win_rate": "N/A", "total_pnl": 0},
    "opportunities": [],
    "exchanges": [],
    "ai_advice": None
}

web_lock = threading.Lock()
WEB_STATE = {
    "portfolio": {"balance": 10000, "trades": 0, "wins": 0, "losses": 0, "win_rate": "N/A", "total_pnl": 0},
    "opportunities": [],
    "exchanges": [],
    "ai_advice": None
}
_last_opportunities = []
_last_update_time = 0

app = Flask(__name__, template_folder="templates")


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_portfolio_from_db(db: Database) -> dict:
    try:
        cursor = db.conn.execute(
            "SELECT total_value_usd, total_trades, wins, losses, total_pnl FROM portfolio_snapshots ORDER BY id DESC LIMIT 1"
        )
        row = cursor.fetchone()
        if row:
            total_value_usd, total_trades, wins, losses, total_pnl = row
            win_rate = f"{wins / total_trades * 100:.0f}%" if total_trades > 0 else "N/A"
            return {
                "balance": total_value_usd or 10000,
                "trades": total_trades,
                "wins": wins,
                "losses": losses,
                "win_rate": win_rate,
                "total_pnl": total_pnl
            }
    except Exception:
        pass
    return {"balance": 10000, "trades": 0, "wins": 0, "losses": 0, "win_rate": "N/A", "total_pnl": 0}


@app.route("/")
def index():
    return send_from_directory("templates", "dashboard.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


@app.route("/api/status")
def api_status():
    import time
    global _last_opportunities, _last_update_time
    try:
        with web_lock:
            # Use cached opportunities for up to 5 seconds
            if time.time() - _last_update_time > 5:
                opps = _last_opportunities
            else:
                opps = WEB_STATE["opportunities"]
            data = {
                "portfolio": WEB_STATE["portfolio"],
                "opportunities": [
                    {
                        "path": o.path[0] if isinstance(o.path, list) else o.path,
                        "exchanges": o.exchanges[0] if isinstance(o.exchanges, list) else o.exchanges,
                        "profit": o.profit_pct,
                        "volume": o.volume,
                        "type": o.arb_type.value
                    }
                    for o in opps
                ],
                "exchanges": WEB_STATE["exchanges"],
                "ai_advice": WEB_STATE["ai_advice"]
            }
            return data
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/pnl-history")
def api_pnl_history():
    global db
    try:
        cursor = db.conn.execute(
            "SELECT timestamp, total_pnl FROM portfolio_snapshots ORDER BY id DESC LIMIT 20"
        )
        rows = cursor.fetchall()
        return {"pnl": [{"timestamp": r[0], "value": r[1]} for r in reversed(rows)]}
    except Exception:
        return {"pnl": []}


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

    global WEB_STATE
    WEB_STATE["exchanges"] = config["exchanges"]

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

    saved_portfolio = load_portfolio_from_db(db)
    WEB_STATE["portfolio"] = saved_portfolio

    class TerminalOutput:
        def update(self, opportunities, portfolio):
            import time
            global _last_opportunities, _last_update_time
            with web_lock:
                WEB_STATE["opportunities"] = opportunities
                _last_opportunities = opportunities
                _last_update_time = time.time()
                WEB_STATE["portfolio"] = {
                    "balance": portfolio.total_value_usd,
                    "trades": portfolio.total_trades,
                    "wins": portfolio.wins,
                    "losses": portfolio.losses,
                    "win_rate": f"{portfolio.wins / portfolio.total_trades * 100:.0f}%" if portfolio.total_trades > 0 else "N/A",
                    "total_pnl": portfolio.total_pnl
                }
                if opportunities:
                    WEB_STATE["ai_advice"] = generate_ai_advice(opportunities, config)
            clear_screen()
            format_opportunities(opportunities, config.get("terminal", {}).get("max_rows", 10))
            format_portfolio(portfolio)
            for opp in opportunities:
                if opp.profit_pct >= config.get("min_profit_pct", 0.05):
                    db.save_opportunity(opp)
            db.save_portfolio(portfolio)

    config["symbols"] = symbols

    engine = Engine(config, source, [TerminalOutput()], ws_manager=ws_manager)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print(f"Monitoring {len(symbols)} symbols", flush=True)
    print(f"Dashboard: http://localhost:5000", flush=True)
    print(f"Poll interval: {config['poll_interval']}s", flush=True)
    print(f"Min profit: {config['min_profit_pct']}%", flush=True)
    if ws_manager:
        print("WebSocket: enabled", flush=True)
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