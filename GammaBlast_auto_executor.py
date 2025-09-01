import json
import time
import os

print("🔁 GammaBlast Auto Executor Started...")

data_path = "/storage/emulated/0/FXGRIT/Data/options_greeks_all.json"

def load_options_data():
    if not os.path.exists(data_path):
        print("❌ File not found:", data_path)
        return []
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Error loading data:", e)
        return []

while True:
    try:
        options = load_options_data()
        for option in options:
            try:
                delta = float(option.get("Delta", 0))
                gamma = float(option.get("Gamma", 0))
                theta = float(option.get("Theta", 0))
                asset = option.get("Asset", "UNKNOWN")
                strike = option.get("StrikePrice", "NA")
                option_type = str(option.get("OptionType", "UNKNOWN")).upper()

                # 🔍 GammaBlast Logic – adjust as needed
                if abs(delta) >= 0.5 and gamma >= 0.015 and theta < 0:
                    print(f"🚀 Executing GammaBlast trade for {asset} {strike} {option_type}")
                    print(f"🔹 Delta: {delta} | Gamma: {gamma} | Theta: {theta}")
                else:
                    print(f"⏭️ Skipped: {asset} – No match")
            except Exception as inner_err:
                print("❌ Option error:", inner_err)
    except Exception as e:
        print("❌ Main error:", e)

    time.sleep(5)