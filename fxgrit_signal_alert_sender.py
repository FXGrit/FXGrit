import requests, json, time, os
from datetime import datetime

# 🔹 Telegram VIP details
BOT_TOKEN = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
VIP_CHAT_ID = "1002416993114"

# 🔹 Paths
LIVE_JSON = "/storage/emulated/0/FXGrit/Data/live_prices.json"
EXEC_JSON = "/storage/emulated/0/FXGrit/Logs/Executed/active_trades.json"
CLOSE_JSON = "/storage/emulated/0/FXGrit/Logs/Closed/closed_trades.json"

# 🔹 Entry price mapping (dummy / initial)
entry_prices = {
    "NIFTY_23700_CALL": 124.5,
    "NIFTY_23600_PUT": 115.2,
    "BANKNIFTY_52500_CALL": 304.6,
    "RELIANCE_3000_PUT": 89.7
}

# 🔹 Circular buffer limit
BUFFER_LIMIT = 1000

# 🔹 Check if current time is within market hours (Mon–Fri 9:15–15:30)
def market_open():
    now = datetime.now()
    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False
    start = now.replace(hour=9, minute=15, second=0, microsecond=0)
    end = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return start <= now <= end

# 🔹 Fetch NSE live data
def fetch_nifty_live():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.nseindia.com/option-chain",
        "Origin": "https://www.nseindia.com"
    }
    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            return res.json()
        except Exception as e:
            print(f"⚠ Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return {}

def parse_live_prices(data):
    prices = {}
    try:
        for item in data.get('records', {}).get('data', []):
            if 'CE' in item:
                strike = item['CE']['strikePrice']
                key = f"NIFTY_{strike}_CALL"
                prices[key] = item['CE']['lastPrice']
            if 'PE' in item:
                strike = item['PE']['strikePrice']
                key = f"NIFTY_{strike}_PUT"
                prices[key] = item['PE']['lastPrice']
    except Exception as e:
        print(f"❌ Parsing Error: {e}")
    return prices

# 🔹 Send VIP Telegram signal
def send_telegram_signal(signal_type, key, entry, sl, tp1, tp2):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"""📢 FXGRIT VIP ALERT
🕒 Time: {now}
✅ Signal: {signal_type}
🎯 Asset: {key}
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": VIP_CHAT_ID, "text": message}
    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print(f"✅ VIP signal sent: {key}")
        else:
            print(f"❌ Failed to send signal: {res.text}")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# 🔹 Log closed trades
def log_exit(trade, exit_price):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_tag = now.strftime("%Y-%m-%d")

    key = f"{trade['asset']}_{trade['strike']}_{trade['type']}"
    entry_price = entry_prices.get(key, 0)
    pnl = round(exit_price - entry_price, 2)

    exit_data = {
        "asset": trade["asset"],
        "strike": trade["strike"],
        "type": trade["type"],
        "strategy": trade["strategy"],
        "entry": entry_price,
        "exit": exit_price,
        "pnl": pnl,
        "time": timestamp
    }

    os.makedirs(os.path.dirname(CLOSE_JSON), exist_ok=True)
    if os.path.exists(CLOSE_JSON):
        with open(CLOSE_JSON) as f:
            closed = json.load(f)
    else:
        closed = {}

    closed.setdefault(date_tag, []).append(exit_data)

    # 🔹 Circular buffer check
    for date in list(closed.keys()):
        if len(closed[date]) > BUFFER_LIMIT:
            closed[date] = closed[date][-BUFFER_LIMIT:]

    with open(CLOSE_JSON, "w") as f:
        json.dump(closed, f, indent=2)

    print(f"✅ Auto Exit: {key} | P&L: {pnl}")

# 🔹 Main loop
def main_loop():
    os.makedirs(os.path.dirname(LIVE_JSON), exist_ok=True)
    os.makedirs(os.path.dirname(EXEC_JSON), exist_ok=True)

    while True:
        if not market_open():
            print("⏳ Market closed. Waiting for next open...")
            time.sleep(60)
            continue

        raw_data = fetch_nifty_live()
        live_prices = parse_live_prices(raw_data)
        if live_prices:
            with open(LIVE_JSON, "w") as f:
                json.dump(live_prices, f, indent=2)
            print("✅ Live prices updated")

            # 🔹 Load active trades
            if os.path.exists(EXEC_JSON):
                with open(EXEC_JSON) as f:
                    active = json.load(f)
            else:
                active = {}

            for date in list(active.keys()):
                trades = active[date]
                new_trades = []
                for trade in trades:
                    key = f"{trade['asset']}_{trade['strike']}_{trade['type']}"
                    live = float(live_prices.get(key, 0))
                    if live == 0: 
                        new_trades.append(trade)
                        continue

                    entry = entry_prices.get(key, live)
                    # 🔹 Example exit logic: 5-point move
                    if abs(live - entry) >= 5:
                        log_exit(trade, live)
                        send_telegram_signal(
                            "BUY" if live > entry else "SELL",
                            key,
                            entry,
                            entry - 2,
                            entry + 5,
                            entry + 10
                        )
                    else:
                        new_trades.append(trade)

                if new_trades:
                    active[date] = new_trades
                else:
                    del active[date]

            with open(EXEC_JSON, "w") as f:
                json.dump(active, f, indent=2)
        else:
            print("⚠ No live prices parsed or fetch failed")

        time.sleep(300)  # 5-minute interval

if __name__ == "__main__":
    main_loop()
