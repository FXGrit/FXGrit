import os
import json
import pandas as pd
from datetime import datetime

# 📁 Path to log file
log_file = "/storage/emulated/0/FXGRIT/Logs/trade_history_master.xlsx"

# 📁 Make sure Logs folder exists
os.makedirs("/storage/emulated/0/FXGRIT/Logs", exist_ok=True)

# ✅ Load trade signal
def load_signal():
    path = "/storage/emulated/0/FXGRIT/Trades/trade_execute.json"
    if not os.path.exists(path):
        print("⚠️ No trade file found.")
        return None
    with open(path, "r") as f:
        return json.load(f)

# ✅ Append trade to Excel log
def save_trade_log(signal, profit_type):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "DateTime": now,
        "Asset": signal.get("Asset", ""),
        "Signal": signal.get("Signal", ""),
        "Entry": signal.get("Entry", ""),
        "SL": signal.get("SL", ""),
        "TP1": signal.get("TP1", ""),
        "TP2": signal.get("TP2", ""),
        "ProfitType": profit_type  # Regular, Compounding, GammaBlast
    }

    if os.path.exists(log_file):
        df = pd.read_excel(log_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_excel(log_file, index=False)
    print("✅ Trade logged successfully.")

# ✅ Run the logger
signal = load_signal()
if signal:
    # 🧠 Choose correct profit type here (custom logic can be added later)
    # For example, if "compound": save_trade_log(signal, "Compounding")
    save_trade_log(signal, "Regular")  # Change to "GammaBlast" / "Compounding" if needed