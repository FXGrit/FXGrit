import json
import time
import random
import os

signal_file_path = "/storage/emulated/0/FXGRIT/Signals/latest_signal.json"

assets = ["BTCUSD", "GOLD", "EURUSD", "GBPUSD"]
directions = ["BUY", "SELL"]

def generate_signal():
    signal_id = f"signal_{int(time.time())}"
    asset = random.choice(assets)
    signal = random.choice(directions)
    entry = round(random.uniform(1000, 70000), 2)
    sl = round(entry + random.uniform(30, 60), 2) if signal == "BUY" else round(entry - random.uniform(30, 60), 2)
    tp1 = round(entry + random.uniform(80, 120), 2) if signal == "BUY" else round(entry - random.uniform(80, 120), 2)
    tp2 = round(tp1 + 100, 2) if signal == "BUY" else round(tp1 - 100, 2)

    data = {
        "id": signal_id,
        "asset": asset,
        "signal": signal,
        "entry": entry,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2
    }

    with open(signal_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"✅ New signal generated: {asset} ({signal})")

# 🔁 Keep generating every 30 seconds
print("📡 FXGRIT Auto Signal Generator Started...\n")
while True:
    generate_signal()
    time.sleep(30)