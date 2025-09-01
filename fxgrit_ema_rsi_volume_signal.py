import pandas as pd
import ta
import requests
from datetime import datetime

# ✅ Telegram Bot Setup
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '6183259863'

def send_telegram_message(signal_type, entry, sl, tp1, tp2):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"""📢 FXGRIT ALERT
🕒 Time: {now}
✅ Signal: {signal_type}
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}"""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

# ✅ Load CSV
df = pd.read_csv('/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data.csv')

# ✅ Indicators
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()
df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

# ✅ Signal Logic
latest = df.iloc[-1]
prev = df.iloc[-2]

if (
    prev['EMA9'] < prev['EMA20'] and
    latest['EMA9'] > latest['EMA20'] and
    latest['RSI'] > 55 and
    latest['Volume'] > df['Volume'].iloc[-3]
):
    signal = "BUY"
    entry = round(latest['Close'], 5)
    sl = round(entry - 0.0010, 5)
    tp1 = round(entry + 0.0020, 5)
    tp2 = round(entry + 0.0030, 5)
    
    send_telegram_message(signal, entry, sl, tp1, tp2)
    print("✅ Signal Sent to Telegram")
else:
    print("🚫 No Signal Found")