# MT5 Trading — IC Markets Global (Codex Skill)

> **Prerequisite:** MT5 portable draait (`C:\AI\MT5_ICMarkets_Global\START-MT5-IC-MARKETS.bat`)  
> en de MT5-MCP is geconfigureerd in `~/.codex/config.toml` onder `[mcp_servers.mt5]`.

## Wat deze skill geeft
30 MCP-tools voor MetaTrader 5, beschikbaar in Codex CLI via de `mt5` MCP server:

| Tool | Doel |
|------|------|
| `initialize` | Verbind met de MT5 terminal (path = portable terminal64.exe) |
| `get_account_info` | Inloggegevens, saldo, margin, leverage |
| `get_symbols` / `get_symbol_info` / `symbol_select` | Instruments / marktwerking |
| `copy_ticks_*` / `copy_rates_*` | Tick- en OHLC-data via `metatrader5` package |
| `order_send` / `order_check` | Orders plaatsen |
| `positions_get` / `orders_get` / `history_deals_get` | Posities / historie |
| `compile_mql5` | MQ5 → EX5 compileren |
| `run_strategy_tester` / `read_test_report` | Backtest draaien + rapport lezen |
| `list_strategies` | EA-bestanden oploceren |

## Veelgebruikte patronen

### 0. Terminal starten (één keer)
```bat
C:\AI\MT5_ICMarkets_Global\START-MT5-IC-MARKETS.bat
```
Deze batch start MT5 in **portable** mode (`/portable`). Alle account/credential data blijft persistent in
`C:\AI\MT5_ICMarkets_Global\Config\accounts.dat` + `terminal.lic` — geen herhaalde inlog meer.

### 1. Verbinden + account check
```
initialize(path="C:\AI\MT5_ICMarkets_Global\terminal64.exe")
get_account_info()
get_symbols()
```

### 2. Symbol selecteren + tickdata halen
```
symbol_select("EURUSD", True)
copy_ticks_from_pos("EURUSD", 0, 1000)
```

### 3. Order plaatsen (demo)
```
order_send({
  "action": mt5.TRADE_ACTION_DEAL,
  "symbol": "EURUSD",
  "volume": 0.01,
  "type": mt5.ORDER_TYPE_BUY,
  "price": 0,
  "deviation": 10,
  "magic": 123456,
  "comment": "codex",
  "type_time": mt5.ORDER_TIME_GTC,
  "type_filling": mt5.ORDER_FILLING_RETURN,
})
```

### 4. Strategie testen
```
run_strategy_tester(
  expert="MyStrategy",
  symbol="EURUSD",
  period="H1",
  deposit=10000,
  currency="USD",
  from_date="2024-01-01",
  to_date="2024-06-01",
  opt_mode=mt5.TESTER_OPTIMIZATION_MODE_SEQUENTIAL,  # or _GENETIC
)
read_test_report()
```

## Troubleshooting
- **login vergeten** → controleer `accounts.dat` mtime in `Config\`. Sluit MT5 *altijd* via File→Exit (niet taskkill).
- **grijs flitsend scherm** → `[Window] IsFlat=0` in `Config\terminal.ini`.
- **mt5.initialize faalt** → CTOR `MetaTrader5`-package draagt de terminal op; sluit alle andere MT5-instanties eerst.
