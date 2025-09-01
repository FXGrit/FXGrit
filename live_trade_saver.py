# 🔁 FXGRIT Live Trade Saver
import json
import os
from datetime import datetime

def save_live_trade(asset, strike, opt_type, entry, strategy):
    try:
        temp_dir = "/storage/emulated/0/FXGRIT/Temp"
        os.makedirs(temp_dir, exist_ok=True)
        live_path = f"{temp_dir}/live_trade.json"

        trade = {
            "asset": asset,
            "strike": strike,
            "type": opt_type,
            "entry": entry,
            "strategy": strategy,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(live_path, "w") as f:
            json.dump(trade, f, indent=2)

        print(f"✅ Live trade saved: {asset}_{strike}_{opt_type}")
        print(f"📁 File: {live_path}")

    except Exception as e:
        print(f"❌ Error saving live trade: {e}")

# 🧪 Example Usage:
save_live_trade(
    asset="NIFTY",
    strike="23700",
    opt_type="CALL",
    entry=124.5,
    strategy="GammaBlast"
)