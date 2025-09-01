import pandas as pd

# Step 1: Load the CSV
df = pd.read_csv('/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data.csv')

# Step 2: Calculate EMA
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()

# Step 3: Get last 2 candles
prev = df.iloc[-2]
latest = df.iloc[-1]

# Step 4: Signal Check
if (
    prev['EMA9'] < prev['EMA20'] and
    latest['EMA9'] > latest['EMA20']
):
    print("✅ BUY Signal Confirmed")
elif (
    prev['EMA9'] > prev['EMA20'] and
    latest['EMA9'] < latest['EMA20']
):
    print("✅ SELL Signal Confirmed")
else:
    print("ℹ️ No Signal")