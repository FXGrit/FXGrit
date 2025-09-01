import time
import json
import requests
import os

# Telegram credentials
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '-1002433721766'  # VIP Channel ID

# JSON File path
JSON_PATH = "/storage/emulated/0/FXGRIT/Signals/latest_signal.json"

# For checking if signal already sent
last_sent = None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

print("📡 FXGRIT Signal Monitor Started...\n")

while True:
    try:
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as f:
                data = json.load(f)

            # Convert to string to compare uniqueness
            signal_str = json.dumps(data)

            if signal_str != last_sent:
                last_sent = signal_str

                asset = data['asset']
                signal = data['signal']
                entry = data['entry']
                sl = data['sl']
                tp1 = data['tp1']
                tp2 = data['tp2']

                # Build formatted message
                message = (
                    f"✅ Signal: {signal}\n"
                    f"💰 Asset: {asset}\n"
                    f"🎯 Entry: {entry}\n"
                    f"🛑 SL: {sl}\n"
                    f"🎯 TP1: {tp1}\n"
                    f"🎯 TP2: {tp2}"
                )

                print("📤 Sending Signal...")
                send_telegram_message(message)
            else:
                print("ℹ️ No new signal.")

        else:
            print("⚠️ Signal file not found.")

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(5)