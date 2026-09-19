import sys, asyncio, json
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
from mcp_mt5.main import mcp

async def run(name, **params):
    try:
        r = await mcp.call_tool(name, arguments=params)
        return r.text if hasattr(r, "text") else str(r)
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {str(e)[:200]}"

async def main():
    print("=== initialize (portable) ===")
    print((await run("initialize", path=r"C:\AI\MT5_ICMarkets_Global\terminal64.exe"))[:200])

    print("=== get_account_info ===")
    a = await run("get_account_info")
    try:
        d = json.loads(a)
        print("login:", d.get("login"), "server:", d.get("server"), "balance:", d.get("balance"), "equity:", d.get("equity"))
    except Exception:
        print(a[:300])

    print("=== list_strategies ===")
    s = await run("list_strategies")
    print("EA count:", s.count('"name"'), "—", s[:100])

    print("=== compile_mql5 (Moving Average.mq5) ===")
    c = await run("compile_mql5", filepath=r"C:\AI\MT5_ICMarkets_Global\MQL5\Experts\Examples\Moving Average\Moving Average.mq5")
    print(c[:250])

    print("=== shutdown ===")
    print((await run("shutdown"))[:100])

asyncio.run(main())
