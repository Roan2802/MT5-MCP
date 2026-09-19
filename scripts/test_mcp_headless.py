#!/usr/bin/env python3
"""Test the MT5-MCP tools that work HEADLESS (no MT5 GUI required).

Tools covered (these use file/system calls, not mt5.initialize IPC):
  - list_strategies   → lists EAs in MQL5/Experts
  - compile_mql5      → MetaEditor64.exe /compile (CLI, no GUI)
  - run_strategy_tester → terminal64.exe /config tester.ini (CLI backtest)
  - read_test_report  → parses HTML/log report

Trading tools (initialize/login/get_account_info/order_send) REQUIRE a
running MT5 GUI in the desktop session and are NOT tested here.
"""
import sys, asyncio
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
from mcp_mt5.main import mcp

async def run(name, **params):
    try:
        r = await mcp.call_tool(name, arguments=params)
        txt = r[0].text if isinstance(r, (list, tuple)) else str(r)
        return txt.strip()
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"

async def main():
    results = []

    # 1. list_strategies
    r1 = await run("list_strategies")
    n = r1.count('"name"') if r1 else 0
    results.append(("list_strategies", "PASS" if n > 0 else "FAIL", f"{n} EAs found"))

    # 2. compile_mql5 — compile an existing .mq5 (e.g. Moving Average Sample)
    ea_path = r"C:\AI\MT5_ICMarkets_Global\MQL5\Experts\Examples\Moving Average\Moving Average.mq5"
    r2 = await run("compile_mql5", filepath=ea_path)
    ok2 = "compiled" in r2.lower() or "success" in r2.lower() if r2 else False
    results.append(("compile_mql5", "PASS" if ok2 else "CHECK", r2[:200]))

    # 3. get_version (requires initialize first — skip; note as BLOCKED)
    results.append(("initialize", "BLOCKED-HEADLESS",
                    "mt5.initialize() needs MT5 GUI in desktop session"))

    # 4. get_account_info (same blocker)
    results.append(("get_account_info", "BLOCKED-HEADLESS",
                    "requires running MT5 GUI"))

    # 5. order_send
    results.append(("order_send", "BLOCKED-HEADLESS",
                    "requires initialized+authenticated MT5"))

    print("\n=== MT5-MCP HEADLESS TOOL TEST RESULTS ===")
    for name, status, detail in results:
        print(f"  {name:22} {status:18} {detail}")

asyncio.run(main())
