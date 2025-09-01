from datetime import datetime
import json
import os
import requests

# Telegram Details
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
CHAT_ID = "-1002416993114"  # FXGrit VIP Group Channel ID

# Multiplier config (e.g., NIFTY = 75, BANKNIFTY = 35, RELIANCE = 500)
LOT_SIZES = {
    "NIFTY": 75,
    "BANKNIFTY": 35,
    "RELIANCE": 500
}

MULTIPLIER = 1  # Can change to 2, 3 if user trades 2 or 3 lots

# Sample dummy trade
trade = {
    "asset": "NIFTY",
    "strike": "23700",
    "type": "CALL",
    "delta": 0.56,
    "gamma": 0.017,
    "theta": -4.23,
    "strategy": "GammaBlast",
    "entry_price": 142.25,
    "exit_price": 156.95,
    "time_entry": "2025-07-19 00:21:18",
    "time_exit": "2025-07-19 09:35:40"
}

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ Telegram message sent.")
        else:
            print(f"❌ Telegram error: {r.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")

def log_and_notify_trade(trade):
    asset = trade["asset"]
    lot_size = LOT_SIZES.get(asset, 1)
    premium_entry = trade["entry_price"]
    premium_exit = trade["exit_price"]
    pnl = round(premium_exit - premium_entry, 2)
    total_pnl = round(pnl * lot_size * MULTIPLIER, 2)
    result = "Profit" if pnl > 0 else "Loss"

    # ENTRY MESSAGE
    entry_msg = (
        f"✅ <b>Entry Confirmed:</b> {asset} {trade['strike']} {trade['type']}\n"
        f"📊 Delta: {trade['delta']} | Gamma: {trade['gamma']} | Theta: {trade['theta']}\n"
        f"💰 Premium: ₹{premium_entry}\n"
        f"📈 Strategy: {trade['strategy']}\n"
        f"🕒 Time: {trade['time_entry']}"
    )

    # EXIT MESSAGE
    exit_msg = (
        f"✅ <b>Auto Exit:</b> {asset} {trade['strike']} {trade['type']}\n"
        f"💰 Entry Price: ₹{premium_entry}\n"
        f"💸 Exit Price: ₹{premium_exit}\n"
        f"📊 P&L: ₹{pnl} × {lot_size} × {MULTIPLIER} = ₹{total_pnl} ({result})\n"
        f"🧠 Strategy: {trade['strategy']}\n"
        f"🕒 Time: {trade['time_exit']}"
    )

    send_to_telegram(entry_msg)
    send_to_telegram(exit_msg)

# 🔁 Trigger test
log_and_notify_trade(trade)