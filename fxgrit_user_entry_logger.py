import json
import os
from datetime import datetime
import requests

# --- Configurations ---
VIP_CHAT_ID = "-1002416993114"
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
LOG_BASE_DIR = "/storage/emulated/0/FXGRIT/Logs/Users"  # Each user log here

# --- Entry Log Function ---
def log_user_entry(user_id, asset, strike, opt_type, delta, gamma, theta, premium, strategy):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_tag = now.strftime("%Y-%m-%d")

        user_dir = f"{LOG_BASE_DIR}/{user_id}"
        os.makedirs(user_dir, exist_ok=True)
        log_path = f"{user_dir}/entries.json"

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

        # --- Telegram Message ---
        msg = f"""✅ Entry Confirmed: {asset} {strike} {opt_type}
📊 Delta: {delta} | Gamma: {gamma} | Theta: {theta}
💰 Premium: ₹{premium}
📈 Strategy: {strategy}
🕒 Time: {timestamp}"""

        send_to_telegram(msg)
        print("✅ Log & Telegram sent successfully")

    except Exception as e:
        print(f"❌ Log Failed: {e}")

# --- Send Message to Telegram ---
def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": VIP_CHAT_ID,
            "text": message
        }
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            print("✅ Message sent to Telegram")
        else:
            print("❌ Telegram error:", r.text)
    except Exception as e:
        print("❌ Telegram send error:", e)

# --- Run Dummy Trade Entry (example) ---
log_user_entry(
    user_id="user123",  # dynamic user ID
    asset="NIFTY",
    strike="23700",
    opt_type="CALL",
    delta=0.56,
    gamma=0.017,
    theta=-4.23,
    premium=142.25,
    strategy="GammaBlast"
)