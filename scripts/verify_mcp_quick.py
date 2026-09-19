import os, sys, json
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")

import MetaTrader5 as mt5
from mcp_mt5.main import _get_mt5_paths, compile_mql5, list_strategies

paths = _get_mt5_paths()
r = mt5.initialize(path=paths["terminal"])
print("1. initialize:", r, mt5.last_error() if not r else "")
if r:
    ai = mt5.account_info()
    print("2. account_info:", "login=%s server=%s balance=%s trade_allowed=%s" % (ai.login, ai.server, ai.balance, ai.trade_allowed))

# list_strategies (filesystem-based, no mt5 IPC needed)
strs = list_strategies()
print("3. list_strategies:", len(strs) if isinstance(strs, list) else strs)

# compile_mql5
mq5 = r"C:\AI\MT5_ICMarkets_Global\MQL5\Experts\Examples\Moving Average\Moving Average.mq5"
c = compile_mql5(filepath=mq5)
print("4. compile_mql5:", c.get("success") if isinstance(c, dict) else c)
mt5.shutdown()
print("5. shutdown: done")
