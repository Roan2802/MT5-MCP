#!/usr/bin/env python3
"""sync_env_creds.py

Synchroniseert MT5 credentials vanaf Config/mt5-creds.json → .env
zodat de MT5-MCP `login()` tool (via _auto_login_if_needed) de juiste
inloggegevens heeft.  Voer dit uit VÓÓR je 'hermes mcp test mt5' of
MT5 via de MCP aanroept.

Usage:
    python sync_env_creds.py            # sync + dry-run report
    python sync_env_creds.py --apply    # also rewrite the .env file
"""
import json, re, sys
from pathlib import Path

ROOT   = Path(r"C:\AI\MT5_MCP\MT5-MCP-main")
ENV    = ROOT / ".env"
CREDS  = Path(r"C:\AI\MT5_ICMarkets_Global\Config\mt5-creds.json")

creds: dict = {}
if CREDS.exists():
    try:
        creds = json.loads(CREDS.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARN: could not parse {CREDS}: {e}")

mapping = {
    "MT5_LOGIN":    creds.get("MT5_LOGIN", ""),
    "MT5_PASSWORD": creds.get("MT5_PASSWORD", ""),
    "MT5_SERVER":   creds.get("MT5_SERVER", ""),
}

lines = ENV.read_text(encoding="utf-8").splitlines()
changed = {k: False for k in mapping}
new_lines = []
for ln in lines:
    m = re.match(r"^([A-Z0-9_]+)=(.*)$", ln)
    if m and m.group(1) in mapping:
        new_val = mapping[m.group(1)]
        new_lines.append(f"{m.group(1)}={new_val}")
        changed[m.group(1)] = new_val
    else:
        new_lines.append(ln)

print("=== Credentials that would be synced into .env ===")
for k, v in mapping.items():
    masked = v if k != "MT5_PASSWORD" else ("*" * len(v)) if v else "<leeg>"
    print(f"  {k:14} = {masked}")

apply = "--apply" in sys.argv
if apply:
    ENV.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print("--- .env updated ---")
else:
    print("--- (dry-run; pass --apply to write) ---")

missing = [k for k, v in mapping.items() if not v]
if missing:
    print(f"WARN: these are still empty — vul ze in {CREDS}: {missing}")
    sys.exit(2)
