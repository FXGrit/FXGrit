import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv"
df = pd.read_csv(file_path)

# Step 2: Calculate EMA
df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

# Step 3: Last 10 candles only (zoom view)
df = df[-10:].reset_index(drop=True)

# Step 4: Check signal
prev = df.iloc[-2]
last = df.iloc[-1]

signal = None
entry = sl = target = None

if prev["EMA9"] < prev["EMA20"] and last["EMA9"] > last["EMA20"]:
    signal = "BUY"
    entry = last["Close"]
    sl = df["Low"].iloc[-2]
    target = entry + (entry - sl) * 2

elif prev["EMA9"] > prev["EMA20"] and last["EMA9"] < last["EMA20"]:
    signal = "SELL"
    entry = last["Close"]
    sl = df["High"].iloc[-2]
    target = entry - (sl - entry) * 2

# Step 5: Plot
plt.figure(figsize=(10,5))
plt.plot(df["Close"], label="Close", color='black')
plt.plot(df["EMA9"], label="EMA 9", color='blue')
plt.plot(df["EMA20"], label="EMA 20", color='orange')

# Entry / SL / Target lines
if signal:
    plt.scatter(len(df)-1, entry, color='green', s=100, label="ENTRY")
    plt.axhline(y=sl, color='red', linestyle='--', label="STOP LOSS")
    plt.axhline(y=target, color='gold', linestyle='--', label="TARGET")

plt.title("📊 FXGRIT SIGNAL CHART")
plt.xlabel("Candles")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()