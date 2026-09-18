import sys, asyncio
sys.path.insert(0, 'src')
from mcp_mt5.main import mcp, _get_mt5_paths

paths = _get_mt5_paths()
print("terminal   :", paths["terminal"])
print("data_folder:", paths["data_folder"])
print("config_folder:", paths["config_folder"])

# Validate paths match our .env (NOT the hardcoded AppData hash fallback)
norm_data = paths["data_folder"].replace("\\", "/")
norm_term = paths["terminal"].replace("\\", "/")
assert "MT5_ICMarkets_Global" in norm_data, "FAIL: still using old AppData hash!"
assert "MT5_ICMarkets_Global" in norm_term, "FAIL: terminal path wrong!"
print("PASS: .env paths loaded correctly (portable)")

# Validate all tools registered
async def names():
    return [t.name async for t in mcp.get_tools()]
names_list = asyncio.run(names())
print("Tools registered:", len(names_list))
assert "list_strategies" in names_list, "FAIL: list_strategies missing"
assert "initialize" in names_list, "FAIL: initialize missing"
assert "order_send" in names_list, "FAIL: order_send missing"
assert "compile_mql5" in names_list, "FAIL: compile_mql5 missing"
print("PASS: tools registered incl. initialize + list_strategies + order_send + compile_mql5")
