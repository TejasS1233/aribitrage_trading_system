import yaml
from dotenv import load_dotenv
load_dotenv()

from core.engine import Engine
from plugins.cex.ccxt_adapter import CCXTAdapter
from output.terminal import format_opportunities, format_portfolio
from core.ai_advice import generate_ai_advice

with open("config.yaml") as f:
    config = yaml.safe_load(f)

source = CCXTAdapter(config["exchanges"])
source.connect()

class TestOutput:
    def update(self, opportunities, portfolio):
        print("\n" + "=" * 60)
        print(" LIVE ARBITRAGE SCAN ")
        print("=" * 60)
        format_opportunities(opportunities, 10)
        print("\n[AI] Generating advice...")
        ai_result = generate_ai_advice(opportunities, config)
        print("AI Result:", ai_result)
        format_portfolio(portfolio)

config["debug"] = True
engine = Engine(config, source, [TestOutput()])
engine.run_once()
print("\nDone!")