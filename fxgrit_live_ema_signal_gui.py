import pandas as pd
import tkinter as tk
from tkinter import Label

file_path = "/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv"

def check_signal():
    try:
        df = pd.read_csv(file_path)
        df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

        prev = df.iloc[-2]
        last = df.iloc[-1]

        if prev["EMA9"] < prev["EMA20"] and last["EMA9"] > last["EMA20"]:
            return "BUY", last["Close"], df["Low"].iloc[-2]
        elif prev["EMA9"] > prev["EMA20"] and last["EMA9"] < last["EMA20"]:
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
        sl_label.config(text=f"🛑 Stop Loss: {round(sl,5)}")
        tp_label.config(text=f"🎯 Target: {round(entry + (entry - sl)*2, 5)}")
    elif signal == "SELL":
        signal_label.config(text="✅ SELL SIGNAL", bg="red")
        entry_label.config(text=f"📌 Entry: {round(entry,5)}")
        sl_label.config(text=f"🛑 Stop Loss: {round(sl,5)}")
        tp_label.config(text=f"🎯 Target: {round(entry - (sl - entry)*2, 5)}")
    elif signal == "NO SIGNAL":
        signal_label.config(text="❌ NO SIGNAL", bg="gray")
        entry_label.config(text="")
        sl_label.config(text="")
        tp_label.config(text="")
    else:
        signal_label.config(text="⚠️ ERROR", bg="black")

    root.after(5000, update_ui)

# 🖼️ UI Design
root = tk.Tk()
root.title("FXGRIT v1.0 - Live Bot")
root.geometry("350x250")
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