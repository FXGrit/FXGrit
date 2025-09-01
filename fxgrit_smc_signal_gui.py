import pandas as pd
import tkinter as tk
from tkinter import Label

file_path = "/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv"

def detect_structure(df):
    df["HH"] = df["High"] > df["High"].shift(1)
    df["LL"] = df["Low"] < df["Low"].shift(1)
    df["CHoCH"] = False
    df["BoS"] = False

    trend = None
    for i in range(2, len(df)):
        if df["HH"].iloc[i] and df["LL"].iloc[i-1]:
            df.at[i, "CHoCH"] = True
            trend = "bullish"
        elif df["LL"].iloc[i] and df["HH"].iloc[i-1]:
            df.at[i, "CHoCH"] = True
            trend = "bearish"

        if trend == "bullish" and df["High"].iloc[i] > df["High"].iloc[i-2]:
            df.at[i, "BoS"] = True
        elif trend == "bearish" and df["Low"].iloc[i] < df["Low"].iloc[i-2]:
            df.at[i, "BoS"] = True

    return df

def check_smc_signal():
    try:
        df = pd.read_csv(file_path)
        df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
        df["MACD"] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
        df["Signal"] = df["MACD"].ewm(span=9).mean()

        df = detect_structure(df)
        last = df.iloc[-1]
        prev = df.iloc[-2]

        volume_avg = df["Volume"].iloc[-4:-1].mean()
        vol_ok = df["Volume"].iloc[-1] > volume_avg

        # BUY Condition: CHoCH + BoS + EMA + MACD + Volume
        if (last["CHoCH"] and last["BoS"] and
            prev["EMA9"] < prev["EMA20"] and last["EMA9"] > last["EMA20"] and
            prev["MACD"] < prev["Signal"] and last["MACD"] > last["Signal"] and
            vol_ok):
            return "BUY", last["Close"], df["Low"].iloc[-2]

        # SELL Condition: CHoCH + BoS + EMA + MACD + Volume
        elif (last["CHoCH"] and last["BoS"] and
              prev["EMA9"] > prev["EMA20"] and last["EMA9"] < last["EMA20"] and
              prev["MACD"] > prev["Signal"] and last["MACD"] < last["Signal"] and
              vol_ok):
            return "SELL", last["Close"], df["High"].iloc[-2]
        else:
            return "NO SIGNAL", None, None
    except Exception as e:
        print("Error:", e)
        return "ERROR", None, None

def update_ui():
    signal, entry, sl = check_smc_signal()
    if signal == "BUY":
        signal_label.config(text="✅ BUY (SMC)", bg="green")
        entry_label.config(text=f"📌 Entry: {round(entry,5)}")
        sl_label.config(text=f"🛑 SL: {round(sl,5)}")
        tp_label.config(text=f"🎯 TP: {round(entry + (entry - sl)*2, 5)}")
    elif signal == "SELL":
        signal_label.config(text="✅ SELL (SMC)", bg="red")
        entry_label.config(text=f"📌 Entry: {round(entry,5)}")
        sl_label.config(text=f"🛑 SL: {round(sl,5)}")
        tp_label.config(text=f"🎯 TP: {round(entry - (sl - entry)*2, 5)}")
    elif signal == "NO SIGNAL":
        signal_label.config(text="❌ NO SIGNAL", bg="gray")
        entry_label.config(text="")
        sl_label.config(text="")
        tp_label.config(text="")
    else:
        signal_label.config(text="⚠️ ERROR", bg="black")

    root.after(5000, update_ui)

# UI Setup
root = tk.Tk()
root.title("FXGRIT SMC v2 – CHoCH + BoS Mode")
root.geometry("380x270")
root.configure(bg="black")

signal_label = Label(root, text="Checking...", font=("Helvetica", 18), fg="white", bg="black")
signal_label.pack(pady=10)

entry_label = Label(root, text="", font=("Helvetica", 14), fg="white", bg="black")
entry_label.pack()

sl_label = Label(root, text="", font=("Helvetica", 14), fg="white", bg="black")
sl_label.pack()

tp_label = Label(root, text="", font=("Helvetica", 14), fg="white", bg="black")
tp_label.pack()

update_ui()
root.mainloop()