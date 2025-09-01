from datetime import datetime
import json
import os
import requests

# MULTI USER: IDs mapped with usernames
USER_IDS = {
    "user_1": 6183259863  # Replace/add more users if needed
}

# Telegram Bot Token (for FXGRIT Bot)
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"

def log_entry(user, asset, strike, opt_type, delta, gamma, theta, premium, strategy):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_tag = now.strftime("%Y-%m-%d")

        base_dir = f"/storage/emulated/0/FXGRIT/Users/{user}/Logs/Executed"
        os.makedirs(base_dir, exist_ok=True)
        log_path = f"{base_dir}/executed_trades.json"

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

        # Telegram Message
        msg = (
            f"✅ Entry Confirmed: {asset} {strike} {opt_type}\n"
            f"📊 Delta: {delta} | Gamma: {gamma} | Theta: {theta}\n"
            f"💰 Premium: ₹{premium}\n"
            f"📈 Strategy: {strategy}\n"
            f"🕒 Time: {timestamp}"
        )

        send_telegram(USER_IDS[user], msg)

        print(f"✅ Entry logged & message sent for {user}")

    except Exception as e:
        print(f"❌ Error: {e}")

def send_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Telegram error: {e}")