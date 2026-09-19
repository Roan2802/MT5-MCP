import os, sys
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
import MetaTrader5 as mt5
from mcp_mt5.main import _get_mt5_paths

# First: direct init (proven working)
p = _get_mt5_paths()
r = mt5.initialize(path=p["terminal"])
print("pre-init terminal_info:", mt5.terminal_info() is not None, "err:", mt5.last_error())
ai = mt5.account_info()
print("pre-init account_info:", "login=%s" % ai.login if ai else "None")
mt5.shutdown()
print("after shutdown terminal_info:", mt5.terminal_info() is not None)

# Now: simulate calling initialize() (our MCP wrapper) then get_terminal_info()
print("\n--- Now via MCP initialize() wrapper ---")
from mcp_mt5.main import initialize, get_terminal_info, _ensure_mt5_connected
init_result = initialize(path=p["terminal"])
print("MCP initialize() returned:", init_result)
print("ensure_connected check:", _ensure_mt5_connected())
try:
    ti = get_terminal_info()
    print("get_terminal_info:", ti.get("name"), ti.get("build"))
except Exception as e:
    print("get_terminal_info FAIL:", str(e)[:150])
mt5.shutdown()
