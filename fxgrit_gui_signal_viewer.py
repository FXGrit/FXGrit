import pandas as pd
import tkinter as tk

# Load CSV file
file_path = '/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv'
df = pd.read_csv(file_path)

# EMA
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()

# MACD
df['EMA12'] = df['Close'].ewm(span=12).mean()
df['EMA26'] = df['Close'].ewm(span=26).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['SignalLine'] = df['MACD'].ewm(span=9).mean()

# CHoCH & BoS
df['CHoCH'] = df['High'].shift(1) < df['High']
df['BoS'] = df['Low'].shift(1) > df['Low']

# Volume Spike
avg_volume = df['Volume'].rolling(window=5).mean()
df['VolumeSpike'] = df['Volume'] > (1.5 * avg_volume)

# Signal Logic
def get_fxgrit_signal(row):
    if (
        row['EMA9'] > row['EMA20'] and
        row['MACD'] > row['SignalLine'] and
        row['CHoCH'] and
        row['BoS'] and
        row['VolumeSpike']
    ):
        return 'BUY'
    elif (
        row['EMA9'] < row['EMA20'] and
        row['MACD'] < row['SignalLine'] and
        not row['CHoCH'] and
        not row['BoS'] and
        row['VolumeSpike']
    ):
        return 'SELL'
    else:
        return 'NO SIGNAL'

df['FXGRIT_SIGNAL'] = df.apply(get_fxgrit_signal, axis=1)
latest = df.iloc[-1]

# GUI START
root = tk.Tk()
root.title("📊 FXGRIT SIGNAL SCREEN")

# Background color based on signal
signal = latest['FXGRIT_SIGNAL']
if signal == 'BUY':
    bg = 'lightgreen'
    msg = '✅ BUY Signal – Trend Confirmed'
elif signal == 'SELL':
    bg = 'red'
    msg = '🔻 SELL Signal – Downtrend Active'
else:
    bg = 'yellow'
    msg = '⚠️ No Signal – Wait for Setup'

root.configure(bg=bg)

label = tk.Label(root, text=msg, font=('Arial', 18, 'bold'), bg=bg)
label.pack(padx=20, pady=40)

time_label = tk.Label(root, text=f"🕒 {latest['Date']} {latest['Time']}", font=('Arial', 14), bg=bg)
time_label.pack()

price_label = tk.Label(root, text=f"📈 Price: {latest['Close']}", font=('Arial', 14), bg=bg)
price_label.pack()

root.mainloop()