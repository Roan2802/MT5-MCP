import sys, asyncio, json, os
sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")
from mcp_mt5.main import mcp, _get_mt5_paths

async def run(name, **params):
    try:
        r = await mcp.call_tool(name, arguments=params)
        txt = r.text if hasattr(r, "text") else str(r)
        try:
            d = json.loads(txt.replace("content=[TextContent(type='text', text='", "").replace("'}]", ""))
            return d
        except Exception:
            return {"raw": txt[:300]}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {str(e)[:200]}"}

async def main():
    print("=== _get_mt5_paths ===")
    p = _get_mt5_paths()
    print("terminal:", p["terminal"])
    print("data_folder:", p["data_folder"])
    print("config_folder:", p["config_folder"])

    # Check if MT5 terminal64.exe is running
    import subprocess
    ps = subprocess.run(["tasklist", "/FI", "IMAGENAME eq terminal64.exe"],
                        capture_output=True, text=True)
    running = "terminal64.exe" in ps.stdout
    print("MT5 running:", running)

    print("=== initialize (portable) ===")
    i = await run("initialize")
    print("init result:", i)

    if i.get("result") or i.get("success"):
        print("=== get_account_info ===")
        a = await run("get_account_info")
        print("acct_info:", a)
    print("=== list_strategies ===")
    s = await run("list_strategies")
    print("strategies count:", len(s) if isinstance(s, list) else s)

asyncio.run(main())
