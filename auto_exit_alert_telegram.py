# 🔁 FXGRIT Auto Exit Module
import json
import os
from datetime import datetime
import requests

# ✅ Telegram credentials
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
VIP_CHAT_ID = "-1002416993114"  # FXGRIT VIP Group ID

# ✅ Auto Exit Trigger
def auto_exit_trade():
    try:
        # 🔹 Path to live trade file
        live_path = "/storage/emulated/0/FXGRIT/Temp/live_trade.json"
        with open(live_path, "r") as f:
            trade = json.load(f)

        asset = trade["asset"]
        strike = trade["strike"]
        opt_type = trade["type"]
        entry_price = trade["entry"]
        exit_price = trade.get("exit", None)

        # ❌ If no exit price found
        if exit_price is None:
            raise Exception("❌ Auto Exit Error: 'exit' price missing in live_trade.json")

        # 🔹 Calculate P&L
        pnl = round(exit_price - entry_price, 2)

        # ✅ Save to log
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        log_path = "/storage/emulated/0/FXGRIT/Logs/Executed/auto_exit_log.json"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

        date_tag = now.strftime("%Y-%m-%d")
        record = {
            "asset": asset,
            "strike": strike,
            "type": opt_type,
            "entry": entry_price,
            "exit": exit_price,
            "pnl": pnl,
            "time": timestamp
        }

        if date_tag not in data:
            data[date_tag] = []

        data[date_tag].append(record)

        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Auto Exit: {asset}_{strike}_{opt_type} | P&L: ₹{pnl}")
        send_telegram_exit_message(asset, strike, opt_type, pnl)

    except Exception as e:
        print(f"❌ Auto Exit Error: {e}")

# ✅ Telegram VIP Message
def send_telegram_exit_message(asset, strike, opt_type, pnl):
    try:
        message = f"✅ Auto Exit: {asset}_{strike}_{opt_type} | P&L: ₹{pnl}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": VIP_CHAT_ID,
            "text": message
        }

        response = requests.post(url, json=payload)
        if response.ok:
            print("✅ Telegram message sent to VIP channel.")
        else:
            print(f"❌ Telegram error: {response.text}")

    except Exception as e:
        print(f"❌ Telegram sending failed: {e}")

# ▶️ Run Auto Exit
if __name__ == "__main__":
    auto_exit_trade()