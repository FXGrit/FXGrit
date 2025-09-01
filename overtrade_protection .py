import json
import os
import time
from datetime import datetime, timedelta

SETTINGS_PATH = "/storage/emulated/0/FXGRIT/Settings/user_settings.json"
TRACKER_PATH = "/storage/emulated/0/FXGRIT/System/trade_tracker.json"

def load_user_settings():
    try:
        with open(SETTINGS_PATH) as f:
            return json.load(f)
    except:
        return {"daily_trade_limit": 3, "cooldown_minutes": 15, "enable_overtrade_protection": True}

def load_trade_tracker():
    if not os.path.exists(TRACKER_PATH):
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "trades_today": 0,
            "profit_trades": 0,
            "last_trade_time": "1970-01-01 00:00:00"
        }
    with open(TRACKER_PATH) as f:
        return json.load(f)

def save_trade_tracker(data):
    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f)

def overtrade_check():
    settings = load_user_settings()
    if not settings.get("enable_overtrade_protection", True):
        return True, "✅ Protection Disabled"

    tracker = load_trade_tracker()
    now = datetime.now()

    # Reset tracker if date changed
    if tracker["date"] != now.strftime("%Y-%m-%d"):
        tracker["date"] = now.strftime("%Y-%m-%d")
        tracker["trades_today"] = 0
        tracker["profit_trades"] = 0
        tracker["last_trade_time"] = "1970-01-01 00:00:00"

    # Check max trades limit
    if tracker["trades_today"] >= settings.get("daily_trade_limit", 3):
        return False, "❌ Max trade limit reached today"

    # Cooldown timer
    last_time = datetime.strptime(tracker["last_trade_time"], "%Y-%m-%d %H:%M:%S")
    cooldown = timedelta(minutes=settings.get("cooldown_minutes", 15))
    if now - last_time < cooldown:
        remaining = cooldown - (now - last_time)
        return False, f"⏳ Cooldown active ({int(remaining.total_seconds() // 60)} min left)"

    # Profit lock
    if tracker["profit_trades"] >= 2:
        return False, "🔒 Profit Lock Activated (2 profitable trades)"

    return True, "✅ Trade allowed"

def update_trade_tracker(profitable=False):
    tracker = load_trade_tracker()
    tracker["trades_today"] += 1
    if profitable:
        tracker["profit_trades"] += 1
    tracker["last_trade_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_trade_tracker(tracker)