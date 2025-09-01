import pandas as pd
import requests
from datetime import datetime

# ✅ Telegram Bot Credentials
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '6183259863'

# ✅ Load CSV File (Change filename if needed)
df = pd.read_csv('/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data(1).csv')

# ✅ Indicator Calculation
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()
df['RSI'] = df['Close'].rolling(window=14).apply(lambda x: ((x.diff() > 0).sum() / 14) * 100)
df['VolumeSpike'] = df['Volume'] > df['Volume'].rolling(window=10).mean()

# ✅ Signal Detection Logic
latest = df.iloc[-1]
prev = df.iloc[-2]

signal = None
if (
    prev['EMA9'] < prev['EMA20'] and
    latest['EMA9'] > latest['EMA20'] and
    latest['RSI'] > 55 and
    latest['VolumeSpike']
):
    signal = "BUY"
elif (
    prev['EMA9'] > prev['EMA20'] and
    latest['EMA9'] < latest['EMA20'] and
    latest['RSI'] < 45 and
    latest['VolumeSpike']
):
    signal = "SELL"

# ✅ Send Signal
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

if signal:
    entry = round(latest['Close'], 5)
    sl = round(entry - 0.0010, 5) if signal == "BUY" else round(entry + 0.0010, 5)
    tp1 = round(entry + 0.0020, 5) if signal == "BUY" else round(entry - 0.0020, 5)
    tp2 = round(entry + 0.0030, 5) if signal == "BUY" else round(entry - 0.0030, 5)

    msg = f"""📢 FXGRIT ALERT
🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
✅ Signal: {signal}
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}"""
    send_telegram(msg)
    print("✅ Signal Sent!")
else:
    print("ℹ️ No signal found – waiting for perfect condition.")