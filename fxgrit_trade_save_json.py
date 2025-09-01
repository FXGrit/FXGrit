import json
from datetime import datetime

# 📌 Signal Details — बस यहां अपना डेटा डालें
signal_data = {
    "Signal": "SELL",  # or "BUY"
    "Asset": "BTCUSD",
    "Entry": 67215.50,
    "SL": 67275.50,
    "TP1": 67015.50,
    "TP2": 66815.50
}

# 📁 File path — जहां फाइल सेव करनी है
file_path = "/storage/emulated/0/FXGRIT/Trades/trade_execute.json"

try:
    # JSON फाइल सेव करें
    with open(file_path, "w") as f:
        json.dump(signal_data, f, indent=4)
    print(f"✅ Signal saved successfully at:\n{file_path}")
except Exception as e:
    print(f"❌ Error saving JSON file:\n{e}")