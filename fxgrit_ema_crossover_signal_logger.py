import pandas as pd
import requests
from datetime import datetime
import os

# ✅ Telegram Bot Setup
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '6183259863'

# ✅ File Paths
chart_file = '/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data.csv'
log_file = '/storage/emulated/0/FXGrit/fxgrit_signal_log.xlsx'
backup_file = '/storage/emulated/0/FXGrit/fxgrit_signal_backup.xlsx'

# ✅ Send Telegram Message
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

# ✅ Load CSV (keep only last 150 rows)
df = pd.read_csv(chart_file)
df = df.tail(150)
df.to_csv(chart_file, index=False)  # Save cleaned chart data

# ✅ Indicators
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()
latest = df.iloc[-1]
prev = df.iloc[-2]

# ✅ Signal Detection
signal = None
if prev['EMA9'] < prev['EMA20'] and latest['EMA9'] > latest['EMA20']:
    signal = "BUY"
elif prev['EMA9'] > prev['EMA20'] and latest['EMA9'] < latest['EMA20']:
    signal = "SELL"

# ✅ On Signal
if signal:
    entry = round(latest['Close'], 5)
    sl = round(entry - 0.0010, 5) if signal == "BUY" else round(entry + 0.0010, 5)
    tp1 = round(entry + 0.0020, 5) if signal == "BUY" else round(entry - 0.0020, 5)
    tp2 = round(entry + 0.0030, 5) if signal == "BUY" else round(entry - 0.0030, 5)
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ✅ Message
    msg = f"""📢 FXGRIT ALERT
🕒 Time: {entry_time}
✅ Signal: {signal}
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}"""
    send_telegram(msg)

    # ✅ Excel Log Handling
    new_row = pd.DataFrame({
        'Time': [entry_time],
        'Signal': [signal],
        'Entry': [entry],
        'SL': [sl],
        'TP1': [tp1],
        'TP2': [tp2]
    })

    if os.path.exists(log_file):
        old_log = pd.read_excel(log_file)
        combined = pd.concat([old_log, new_row], ignore_index=True)
        trimmed = combined.tail(500)  # ✅ Keep only last 500
    else:
        trimmed = new_row

    # ✅ Save to Excel Log and Backup
    trimmed.to_excel(log_file, index=False)
    trimmed.to_excel(backup_file, index=False)

    print("✅ Signal Sent & Logged")

else:
    print("ℹ️ No signal found – waiting for perfect condition.")