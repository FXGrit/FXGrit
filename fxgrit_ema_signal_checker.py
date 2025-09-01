import pandas as pd

# ✅ आपकी CSV फाइल का रास्ता
file_path = "/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data.csv"

# ✅ फाइल को पढ़ें
df = pd.read_csv(file_path)

# ✅ EMA निकालना (Close price से)
df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()

# ✅ पिछले और अभी के EMA मान
ema_9_prev = df['EMA_9'].iloc[-2]
ema_20_prev = df['EMA_20'].iloc[-2]
ema_9_now = df['EMA_9'].iloc[-1]
ema_20_now = df['EMA_20'].iloc[-1]

# ✅ FXGrit Signal Logic
print("\n📊 FXGrit Signal Check:")
print(f"👈 Previous EMA9: {ema_9_prev:.4f}, EMA20: {ema_20_prev:.4f}")
print(f"👉 Current  EMA9: {ema_9_now:.4f}, EMA20: {ema_20_now:.4f}")

if ema_9_prev < ema_20_prev and ema_9_now > ema_20_now:
    print("✅ FXGrit ENTRY: BUY Signal Confirmed ✅")
elif ema_9_prev > ema_20_prev and ema_9_now < ema_20_now:
    print("🔻 FXGrit ENTRY: SELL Signal Confirmed 🔻")
else:
    print("🚫 No Entry Signal")