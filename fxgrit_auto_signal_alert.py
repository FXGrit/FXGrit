import pandas as pd
import requests
from datetime import datetime
import os

# ✅ Telegram Bot Setup
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '6183259863'

# ✅ File Paths
input_file = '/storage/emulated/0/FXGRIT/fxgrit_buy_signal_data.xlsx'
log_file = '/storage/emulated/0/FXGRIT/fxgrit_signal_log.xlsx'

# ✅ Telegram Sender
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

# ✅ Log to Excel
def log_to_excel(entry_time, signal, entry, sl, tp1, tp2):
    data = {
        'Time': [entry_time],
        'Signal': [signal],
        'Entry': [entry],
        'SL': [sl],
        'TP1': [tp1],
        'TP2': [tp2]
    }
    df_log = pd.DataFrame(data)

    if os.path.exists(log_file):
        old_log = pd.read_excel(log_file)
        new_log = pd.concat([old_log, df_log], ignore_index=True)
    else:
        new_log = df_log

    new_log.to_excel(log_file, index=False)

# ✅ Load Excel Data
df = pd.read_excel(input_file)

# ✅ Indicators
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()

# ✅ Latest Candles
latest = df.iloc[-1]
prev = df.iloc[-2]

# ✅ Signal Logic
signal = None
if prev['EMA9'] < prev['EMA20'] and latest['EMA9'] > latest['EMA20']:
    signal = "BUY"
elif prev['EMA9'] > prev['EMA20'] and latest['EMA9'] < latest['EMA20']:
    signal = "SELL"

if signal:
    entry = round(latest['Close'], 5)
    sl = round(entry - 0.0010, 5) if signal == "BUY" else round(entry + 0.0010, 5)
    tp1 = round(entry + 0.0020, 5) if signal == "BUY" else round(entry - 0.0020, 5)
    tp2 = round(entry + 0.0030, 5) if signal == "BUY" else round(entry - 0.0030, 5)
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = f"""📢 FXGRIT ALERT
🕒 Time: {entry_time}
✅ Signal: {signal}
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}"""

    send_telegram_message(msg)
    log_to_excel(entry_time, signal, entry, sl, tp1, tp2)

    print("✅ Signal Sent & Logged")
else:
    print("ℹ️ No Signal Found")