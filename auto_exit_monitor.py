# auto_exit_monitor.py
# 🔁 FXGRIT Auto Exit + Trailing Monitor
import json, os, time
from datetime import datetime

# ---------------- Paths ----------------
exec_path = "/storage/emulated/0/FXGRIT/Logs/Executed/active_trades.json"
live_path = "/storage/emulated/0/FXGRIT/Data/live_prices.json"
close_path = "/storage/emulated/0/FXGRIT/Logs/Closed/closed_trades.json"
os.makedirs(os.path.dirname(close_path), exist_ok=True)

# ---------------- Entry Price Mapping ----------------
entry_prices = {
    "NIFTY_23700_CALL": 124.5,
    "NIFTY_23600_PUT": 115.2,
    "BANKNIFTY_52500_CALL": 304.6,
    "RELIANCE_3000_PUT": 89.7
}

# ---------------- Helper Functions ----------------
def get_key(asset, strike, opt_type):
    return f"{asset}_{strike}_{opt_type}"

def get_live_price(key, live_data):
    try:
        return float(live_data.get(key, 0))
    except:
        return 0

def log_exit(trade, exit_price):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_tag = now.strftime("%Y-%m-%d")

    key = get_key(trade["asset"], trade["strike"], trade["type"])
    entry_price = entry_prices.get(key, 0)
    pnl = round(exit_price - entry_price, 2)

    exit_data = {
        "asset": trade["asset"],
        "strike": trade["strike"],
        "type": trade["type"],
        "strategy": trade.get("strategy", ""),
        "entry": entry_price,
        "exit": exit_price,
        "pnl": pnl,
        "time": timestamp
    }

    if os.path.exists(close_path):
        with open(close_path) as f:
            closed = json.load(f)
    else:
        closed = {}

    closed.setdefault(date_tag, []).append(exit_data)

    with open(close_path, "w") as f:
        json.dump(closed, f, indent=2)

    print(f"✅ Auto Exit: {key} | P&L: {pnl}")

# ---------------- Main Loop ----------------
while True:
    try:
        # Wait if files not present
        if not os.path.exists(exec_path) or not os.path.exists(live_path):
            print("⏳ Waiting for trade or price file...")
            time.sleep(5)
            continue

        # Load active trades
        with open(exec_path) as f:
            active = json.load(f)

        # Load live prices
        with open(live_path) as f:
            prices = json.load(f)

        for date in list(active.keys()):
            trades = active[date]
            new_trades = []

            for trade in trades:
                try:
                    key = get_key(trade["asset"], trade["strike"], trade["type"])
                    live = get_live_price(key, prices)
                    if live == 0: 
                        new_trades.append(trade)
                        continue

                    entry = entry_prices.get(key, 0)
                    # Example trailing exit logic
                    if (trade["type"].upper() == "CALL" and (live - entry) >= 5) or \
                       (trade["type"].upper() == "PUT" and (entry - live) >= 5):
                        log_exit(trade, live)
                    else:
                        new_trades.append(trade)

                except KeyError as e:
                    print(f"❌ Trade Key Missing: {e}")
                    new_trades.append(trade)
                except Exception as e:
                    print(f"❌ Trade Processing Error: {e}")
                    new_trades.append(trade)

            # Update active trades
            if new_trades:
                active[date] = new_trades
            else:
                del active[date]

        # Save updated active trades
        with open(exec_path, "w") as f:
            json.dump(active, f, indent=2)

    except Exception as e:
        print(f"❌ Exit Monitor Error: {e}")

    time.sleep(5)
