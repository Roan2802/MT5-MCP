import os, sys
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
import MetaTrader5 as mt5
from mcp_mt5.main import _get_mt5_paths, initialize, get_terminal_info, get_account_info, list_strategies, compile_mql5, shutdown

p = _get_mt5_paths()
print("1. initialize():", initialize())               # no path arg → auto portable
ti = get_terminal_info()
print("2. get_terminal_info: name='%s' build=%s" % (ti.get("name"), ti.get("build")))
ai = get_account_info()
print("3. get_account_info: login=%s server=%s balance=%s trade_allowed=%s" % (ai.login, ai.server, ai.balance, ai.trade_allowed))
strs = list_strategies()
print("4. list_strategies: count=%d" % len(strs))
c = compile_mql5(filepath=r"C:\AI\MT5_ICMarkets_Global\MQL5\Experts\Examples\Moving Average\Moving Average.mq5")
print("5. compile_mql5: success=%s ex5_exists=%s" % (c.get("success"), c.get("ex5_exists")))
print("6. shutdown():", shutdown())
