import json
import os
from datetime import datetime

# File Path
risk_file = "/storage/emulated/0/FXGRIT/System/risk_limit_state.json"
today = datetime.now().strftime("%Y-%m-%d")

# Configurable Limits
MAX_TRADES = 5
MAX_LOSS = 500.0  # Currency value (can be in INR/USD etc.)

# Default structure
default_data = {
    "date": today,
    "total_trades": 0,
    "total_loss": 0.0
}

# Load or initialize
if not os.path.exists(risk_file):
    data = default_data
else:
    with open(risk_file, "r") as f:
        data = json.load(f)

# Reset if new day
if data["date"] != today:
    data = default_data

# ✅ Check Conditions
if data["total_trades"] >= MAX_TRADES:
    print("❌ Daily Trade Limit Reached.")
    exit()

if data["total_loss"] >= MAX_LOSS:
    print("❌ Daily Loss Limit Reached.")
    exit()

# ✅ Trade is allowed → increment counters
data["total_trades"] += 1

# ✅ You can update this after trade completes:
# For example, add this after trade:
# data["total_loss"] += actual_loss_amount

# Save state
with open(risk_file, "w") as f:
    json.dump(data, f)

print("✅ Risk Check Passed – Trade Allowed.")