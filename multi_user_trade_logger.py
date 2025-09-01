# 🔁 FXGRIT Multi-User Trade Logger (Entry)
from datetime import datetime
import json
import os

def log_trade_entry(user_id, asset, strike, opt_type, delta, gamma, theta, premium, strategy):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_tag = now.strftime("%Y-%m-%d")

        user_log_dir = f"/storage/emulated/0/FXGRIT/Users/{user_id}/Logs/Executed"
        os.makedirs(user_log_dir, exist_ok=True)
        log_path = f"{user_log_dir}/executed_trades.json"

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

        print(f"✅ Entry saved for user {user_id}: {asset} {strike} {opt_type}")

    except Exception as e:
        print(f"❌ Error logging entry for user {user_id}: {e}")

# ✅ Example (for testing)
log_trade_entry(
    user_id="user123",
    asset="NIFTY",
    strike="23700",
    opt_type="CALL",
    delta=0.56,
    gamma=0.017,
    theta=-4.23,
    premium=142.25,
    strategy="GammaBlast"
)