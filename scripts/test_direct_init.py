import os, sys
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
import MetaTrader5 as mt5
from mcp_mt5.main import _get_mt5_paths

# Reproduce the WORKING CLI test
p = _get_mt5_paths()
print("path:", p["terminal"], "exists:", os.path.exists(p["terminal"]))
print("data_folder:", p["data_folder"])

# Direct mt5.initialize (like the CLI test that worked)
r = mt5.initialize(path=p["terminal"])
print("mt5.initialize(path=terminal):", r, "err:", mt5.last_error() if not r else "ok")
if r:
    ti = mt5.terminal_info()
    print("terminal_info:", "name=%s build=%s" % (ti.name, ti.build) if ti else "None", "err:", mt5.last_error())
    ai = mt5.account_info()
    print("account_info:", "login=%s server=%s" % (ai.login, ai.server) if ai else "None", "err:", mt5.last_error())
mt5.shutdown()
print("shutdown done")
