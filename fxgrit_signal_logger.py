import pandas as pd
import csv
from datetime import datetime

# ✅ Step 1: Load CSV File
file_path = '/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv'
data = pd.read_csv(file_path)

# ✅ Step 2: Calculate EMAs
data['EMA9'] = data['Close'].rolling(window=9).mean()
data['EMA20'] = data['Close'].rolling(window=20).mean()
data['FXGRIT_SIGNAL'] = None

# ✅ Step 3: Generate Buy/Sell Signal
for i in range(1, len(data)):
    if data['EMA9'][i] > data['EMA20'][i] and data['EMA9'][i-1] <= data['EMA20'][i-1]:
        data.at[i, 'FXGRIT_SIGNAL'] = 'BUY'
    elif data['EMA9'][i] < data['EMA20'][i] and data['EMA9'][i-1] >= data['EMA20'][i-1]:
        data.at[i, 'FXGRIT_SIGNAL'] = 'SELL'

# ✅ Step 4: Get latest row
latest = data.iloc[-1]
signal = latest['FXGRIT_SIGNAL']
close = round(latest['Close'], 5)

# ✅ Step 5: Entry / SL / TP
if signal == 'BUY':
    entry = close
    sl = round(entry - 0.0010, 5)
    tp1 = round(entry + 0.0020, 5)
    tp2 = round(entry + 0.0030, 5)
elif signal == 'SELL':
    entry = close
    sl = round(entry + 0.0010, 5)
    tp1 = round(entry - 0.0020, 5)
    tp2 = round(entry - 0.0030, 5)
else:
    entry = sl = tp1 = tp2 = None

# ✅ Step 6: Log the trade only if signal is valid
def log_trade(signal, entry, sl, tp1, tp2):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [now, signal, entry, sl, tp1, tp2]

    log_file = '/storage/emulated/0/FXGRIT/fxgrit_trade_log.csv'
    try:
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        print("📝 Trade Logged Successfully")
    except Exception as e:
        print("⚠️ Failed to log trade:", e)

# ✅ Step 7: Execute
if signal in ['BUY', 'SELL']:
    print(f"✅ FXGRIT Signal: {signal}")
    log_trade(signal, entry, sl, tp1, tp2)
else:
    print("🚫 No Signal – Nothing to Log")