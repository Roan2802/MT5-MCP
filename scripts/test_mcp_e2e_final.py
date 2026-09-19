import os, sys
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
from mcp_mt5.main import mcp

def parse(r):
    """Parse FastMCP TextContent wrapper."""
    txt = r.text if hasattr(r, "text") else str(r)
    if "content=[TextContent" in txt:
        import re
        m = re.search(r"text='((?:[^'\\]|\\')*)'", txt, re.DOTALL)
        txt = m.group(1).replace("\\'", "'") if m else txt
    try:
        import json
        return json.loads(txt)
    except Exception:
        return {"raw": txt[:300]}

async def run(name, **params):
    try:
        r = await mcp.call_tool(name, arguments=params)
        return parse(r)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {str(e)[:200]}"}

async def main():
    print("=== initialize ===")
    i = await run("initialize")
    print("init:", i)
    print("=== get_terminal_info ===")
    t = await run("get_terminal_info")
    print("terminal:", t.get("name") if isinstance(t, dict) else t, "build:", t.get("build") if isinstance(t, dict) else "")
    print("=== get_account_info ===")
    a = await run("get_account_info")
    if "login" in a:
        print("login:", a.get("login"), "server:", a.get("server"), "balance:", a.get("balance"), "trade_allowed:", a.get("trade_allowed"))
    else:
        print(a)
    print("=== list_strategies ===")
    s = await run("list_strategies")
    n = len(s["strategies"]) if isinstance(s.get("strategies", None), list) else s
    print("strategies:", n)
    print("=== compile_mql5 ===")
    c = await run("compile_mql5", **{"filepath": r"C:\AI\MT5_ICMarkets_Global\MQL5\Experts\Examples\Moving Average\Moving Average.mq5"})
    print("compile success:", c.get("success"), "ex5_exists:", c.get("ex5_exists"))
    print("=== shutdown ===")
    print(await run("shutdown"))

import asyncio
asyncio.run(main())
