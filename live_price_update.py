# 🔁 FXGRIT Simulated Live Price Feeder
import json, time, random, os

path = "/storage/emulated/0/FXGRIT/Data"
os.makedirs(path, exist_ok=True)

live_prices_path = f"{path}/live_prices.json"

# Dummy options list
options = [
    "NIFTY_23700_CALL",
    "NIFTY_23600_PUT",
    "BANKNIFTY_52500_CALL",
    "RELIANCE_3000_PUT"
]

def simulate_prices():
    prices = {}
    for opt in options:
        base = random.uniform(90, 250)
        move = random.uniform(-1.5, 1.5)
        prices[opt] = round(base + move, 2)
    return prices

while True:
    prices = simulate_prices()
    with open(live_prices_path, "w") as f:
        json.dump(prices, f, indent=2)
    print("✅ Live Prices Updated")
    time.sleep(5)