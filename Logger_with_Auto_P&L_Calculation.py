import json
import os
import pandas as pd
from datetime import datetime

# Paths
signal_path = "/storage/emulated/0/FXGRIT/Trades/trade_execute.json"
log_path = "/storage/emulated/0/FXGRIT/Logs/fxgrit_trade_log.xlsx"

# Load signal
if not os.path.exists(signal_path):
    print("❌ No signal to log.")
    exit()

with open(signal_path, "r") as f:
    signal = json.load(f)

# Extract details
asset = signal['Asset']
signal_type = signal['Signal']
entry = float(signal['Entry'])
sl = float(signal['SL'])
tp1 = float(signal['TP1'])
tp2 = float(signal['TP2'])
time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

# Calculate P&L (theoretical)
if signal_type == "BUY":
    max_profit = tp2 - entry
    max_loss = entry - sl
else:  # SELL
    max_profit = entry - tp2
    max_loss = sl - entry

# Prepare row
row = {
    "Time": time_now,
    "Asset": asset,
    "Signal": signal_type,
    "Entry": entry,
    "SL": sl,
    "TP1": tp1,
    "TP2": tp2,
    "Max Profit": round(max_profit, 5),
    "Max Loss": round(max_loss, 5)
}

# Save to Excel
if os.path.exists(log_path):
    df_old = pd.read_excel(log_path)
    df_new = df_old.append(row, ignore_index=True)
else:
    df_new = pd.DataFrame([row])

df_new.to_excel(log_path, index=False)
print("✅ Trade logged with P&L.")