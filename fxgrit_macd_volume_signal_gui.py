import pandas as pd
import tkinter as tk
from tkinter import Label

file_path = "/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv"

def calculate_macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal_line

def is_volume_strong(df):
    avg_vol = df["Volume"].iloc[-4:-1].mean()
    current_vol = df["Volume"].iloc[-1]
    return current_vol > avg_vol

def check_signal():
    try:
        df = pd.read_csv(file_path)
        df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
        df["MACD"], df["Signal"] = calculate_macd(df)

        prev = df.iloc[-2]
        last = df.iloc[-1]

        vol_ok = is_volume_strong(df)

        # BUY: EMA + MACD cross UP + volume confirm
        if (prev["EMA9"] < prev["EMA20"] and last["EMA9"] > last["EMA20"] and
            prev["MACD"] < prev["Signal"] and last["MACD"] > last["Signal"] and vol_ok):
            return "BUY", last["Close"], df["Low"].iloc[-2]
        
        # SELL: EMA + MACD cross DOWN + volume confirm
        elif (prev["EMA9"] > prev["EMA20"] and last["EMA9"] < last["EMA20"] and
              prev["MACD"] > prev["Signal"] and last["MACD"] < last["Signal"] and vol_ok):
            return "SELL", last["Close"], df["High"].iloc[-2]
        
        else:
            return "NO SIGNAL", None, None
    except Exception as e:
        print("Error:", e)
        return "ERROR", None, None

def update_ui():
    signal, entry, sl = check_signal()
    if signal == "BUY":
        signal_label.config(text="✅ BUY SIGNAL", bg="green")
        entry_label.config(text=f"📌 Entry: {round(entry,5)}")
        sl_label.config(text=f"🛑 SL: {round(sl,5)}")
        tp_label.config(text=f"🎯 TP: {round(entry + (entry - sl)*2, 5)}")
    elif signal == "SELL":
        signal_label.config(text="✅ SELL SIGNAL", bg="red")
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

# 🎨 UI Setup
root = tk.Tk()
root.title("FXGRIT Pro – MACD + Volume")
root.geometry("360x260")
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