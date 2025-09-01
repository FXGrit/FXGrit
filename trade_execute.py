import pandas as pd
import os
import json
from datetime import datetime
import requests

# Config
BOT_TOKEN = 'YOUR_BOT_TOKEN'
VIP_CHANNEL_ID = 'YOUR_VIP_CHANNEL_ID'

BASE_LOT = 0.01
RISK_MULTIPLIER = 0.0001
log_path = '/storage/emulated/0/FXGRIT/fxgrit_signal_log.xlsx'
trade_path = '/storage/emulated/0/FXGRIT/Trades/trade_execute.json'

# Sample latest signal
latest_signal = {
    "Asset": "BTCUSD",
    "Signal": "BUY",
    "Entry": 67215.5,
    "SL": 67115.5,
    "TP1": 67315.5,
    "TP2": 67415.5
}

# 1. Calculate Lot Size from Log
def calculate_lot():
    if not os.path.exists(log_path):
        return BASE_LOT
    df = pd.read_excel(log_path)
    net_pl = (df['TP1'] - df['Entry']).sum() - (df['Entry'] - df['SL']).sum()
    return round(BASE_LOT + (net_pl * RISK_MULTIPLIER), 2)

# 2. Send to Telegram
def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': VIP_CHANNEL_ID, 'text': text}
    requests.post(url, data=data)

# 3. Save Trade to JSON
def save_trade(signal, lot):
    trade_data = {
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "asset": signal['Asset'],
        "signal": signal['Signal'],
        "entry": signal['Entry'],
        "sl": signal['SL'],
        "tp1": signal['TP1'],
        "tp2": signal['TP2'],
        "lot": lot
    }
    with open(trade_path, 'w') as f:
        json.dump(trade_data, f, indent=2)

# 4. Trigger Full Flow
lot = calculate_lot()
save_trade(latest_signal, lot)

msg = f"""📢 FXGRIT VIP SIGNAL
✅ Signal: {latest_signal['Signal']}
💰 Asset: {latest_signal['Asset']}
🎯 Entry: {latest_signal['Entry']}
🛑 SL: {latest_signal['SL']}
🎯 TP1: {latest_signal['TP1']}
🎯 TP2: {latest_signal['TP2']}
📦 Lot Size: {lot}"""
send_to_telegram(msg)

print("✅ Signal saved & sent to VIP")