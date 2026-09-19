"""Direct MCP stdio client test: get_terminal_info + list_strategies.

This mimics what the other Hermes chat session (Cursor IDE) does:
calls the MCP server's get_terminal_info tool, which FAILED there.
We debug here whether it's a tool-implementation bug or an env issue.
"""
import asyncio, json, os, sys

# Strip inherited PYTHONPATH (Hermes venv → pydantic_core conflict)
if "PYTHONPATH" in os.environ:
    del os.environ["PYTHONPATH"]

sys.path.insert(0, r"C:\AI\MT5_MCP\MT5-MCP-main\src")

# Import the tool function directly (bypass FastMCP call_tool wrapper)
from mcp_mt5.main import _get_mt5_paths

def parse_result(r):
    """Extract text from FastMCP result."""
    txt = r.text if hasattr(r, "text") else str(r)
    if "content=[TextContent" in txt:
        import re
        m = re.search(r"text='([^']*)'", txt, re.DOTALL)
        txt = m.group(1) if m else txt
    txt = txt.replace("\\'", "'").replace("\\\\", "\\")
    try:
        return json.loads(txt)
    except Exception:
        return {"raw": txt[:400]}

async def main():
    paths = _get_mt5_paths()
    print("=== PATHS (verify portable resolution) ===")
    print("terminal:", paths["terminal"])
    print("data_folder:", paths["data_folder"])
    print("config_folder:", paths["config_folder"])

    # Test get_terminal_info directly — this is what FAILED in the other chat
    print("\n=== get_terminal_info (direct call) ===")
    try:
        from mcp_mt5.main import get_terminal_info, initialize, list_strategies
        r = get_terminal_info()
        print("get_terminal_info result:", r)
    except Exception as e:
        print("get_terminal_info EXCEPTION:", f"{type(e).__name__}: {str(e)[:300]}")

    # list_strategies (filesystem-based, does NOT need MT5 IPC)
    print("\n=== list_strategies (no MT5 IPC needed) ===")
    try:
        r = list_strategies()
        n = len(r["strategies"]) if isinstance(r, dict) and isinstance(r.get("strategies"), list) else r
        print("list_strategies:", n, "items")
    except Exception as e:
        print("list_strategies EXCEPTION:", f"{type(e).__name__}: {str(e)[:300]}")

asyncio.run(main())
