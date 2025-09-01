from datetime import datetime
import json
import os

def send_telegram(message):
    import requests
    token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def auto_exit_trade(asset, strike, opt_type, entry_price, exit_price, strategy, lot_size=50, qty_multiplier=1):
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        pnl_per_lot = round(exit_price - entry_price, 2)
        total_profit = round(pnl_per_lot * lot_size * qty_multiplier, 2)
        result = "Profit" if pnl_per_lot > 0 else "Loss"

        message = (
            f"✅ <b>Auto Exit:</b> {asset} {strike} {opt_type}\n"
            f"💰 <b>Entry Price:</b> ₹{entry_price:.2f}\n"
            f"💸 <b>Exit Price:</b> ₹{exit_price:.2f}\n"
            f"📊 <b>P&L:</b> ₹{pnl_per_lot:.2f} × {lot_size} × {qty_multiplier} = ₹{total_profit:.2f} ({result})\n"
            f"🧠 <b>Strategy:</b> {strategy}\n"
            f"🕒 <b>Time:</b> {timestamp}"
        )

        print(message)
        send_telegram(message)

        log_dir = "/storage/emulated/0/FXGRIT/Logs/Exit"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "auto_exit_log.json")

        exit_log = {
            "asset": asset,
            "strike": strike,
            "type": opt_type,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl_per_lot": pnl_per_lot,
            "total_profit": total_profit,
            "strategy": strategy,
            "timestamp": timestamp
        }

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(exit_log)

        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Trade Executed & Counted")

    except Exception as e:
        print(f"❌ Auto Exit Error: {e}")