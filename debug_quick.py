import yaml
import logging
from core.engine import Engine
from plugins.cex.ccxt_adapter import CCXTAdapter

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("urllib3").setLevel(logging.WARNING)

with open("config.yaml") as f:
    config = yaml.safe_load(f)
config['debug'] = True

source = CCXTAdapter(config["exchanges"])
source.set_debug(True)
source.connect()

engine = Engine(config, source, [])
engine.run_once()

print("=== DONE ===")