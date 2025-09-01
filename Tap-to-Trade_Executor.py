import json
import os
import time
from datetime import datetime
import requests

# File paths
signal_file = '/storage/emulated/0/FXGRIT/Trades/trade_execute.json'
executed_log = '/storage/emulated/0/FXGRIT/Trades/executed_log.txt'

# Telegram Config
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
VIP_CHAT_ID = '-1002433721766'

def send_telegram_alert(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': VIP_CHAT_ID, 'text': message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❌ Telegram Error:", e)

def load_signal():
    with open(signal_file, 'r') as f:
        return json.load(f)

def mark_executed(entry):
    with open(executed_log, 'a') as f:
        f.write(entry + '\n')

def already_executed(entry):
    if not os.path.exists(executed_log):
        return False
    with open(executed_log, 'r') as f:
        return entry in f.read()

print("🛠️ FXGRIT Tap-to-Trade Executor started...")

while True:
    try:
        if os.path.exists(signal_file):
            signal = load_signal()
            asset = signal.get("Asset")
            signal_type = signal.get("Signal")
            entry = float(signal.get("Entry"))
            sl = float(signal.get("SL"))
            tp1 = float(signal.get("TP1"))
            tp2 = float(signal.get("TP2"))

            unique_id = f"{entry}_{asset}"

            if not already_executed(unique_id):
                print(f"🚀 Executing {signal_type} trade for {asset}")
                print(f"🎯 Entry: {entry} | 🛑 SL: {sl} | 🎯 TP1: {tp1} | 🎯 TP2: {tp2}")
                print("✅ Trade executed successfully (simulated)")

                # ✅ Telegram Alert
                now = datetime.now().strftime('%Y-%m-%d %H:%M')
                message = f"""📢 FXGRIT TRADE EXECUTED
✅ Asset: {asset} ({signal_type})
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}
📆 Time: {now}"""
                send_telegram_alert(message)

                # ✅ Mark executed
                mark_executed(unique_id)

                # 🗑️ Delete signal file
                os.remove(signal_file)
                print("🗑️ trade_execute.json deleted after execution.\n")
            else:
                print("⚠️ Already executed – waiting for new signal.\n")
        else:
            print("⚠️ Waiting for new trade signal...\n")

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(5)