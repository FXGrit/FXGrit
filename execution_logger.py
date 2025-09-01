# fxgrit_logger.py 🔁 FXGRIT Execution Logger
from datetime import datetime
import json
import os

def confirm_trade_execution(asset, strike, opt_type, delta, gamma, theta, strategy):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_tag = now.strftime("%Y-%m-%d")

        log_dir = "/storage/emulated/0/FXGRIT/Logs/Executed"
        os.makedirs(log_dir, exist_ok=True)
        log_path = f"{log_dir}/executed_trades.json"

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
            "strategy": strategy,
            "time": timestamp
        }

        if date_tag not in data:
            data[date_tag] = []

        data[date_tag].append(trade)

        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Trade Executed: {asset} {strike} {opt_type} | Strategy: {strategy}")
        print(f"📁 Log Updated: {log_path}")

    except Exception as e:
        print(f"❌ Execution log failed: {e}")