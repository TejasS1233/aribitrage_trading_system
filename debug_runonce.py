import yaml
from core.config_loader import load_config
from core.engine import Engine
from plugins.cex.ccxt_adapter import CCXTAdapter

config = load_config()
adapter = CCXTAdapter(config['exchanges'])
adapter.connect()
adapter.set_debug(True)
engine = Engine(config, adapter, [], debug=True)
engine.run_once()