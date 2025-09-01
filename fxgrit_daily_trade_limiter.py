from datetime import datetime
import json
import os

MAX_TRADES_PER_DAY = 4

def can_enter_trade():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = "/storage/emulated/0/FXGRIT/Logs/Executed/filtered_trades.json"
    
    if not os.path.exists(log_file):
        return True
    
    with open(log_file, "r") as f:
        logs = json.load(f)
    
    today_trades = logs.get(today, [])
    
    return len(today_trades) < MAX_TRADES_PER_DAY

def log_filtered_trade(trade_data):
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = "/storage/emulated/0/FXGRIT/Logs/Executed/filtered_trades.json"

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = {}

    if today not in logs:
        logs[today] = []

    logs[today].append(trade_data)

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

# Example usage in bot
if can_enter_trade():
    # 💡 Ensure high-probability logic already verified
    trade = {
        "asset": "NIFTY",
        "strike": "23700",
        "type": "CALL",
        "delta": 0.56,
        "gamma": 0.017,
        "theta": -4.23,
        "strategy": "GammaBlast",
        "entry_price": 142.25,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    log_filtered_trade(trade)
    print("✅ Trade Executed & Counted")
else:
    print("🚫 Daily limit reached. No more trades allowed today.")