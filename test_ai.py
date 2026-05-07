import yaml
from dotenv import load_dotenv
load_dotenv()

from core.engine import Engine
from plugins.cex.ccxt_adapter import CCXTAdapter

with open("config.yaml") as f:
    config = yaml.safe_load(f)

source = CCXTAdapter(config["exchanges"])
source.connect()

engine = Engine(config, source, [])
engine.run_once()

print("=== Done ===")