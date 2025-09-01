import os
import json
import pandas as pd
from datetime import datetime

trade_path = "/storage/emulated/0/FXGRIT/Trades/trade_execute.json"
log_path = "/storage/emulated/0/FXGRIT/Logs/user_trade_log.xlsx"

def log_trade():
    if not os.path.exists(trade_path):
        print("⚠️ No trade to log.")
        return

    with open(trade_path) as f:
        signal = json.load(f)

    entry = float(signal["Entry"])
    sl = float(signal["SL"])
    tp1 = float(signal["TP1"])
    tp2 = float(signal["TP2"])
    signal_type = signal["Signal"]
    asset = signal["Asset"]
    lot = float(signal.get("Lot", 0.01))

    # Basic P&L Calculation (mocked)
    if signal_type == "BUY":
        pnl = (tp1 - entry) * 100000 * lot
    else:
        pnl = (entry - tp1) * 100000 * lot

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    row = {
        "Date/Time": now,
        "Asset": asset,
        "Signal": signal_type,
        "Entry": entry,
        "SL": sl,
        "TP1": tp1,
        "TP2": tp2,
        "Lot": lot,
        "P&L": round(pnl, 2)
    }

    # Load or create log
    if os.path.exists(log_path):
        df = pd.read_excel(log_path)
        df = df.append(row, ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(log_path, index=False)
    print("✅ Trade logged with P&L.")