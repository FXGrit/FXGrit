import pandas as pd
import time
import os
import requests

# Telegram Config
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
VIP_CHAT_ID = "-1002416993114"

def send_to_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": VIP_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Telegram Error:", e)

# CSV File Location
file_path = "/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv"

active_signal = None  # store active trade for trailing

# कितने point move पर trailing SL shift करना है
TRAIL_STEP = 0.5  

while True:
    os.system("clear")

    try:
        df = pd.read_csv(file_path)

        if len(df) > 3:
            df = df.tail(3)

        df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

        prev = df.iloc[-2]
        last = df.iloc[-1]

        signal = "❌ No Signal"
        entry = sl = None

        # BUY Condition
        if prev["EMA9"] < prev["EMA20"] and last["EMA9"] > last["EMA20"]:
            signal = "✅ BUY ENTRY"
            entry = round(last["Close"], 5)
            sl = round(df["Low"].iloc[-2], 5)

        # SELL Condition
        elif prev["EMA9"] > prev["EMA20"] and last["EMA9"] < last["EMA20"]:
            signal = "✅ SELL ENTRY"
            entry = round(last["Close"], 5)
            sl = round(df["High"].iloc[-2], 5)

        print("🔁 FXGRIT AUTO-SCAN MODE (VIP Only)")
        print("🧠 Powered by FXGRIT v3.0 (Point-to-Point Trailing)")
        print("➡️", signal)

        if entry:
            print("📌 Entry:", entry)
            print("🛑 SL:", sl)

            active_signal = {
                "type": "BUY" if "BUY" in signal else "SELL",
                "entry": entry,
                "sl": sl,
                "last_trail": entry,  # last price where trail updated
                "active": True
            }

            message = f"""
<b>🚨 FXGRIT VIP Signal</b>
➡️ {signal}
💰 Entry: {entry}
🛑 SL: {sl}
            """
            send_to_telegram(message)

        # ✅ POINT-TO-POINT TRAILING SL
        if active_signal:
            current_price = last["Close"]
            sig_type = active_signal["type"]

            # BUY trailing
            if sig_type == "BUY":
                if current_price >= active_signal["last_trail"] + TRAIL_STEP:
                    new_sl = active_signal["sl"] + TRAIL_STEP
                    if new_sl < current_price:  # SL should always stay below price
                        active_signal["sl"] = round(new_sl, 5)
                        active_signal["last_trail"] = current_price
                        send_to_telegram(f"📢 Trailing SL Updated (BUY)\n🛑 New SL: {active_signal['sl']}")

            # SELL trailing
            elif sig_type == "SELL":
                if current_price <= active_signal["last_trail"] - TRAIL_STEP:
                    new_sl = active_signal["sl"] - TRAIL_STEP
                    if new_sl > current_price:  # SL should always stay above price
                        active_signal["sl"] = round(new_sl, 5)
                        active_signal["last_trail"] = current_price
                        send_to_telegram(f"📢 Trailing SL Updated (SELL)\n🛑 New SL: {active_signal['sl']}")

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(300)  # scan every 5 min
