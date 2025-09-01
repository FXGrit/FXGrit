import pandas as pd
import os

# Log file path
log_path = '/storage/emulated/0/FXGRIT/fxgrit_signal_log.xlsx'

# Compound Parameters
BASE_LOT = 0.01
RISK_MULTIPLIER = 0.0001

def calculate_lot():
    if not os.path.exists(log_path):
        print("❌ Log file not found.")
        return BASE_LOT

    df = pd.read_excel(log_path)

    # Calculate total Net Profit (Assuming TP1 hit = +20, SL hit = -10)
    win_count = df[df['Signal'] == 'BUY'].shape[0]  # or any logic
    total_profit = (df['TP1'] - df['Entry']).sum()

    # If any SL hit, subtract those
    sl_loss = (df['Entry'] - df['SL']).sum()

    net_pl = total_profit - sl_loss
    lot_size = round(BASE_LOT + (net_pl * RISK_MULTIPLIER), 2)

    print(f"📊 Net P/L: {net_pl:.2f}")
    print(f"🔁 Suggested Lot Size: {lot_size}")
    return lot_size

# Run calculation
calculate_lot()