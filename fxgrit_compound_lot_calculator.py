import os
import json

# 🚩 Input Paths
balance_file = "/storage/emulated/0/FXGRIT/Wallet/wallet_data.json"
compound_file = "/storage/emulated/0/FXGRIT/Settings/compound_config.json"

# ✅ Load wallet balance
def get_wallet_balance():
    if not os.path.exists(balance_file):
        return 0.0
    with open(balance_file, 'r') as f:
        data = json.load(f)
    return float(data.get("balance", 0))

# ✅ Load compound config
def get_compound_percent():
    if not os.path.exists(compound_file):
        return 2  # default 2% per trade
    with open(compound_file, 'r') as f:
        data = json.load(f)
    return float(data.get("percent", 2))

# ✅ Calculate Lot Size using compound method
def calculate_lot(balance, percent):
    risk_amount = balance * (percent / 100)
    lot = round(risk_amount / 1000, 3)  # approx. 1 lot = 1000 units risk (adjust as per broker)
    return max(0.01, lot)

# 🔁 Execution
balance = get_wallet_balance()
percent = get_compound_percent()
lot_size = calculate_lot(balance, percent)

print(f"✅ Compound Lot Size: {lot_size}")