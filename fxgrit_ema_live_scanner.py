import pandas as pd
import requests
import time

# File path
file_path = '/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data.csv'

# Telegram Bot Token & Chat ID
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '6183259863'

# Telegram Send Function
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# Last signal tracker to avoid repeat
last_signal = ""

# Real-time Scan Loop
while True:
    try:
        df = pd.read_csv(file_path)

        df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

        prev_ema9 = df['EMA9'].iloc[-2]
        prev_ema20 = df['EMA20'].iloc[-2]
        curr_ema9 = df['EMA9'].iloc[-1]
        curr_ema20 = df['EMA20'].iloc[-1]

        signal = ""
        if prev_ema9 < prev_ema20 and curr_ema9 > curr_ema20:
            signal = "✅ FXGRIT SIGNAL: BUY 🔼 Confirmed"
        elif prev_ema9 > prev_ema20 and curr_ema9 < curr_ema20:
            signal = "✅ FXGRIT SIGNAL: SELL 🔽 Confirmed"

        # Send only if signal is new
        if signal and signal != last_signal:
            send_telegram(signal)
            print(signal)
            last_signal = signal

    except Exception as e:
        print("⚠️ Error:", e)

    time.sleep(5)  # Wait 5 seconds before next check