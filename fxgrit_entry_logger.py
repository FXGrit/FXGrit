from datetime import datetime
import json
import os
import requests

# 🔐 Telegram Configuration
TELEGRAM_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
VIP_CHANNEL_ID = "-1002416993114"

def send_telegram_entry(asset, strike, opt_type, delta, gamma, theta, premium, strategy):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""✅ Entry Confirmed: {asset} {strike} {opt_type}
📊 Delta: {delta} | Gamma: {gamma} | Theta: {theta}
💰 Premium: ₹{premium}
📈 Strategy: {strategy}
🕒 Time: {now}"""

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": VIP_CHANNEL_ID,
            "text": message
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram message sent to VIP channel.")
        else:
            print(f"❌ Telegram error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram sending failed: {e}")

def log_entry_trade(asset, strike, opt_type, delta, gamma, theta, premium, strategy):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_tag = now.strftime("%Y-%m-%d")

        log_dir = "/storage/emulated/0/FXGRIT/Logs/Executed"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "executed_trades.json")

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

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

        if date_tag not in data:
            data[date_tag] = []

        data[date_tag].append(trade)

        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Entry confirmed for {asset} {strike} {opt_type}")
        print("🚀 Trade Executed (Logged & Sent)")

        # 🚀 Send to Telegram
        send_telegram_entry(asset, strike, opt_type, delta, gamma, theta, premium, strategy)

    except Exception as e:
        print(f"❌ Error: {e}")

# 🔃 Dummy Test
log_entry_trade(
    asset="NIFTY",
    strike="23700",
    opt_type="CALL",
    delta=0.56,
    gamma=0.017,
    theta=-4.23,
    premium=142.25,
    strategy="GammaBlast"
)