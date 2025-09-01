import pandas as pd

# ✅ CSV File Path
file_path = '/storage/emulated/0/FXGRIT/fxgrit_advanced_chart_data.csv'
df = pd.read_csv(file_path)

# ✅ Indicators
df['EMA9'] = df['Close'].ewm(span=9).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()
df['EMA12'] = df['Close'].ewm(span=12).mean()
df['EMA26'] = df['Close'].ewm(span=26).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['SignalLine'] = df['MACD'].ewm(span=9).mean()
df['CHoCH'] = df['High'].shift(1) < df['High']
df['BoS'] = df['Low'].shift(1) > df['Low']
avg_vol = df['Volume'].rolling(window=5).mean()
df['VolumeSpike'] = df['Volume'] > (1.5 * avg_vol)

# ✅ Signal Logic
def get_signal(row):
    if (
        row['EMA9'] > row['EMA20'] and
        row['MACD'] > row['SignalLine'] and
        row['CHoCH'] and row['BoS'] and row['VolumeSpike']
    ):
        return 'BUY'
    elif (
        row['EMA9'] < row['EMA20'] and
        row['MACD'] < row['SignalLine'] and
        not row['CHoCH'] and not row['BoS'] and row['VolumeSpike']
    ):
        return 'SELL'
    else:
        return 'NO SIGNAL'

df['FXGRIT_SIGNAL'] = df.apply(get_signal, axis=1)
latest = df.iloc[-1]
signal = latest['FXGRIT_SIGNAL']
close = round(latest['Close'], 5)

# ✅ Trailing SL Calculation
risk = 0.0010  # 10 pip
entry = sl = tp1 = tp2 = tsl = 0

if signal == 'BUY':
    entry = close
    sl = round(entry - risk, 5)
    price_moved = close - entry
    if price_moved >= 0.0020:
        tsl = round(entry + price_moved - 0.0010, 5)
    tp1 = round(entry + risk * 2, 5)
    tp2 = round(entry + risk * 3, 5)

elif signal == 'SELL':
    entry = close
    sl = round(entry + risk, 5)
    price_moved = entry - close
    if price_moved >= 0.0020:
        tsl = round(entry - price_moved + 0.0010, 5)
    tp1 = round(entry - risk * 2, 5)
    tp2 = round(entry - risk * 3, 5)

# ✅ Output
print("🔔 FXGRIT TRAILING SL MODE v1.2")
print("📊 Signal:", signal)
if signal in ['BUY', 'SELL']:
    print("💰 Entry:", entry)
    print("🛡️ Original SL:", sl)
    print("🔄 Trailing SL:", tsl if tsl != 0 else "Not Triggered Yet")
    print("🎯 TP1:", tp1)
    print("🎯 TP2:", tp2)
else:
    print("⚠️ No Trade Signal. Please Wait.")