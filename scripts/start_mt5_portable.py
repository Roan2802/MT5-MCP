"""start_mt5_portable.py — Hermes cronscript

Zorgt ervoor dat de MT5 IC Markets Global portable terminal draait en
ingelogd is. Veilig headless: zonder interactieve desktop kan MT5 GUI niet
worden gestart, maar wanneer MT5 *al* draait (user opende hem via
START-MT5-IC-MARKETS.bat) dan koppelen we via de MT5-MCP initialize() tool en
loggen we eventueel automatisch in via _auto_login_if_needed().

De MT5 terminal MOET één keer per sessie handmatig worden opgestart via:
    C:\AI\MT5_ICMarkets_Global\START-MT5-IC-MARKETS.bat
na welke accounts.dat de login persistent maakt. Deze cron zorgt alleen
dat de status gemonitord + gerapporteerd wordt, en MT5 herstart wordt
als die vastloopt (niet via headless GUI, maar via Task Scheduler entry
die de user moet importeren — zie START-MT5-IC-MARKETS.bat footer).
"""
import os, subprocess, sys, time
from pathlib import Path

MT5_EXE   = Path(r"C:\AI\MT5_ICMarkets_Global\terminal64.exe")
MT5_DIR   = Path(r"C:\AI\MT5_ICMarkets_Global")
PORTABLE  = "/portable"

def mt5_running() -> list[int]:
    out = subprocess.run(
        ["cmd.exe", "/c", "tasklist /FI \"imagename eq terminal64.exe\" /FO CSV"],
        capture_output=True, text=True
    ).stdout
    pids = []
    for line in out.splitlines()[1:]:
        pid = line.split(',')[-2].strip('"') if ',' in line else ""
        if pid.isdigit():
            pids.append(int(pid))
    return pids

def start_mt5():
    # CREATE_NEW_CONSOLE detaches into the user desktop session.
    subprocess.Popen(
        [str(MT5_EXE), PORTABLE, "/config", str(MT5_DIR / "Config/terminal.ini")],
        cwd=str(MT5_DIR),
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )

def main():
    pids = mt5_running()
    report = {"running": bool(pids), "pids": pids}
    if not pids:
        try:
            start_mt5()
            time.sleep(8)
            report["attempted_start"] = True
            report["running_after"] = bool(mt5_running())
        except Exception as e:
            report["start_error"] = str(e)
    print("MT5 status:", report)
    # Silent (no deliver) when nothing to report per watchdog pattern.

if __name__ == "__main__":
    main()
