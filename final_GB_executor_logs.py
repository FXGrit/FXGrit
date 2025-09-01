import json
import time
import os
from datetime import datetime

DATA_FILE = "/storage/emulated/0/FXGRIT/Data/options_greeks_all.json"
LOG_FILE = "/storage/emulated/0/FXGRIT/Logs/gammablast_trades.json"
PNL_FILE = "/storage/emulated/0/FXGRIT/Logs/profit_master.json"
TELEGRAM_FREE = "/storage/emulated/0/FXGRIT/Telegram/free.txt"
TELEGRAM_VIP = "/storage/emulated/0/FXGRIT/Telegram/vip.txt"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_log(entry):
    log = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                log = json.load(f)
            except:
                log = []
    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def save_profit(entry):
    profit_log = []
    if os.path.exists(PNL_FILE):
        with open(PNL_FILE, "r") as f:
            try:
                profit_log = json.load(f)
            except:
                profit_log = []
    profit_log.append(entry)
    with open(PNL_FILE, "w") as f:
        json.dump(profit_log, f, indent=2)

def send_telegram(message):
    with open(TELEGRAM_FREE, "a") as f:
        f.write(message + "\n")
    with open(TELEGRAM_VIP, "a") as f:
        f.write(message + "\n")

print("🔁 GammaBlast Auto Executor Started...")

while True:
    data = load_data()
    for item in data:
        try:
            asset = item["Asset"]
            strike = item["Strike"]
            delta = item["Delta"]
            gamma = item["Gamma"]
            theta = item["Theta"]

            option_type = "CALL" if delta > 0 else "PUT"

            # Example condition for GammaBlast trigger
            if abs(delta) > 0.5 and gamma > 0.015 and theta < -3:
                print(f"🚀 Executing GammaBlast trade for {asset} {strike} {option_type}")
                print(f"🔹 Delta: {delta} | Gamma: {gamma} | Theta: {theta}")

                # Save log
                trade_entry = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "asset": asset,
                    "strike": strike,
                    "option": option_type,
                    "delta": delta,
                    "gamma": gamma,
                    "theta": theta,
                    "strategy": "GammaBlast"
                }
                save_log(trade_entry)

                # Simulated Profit (You can later update with real P&L)
                profit = round(abs(delta * 100), 2)
                profit_entry = {
                    "time": trade_entry["time"],
                    "asset": asset,
                    "strategy": "GammaBlast",
                    "profit": profit
                }
                save_profit(profit_entry)

                # Telegram Alerts
                msg = f"🚀 GammaBlast Signal:\n📌 {asset} {strike} {option_type}\n📊 Δ: {delta} | Γ: {gamma} | Θ: {theta}\n💰 Est. Profit: ₹{profit}"
                send_telegram(msg)

        except Exception as e:
            print(f"❌ Error: {e}")
    
    time.sleep(5)