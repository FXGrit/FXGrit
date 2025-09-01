import pandas as pd
import time
import os

# Step 1: CSV File Location
file_path = "/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv"

# Step 2: Loop forever (use Ctrl+C to stop manually)
while True:
    os.system('clear')  # for screen clear (optional)

    try:
        df = pd.read_csv(file_path)
        df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

        prev = df.iloc[-2]
        last = df.iloc[-1]

        signal = "❌ No Signal"
        entry = sl = target = None

        if prev["EMA9"] < prev["EMA20"] and last["EMA9"] > last["EMA20"]:
            signal = "✅ BUY ENTRY"
            entry = round(last["Close"], 5)
            sl = round(df["Low"].iloc[-2], 5)
            target = round(entry + (entry - sl) * 2, 5)

        elif prev["EMA9"] > prev["EMA20"] and last["EMA9"] < last["EMA20"]:
            signal = "✅ SELL ENTRY"
            entry = round(last["Close"], 5)
            sl = round(df["High"].iloc[-2], 5)
            target = round(entry - (sl - entry) * 2, 5)

        print("🔁 FXGRIT AUTO-SCAN MODE")
        print("🧠 Powered by FXGRIT v1.0")
        print("➡️", signal)
        if entry:
            print("📌 Entry:", entry)
            print("🛑 SL:", sl)
            print("🎯 Target:", target)
        
    except Exception as e:
        print("❌ Error:", e)

    time.sleep(5)  # 🔁 Scan every 5 seconds