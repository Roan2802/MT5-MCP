"""Standalone verification script for MT5-MCP — reproduces the E2E test.

Usage:
    cd C:\AI\MT5_MCP\MT5-MCP-main
    set PYTHONPATH=
    .venv\Scripts\python.exe scripts\verify_mcp_quick.py

Run AFTER starting the portable MT5 (START-MT5-IC-MARKETS.bat in desktop).
"""
import os, sys
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
from mcp_mt5.main import initialize, get_terminal_info, get_account_info, list_strategies, compile_mql5, shutdown

print("Prerequisites: MT5 portable running (START-MT5-IC-MARKETS.bat)")
print("1. initialize():", initialize())
ti = get_terminal_info()
print("2. get_terminal_info:", ti.get("name"), "build", ti.get("build"))
ai = get_account_info()
print("3. get_account_info: login=%s server=%s balance=%s trade_allowed=%s" % (
    ai.login, ai.server, ai.balance, ai.trade_allowed))
print("4. list_strategies: %d items" % len(list_strategies()))
c = compile_mql5(filepath=r"C:\AI\MT5_ICMarkets_Global\MQL5\Experts\Examples\Moving Average\Moving Average.mq5")
print("5. compile_mql5: success=%s ex5_exists=%s" % (c.get("success"), c.get("ex5_exists")))
print("6. shutdown():", shutdown())
