import json, os, time
from datetime import datetime, timedelta

# 🔁 Load P&L logs for a specific asset
def get_trade_history(asset):
    try:
        log_path = "/storage/emulated/0/FXGRIT/Logs/trade_logs.json"
        if not os.path.exists(log_path):
            return []
        with open(log_path) as f:
            data = json.load(f)
        return [t for t in data if t["Asset"] == asset]
    except:
        return []

# 🧠 Check if over-trading is happening
def check_over_trading(asset):
    trades = get_trade_history(asset)
    today = datetime.now().strftime("%Y-%m-%d")
    today_trades = [t for t in trades if t["Date"].startswith(today)]

    if len(today_trades) >= 3:
        return False, "🛑 Max 3 trades allowed per day"

    if len(today_trades) >= 1:
        last_trade_time = datetime.strptime(today_trades[-1]["Date"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last_trade_time < timedelta(minutes=15):
            return False, "🕒 Wait 15 mins between trades"

    if len(today_trades) >= 2 and today_trades[-1]["P&L"] < 0 and today_trades[-2]["P&L"] < 0:
        return False, "🛑 2 Consecutive Losses – Cooldown active"

    return True, "✅ Trade allowed"

# 🔁 Trade Execution Example
def execute_trade(asset):
    allowed, message = check_over_trading(asset)
    print(message)
    if allowed:
        print(f"🚀 Executing trade for {asset}")
        # Add your trade execution code here
    else:
        print(f"❌ Trade blocked for {asset}")

# 🔁 Example Trigger
execute_trade("NIFTY")