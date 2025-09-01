import json
import os
import time
from datetime import datetime

# File path
signal_file = '/storage/emulated/0/FXGRIT/Trades/trade_execute.json'
executed_log = '/storage/emulated/0/FXGRIT/Trades/executed_log.txt'

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
            unique_id = signal.get("Entry", "") + "_" + signal.get("Asset", "")

            if not already_executed(unique_id):
                print("✅ Trade Executed for:", signal['Asset'])
                print("📈 Signal:", signal['Signal'])
                print("🎯 Entry:", signal['Entry'], "TP1:", signal['TP1'], "TP2:", signal['TP2'])
                print("🛑 SL:", signal['SL'])

                mark_executed(unique_id)
            else:
                print("⏳ No new trade signal.")
        else:
            print("⚠️ Signal file not found.")
    except Exception as e:
        print("❌ Error:", e)

    time.sleep(5)