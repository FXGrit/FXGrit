from datetime import datetime
import json
import os
import requests

# === CONFIGURATION ===
lot_sizes = {
    "NIFTY": 50,
    "BANKNIFTY": 15,
    "RELIANCE": 250
}
overtrade_limit = 4
telegram_token = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
vip_chat_id = "-1002416993114"

# === TRADE INPUT ===
asset = "NIFTY"
strike = "23700"
opt_type = "CALL"
premium = 142.25
delta = 0.56
gamma = 0.017
theta = -4.23
strategy = "GammaBlast"

# === DATE & PATH SETUP ===
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
date_tag = now.strftime("%Y-%m-%d")
log_dir = "/storage/emulated/0/FXGRIT/Logs/Executed"
os.makedirs(log_dir, exist_ok=True)
log_path = f"{log_dir}/executed_trades.json"

# === READ TRADE LOG ===
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        data = json.load(f)
else:
    data = {}

if date_tag not in data:
    data[date_tag] = []

# === OVERTRADING CHECK ===
today_trades = [t for t in data[date_tag] if t["asset"] == asset]
if len(today_trades) >= overtrade_limit:
    print(f"❌ Overtrading Blocked for {asset} (Limit {overtrade_limit} per day)")
    print(f"⚠️ Trade Blocked for {asset}")
else:
    # === LOG TRADE ===
    trade = {
        "asset": asset,
        "strike": strike,
        "type": opt_type,
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "premium": premium,
        "strategy": strategy,
        "time": timestamp
    }
    data[date_tag].append(trade)
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

    # === TELEGRAM MESSAGE ===
    msg = f"""✅ Entry Confirmed: {asset} {strike} {opt_type}
📊 Delta: {delta} | Gamma: {gamma} | Theta: {theta}
💰 Premium: ₹{premium}
📈 Strategy: {strategy}
🕒 Time: {timestamp}"""

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": vip_chat_id,
        "text": msg
    }
    r = requests.post(url, data=payload)

    print("✅ Entry confirmed for", asset, strike, opt_type)
    print("🚀 Trade Executed (Logged & Sent)")
    print("✅ Telegram message sent to VIP channel.")