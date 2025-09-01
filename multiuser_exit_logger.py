from datetime import datetime
import json
import os
import requests

# SAME: Multi-user support
USER_IDS = {
    "user_1": 6183259863
}
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"

def log_exit(user, asset, strike, opt_type, entry_price, exit_price, lot_size, multiplier, strategy):
    try:
        pnl = round((exit_price - entry_price) * lot_size * multiplier, 2)
        result = "Profit" if pnl >= 0 else "Loss"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        msg = (
            f"✅ Auto Exit: {asset} {strike} {opt_type}\n"
            f"💰 Entry Price: ₹{entry_price}\n"
            f"💸 Exit Price: ₹{exit_price}\n"
            f"📊 P&L: ₹{exit_price - entry_price:.2f} × {lot_size} × {multiplier} = ₹{pnl} ({result})\n"
            f"🧠 Strategy: {strategy}\n"
            f"🕒 Time: {timestamp}"
        )

        send_telegram(USER_IDS[user], msg)
        print(f"✅ Exit logged & message sent for {user}")

    except Exception as e:
        print(f"❌ Exit log error: {e}")

def send_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Telegram error: {e}")