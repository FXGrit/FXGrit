import json
import os
from datetime import datetime, timedelta

# CONFIGURABLE PARAMETERS
MAX_DAILY_LOSS = -3000  # ₹ में
MAX_TRADES_PER_DAY = 10
COOLDOWN_MINUTES = 5

# File paths
log_path = "/storage/emulated/0/FXGRIT/Logs/Executed/executed_trades.json"
state_path = "/storage/emulated/0/FXGRIT/Temp/risk_state.json"

def is_trade_allowed():
    now = datetime.now()
    date_tag = now.strftime("%Y-%m-%d")

    # Load trade history
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    trades_today = data.get(date_tag, [])

    # Calculate total P&L
    total_pl = 0
    for t in trades_today:
        entry = float(t.get("entry_price", 0))
        exit_ = float(t.get("exit_price", 0))
        lots = int(t.get("lots", 1))
        qty = int(t.get("lot_size", 50))
        total_pl += (exit_ - entry) * lots * qty

    # Load last trade time
    if os.path.exists(state_path):
        with open(state_path, 'r') as f:
            state = json.load(f)
    else:
        state = {}

    last_trade_time = state.get("last_trade_time")
    if last_trade_time:
        last_time = datetime.strptime(last_trade_time, "%Y-%m-%d %H:%M:%S")
        if now - last_time < timedelta(minutes=COOLDOWN_MINUTES):
            print(f"❌ Trade Cooldown Active: Wait for {COOLDOWN_MINUTES} mins.")
            return False

    if len(trades_today) >= MAX_TRADES_PER_DAY:
        print(f"❌ Max daily trades ({MAX_TRADES_PER_DAY}) reached.")
        return False

    if total_pl <= MAX_DAILY_LOSS:
        print(f"❌ Daily loss limit reached: ₹{total_pl}")
        return False

    # ✅ Allowed: Update last trade time
    state["last_trade_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    print("✅ Trade allowed by Risk Control")
    return True