from datetime import datetime
import json
import os
import requests

# --- Configuration ---
TELEGRAM_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
TELEGRAM_CHAT_ID = '-1002416993114'  # VIP channel ID
LOT_SIZE = {
    "NIFTY": 50,
    "BANKNIFTY": 15,
    "RELIANCE": 250
}

# --- Function ---
def send_auto_exit_message(asset, strike, opt_type, entry_price, exit_price, strategy, quantity=1):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        lot = LOT_SIZE.get(asset.upper(), 1)
        pnl = round((exit_price - entry_price) * lot * quantity, 2)
        diff = round(exit_price - entry_price, 2)
        status = "Profit" if pnl > 0 else "Loss"

        msg = (
            f"✅ Auto Exit: {asset} {strike} {opt_type}\n"
            f"💰 Entry Price: ₹{entry_price:.2f}\n"
            f"💸 Exit Price: ₹{exit_price:.2f}\n"
            f"📊 P&L: ₹{diff:.2f} × {lot} × {quantity} = ₹{pnl:.2f} ({status})\n"
            f"🧠 Strategy: {strategy}\n"
            f"🕒 Time: {timestamp}"
        )

        # Telegram Send
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ Auto Exit message sent to VIP Telegram.")
        else:
            print("❌ Telegram send failed:", r.text)

        # Save to Log
        log_dir = "/storage/emulated/0/FXGRIT/Logs/Exited"
        os.makedirs(log_dir, exist_ok=True)
        log_path = f"{log_dir}/auto_exit_trades.json"

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

        date_key = now.strftime("%Y-%m-%d")
        trade = {
            "asset": asset,
            "strike": strike,
            "type": opt_type,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": pnl,
            "strategy": strategy,
            "time": timestamp
        }

        data.setdefault(date_key, []).append(trade)
        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Trade saved to exit log.")

    except Exception as e:
        print(f"❌ Auto Exit Error: {e}")


# 🔃 Run test (dummy)
send_auto_exit_message(
    asset="NIFTY",
    strike="23700",
    opt_type="CALL",
    entry_price=142.25,
    exit_price=156.95,
    strategy="GammaBlast",
    quantity=1  # ← Set to 2 for double lots
)