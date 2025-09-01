# /storage/emulated/0/FXGrit/FXGritApp/fxgrit_auto_flow.py
"""
FXGRIT AutoFlow - Final
- Uses Ind_fxgrit_auto_flow.csv as data source
- EMA9/EMA20 crossover + RSI + volume filters
- Generates trade_execute.json when signal found
- Logs to Excel (openpyxl) or CSV fallback
- Sends VIP Telegram alerts
- Runs every 5 minutes (300s)
- Auto-updates NSE holiday calendar (cached daily). If holiday => skips processing
"""

import os
import time
import json
import re
from datetime import datetime, date, time as dtime, timedelta
import pytz
import requests
import pandas as pd

# ========== CONFIG ==========
BOT_TOKEN   = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
VIP_CHAT_ID = "-1002433721766"

CSV_PATH    = "/storage/emulated/0/FXGrit/Ind_fxgrit_auto_flow.csv"
SIGNAL_PATH = "/storage/emulated/0/FXGrit/Trades/trade_execute.json"
LOG_XL      = "/storage/emulated/0/FXGrit/Trades/trade_logs.xlsx"
LOG_CSV     = "/storage/emulated/0/FXGrit/Trades/trade_logs.csv"
HOLIDAY_CACHE = "/storage/emulated/0/FXGrit/Config/nse_holidays.json"  # cached holidays
os.makedirs(os.path.dirname(SIGNAL_PATH), exist_ok=True)
os.makedirs(os.path.dirname(HOLIDAY_CACHE), exist_ok=True)

# NSE sources we try (primary + fallbacks)
NSE_URLS = [
    "https://www.nseindia.com/holidays-for-the-calendar-year-{year}",
    "https://www.nseindia.com/resources/exchange-communication-holidays",
    "https://www.niftyindices.com/resources/holiday-calendar",
    "https://zerodha.com/marketintel/holiday-calendar/",
    "https://groww.in/p/nse-holidays"
]

# Market timing
IST = pytz.timezone("Asia/Kolkata")
MARKET_OPEN_TIME = dtime(9, 15)
MARKET_CLOSE_TIME = dtime(15, 30)
LOOP_SECONDS = 300  # 5 minutes interval

# ========== Utilities ==========
def now_ist():
    return datetime.now(IST)

def send_vip(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": VIP_CHAT_ID, "text": message}, timeout=10)
        if r.status_code == 200:
            print("✅ VIP message sent")
        else:
            print(f"❌ Telegram send failed: {r.status_code} {r.text}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def safe_to_excel_or_csv(df: pd.DataFrame, xlsx_path: str, csv_path: str):
    try:
        import openpyxl
        df.to_excel(xlsx_path, index=False)
        print(f"📁 Log saved: {xlsx_path}")
    except Exception as e:
        df.to_csv(csv_path, index=False)
        print(f"📁 Log saved (CSV fallback): {csv_path} | reason: {e}")

# ========== Holiday fetch & parse ==========
def parse_dates_from_text(text):
    """Find date-like strings and return yyyy-mm-dd set. Handles formats like '26 Feb 2025' '26-Feb-2025' and '2025-02-26'."""
    found = set()
    # ISO dates first
    for m in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})", text):
        y, mo, d = m.groups()
        try:
            dt = date(int(y), int(mo), int(d))
            found.add(dt.isoformat())
        except:
            pass

    # Patterns like '26 Feb 2025', '26-Feb-2025', '26 February 2025'
    month_map = {m.lower(): i for i,m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)}
    # more robust: accept full month names too
    month_names = ("January February March April May June July August September October November December").split()
    for m in re.finditer(r"(\d{1,2})\s*[-\u2011–—]?\s*([A-Za-z]+)\s*[,]?\s*(\d{4})", text):
        dstr, mstr, ystr = m.groups()
        mkey = mstr[:3].lower()
        try:
            mo = month_map.get(mkey)
            if mo is None:
                # try full month names
                midx = None
                for idx, name in enumerate(month_names, 1):
                    if name.lower().startswith(mstr.lower()[:3]):
                        midx = idx; break
                mo = midx
            if mo:
                dt = date(int(ystr), int(mo), int(dstr))
                found.add(dt.isoformat())
        except:
            pass

    # Also patterns like 'January 26, 2025'
    for m in re.finditer(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", text):
        mname, dstr, ystr = m.groups()
        mkey = mname[:3].lower()
        try:
            mo = month_map.get(mkey)
            if mo:
                dt = date(int(ystr), int(mo), int(dstr))
                found.add(dt.isoformat())
        except:
            pass

    return found

def fetch_holidays_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and r.text:
            return parse_dates_from_text(r.text)
    except Exception as e:
        print(f"⚠️ Fetch failed for {url}: {e}")
    return set()

def get_nse_holidays(year=None, force_refresh=False):
    """Return a set of YYYY-MM-DD holiday strings for the given year.
       Caches to HOLIDAY_CACHE; refreshes once daily or when force_refresh True."""
    if year is None:
        year = now_ist().year

    # Load cache if present
    try:
        if os.path.exists(HOLIDAY_CACHE) and not force_refresh:
            with open(HOLIDAY_CACHE, "r") as f:
                cache = json.load(f)
            cache_date = cache.get("_fetched_date", "")
            if cache_date:
                fetched_on = datetime.fromisoformat(cache_date)
                if (now_ist() - fetched_on).total_seconds() < 86400:
                    # use cached year if available
                    if str(year) in cache.get("years", {}):
                        return set(cache["years"].get(str(year), []))
    except Exception as e:
        print("⚠️ Holiday cache read error:", e)

    # Try fetching from NSE and fallbacks
    found = set()
    tried = []
    for base in NSE_URLS:
        url = base.format(year=year)
        tried.append(url)
        found |= fetch_holidays_from_url(url)

    # If nothing found for year, also try searching other pages (no year)
    if not found:
        for base in NSE_URLS:
            try:
                found |= fetch_holidays_from_url(base)
            except:
                pass

    # Ensure we pick only dates in requested year
    found = {d for d in found if d.startswith(str(year))}
    # Basic fallback hardcoded small list (if nothing found), keep minimal
    if not found:
        print("⚠️ No holidays parsed from web; using common-known fallbacks for year", year)
        fallback = {
            "01-01", "26-01", "15-08", "02-10", "25-12"
        }
        for mmdd in fallback:
            m, d = mmdd.split("-")
            found.add(f"{year}-{m.zfill(2)}-{d.zfill(2)}")

    # Save cache
    try:
        cache = {"_fetched_date": now_ist().isoformat(), "years": {}}
        if os.path.exists(HOLIDAY_CACHE):
            try:
                with open(HOLIDAY_CACHE, "r") as f: cache = json.load(f)
            except:
                cache = {"_fetched_date": now_ist().isoformat(), "years": {}}
        cache["years"][str(year)] = sorted(list(found))
        cache["_fetched_date"] = now_ist().isoformat()
        with open(HOLIDAY_CACHE, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print("⚠️ Could not write holiday cache:", e)

    return set(found)

# ========== Market open check ==========
def is_market_open():
    now = now_ist()
    # weekends
    if now.weekday() >= 5:
        return False
    # holidays (auto fetch)
    holidays = get_nse_holidays(year=now.year)
    if now.strftime("%Y-%m-%d") in holidays:
        return False
    # time window
    return MARKET_OPEN_TIME <= now.time() <= MARKET_CLOSE_TIME

# ========== Indicators & Strategy ==========
def rsi_series(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs  = avg_gain / (avg_loss.replace(0, 1e-9))
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal():
    if not os.path.exists(CSV_PATH):
        print("❌ Data CSV not found at", CSV_PATH)
        return None

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print("❌ Could not read CSV:", e)
        return None

    required = {"Timestamp","Symbol","Open","High","Low","Close","Volume"}
    missing = required - set(df.columns)
    if missing:
        print("❌ Missing columns in CSV:", missing)
        return None

    # indicators
    df["EMA9"]  = df["Close"].ewm(span=9, adjust=False).mean()
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["RSI"]   = rsi_series(df["Close"], period=14)
    df["VolAvg3"] = df["Volume"].rolling(3).mean()

    if len(df) < 25:
        print("ℹ️ Not enough rows for indicators.")
        return None

    latest = df.iloc[-1]
    prev   = df.iloc[-2]

    crossed_up   = (prev["EMA9"] < prev["EMA20"]) and (latest["EMA9"] > latest["EMA20"])
    crossed_down = (prev["EMA9"] > prev["EMA20"]) and (latest["EMA9"] < latest["EMA20"])

    vol_ok = (latest["VolAvg3"] > 0) and (latest["Volume"] >= latest["VolAvg3"])
    rsi_ok_buy  = latest["RSI"] > 45
    rsi_ok_sell = latest["RSI"] < 55

    symbol = str(latest["Symbol"])
    px = float(latest["Close"])

    if crossed_up and vol_ok and rsi_ok_buy:
        signal = {
            "Asset": symbol,
            "Signal": "BUY",
            "Entry": round(px, 2),
            "SL": round(px - max(0.006*px, 50), 2),
            "TP1": round(px + max(0.012*px, 100), 2),
            "TP2": round(px + max(0.024*px, 200), 2)
        }
    elif crossed_down and vol_ok and rsi_ok_sell:
        signal = {
            "Asset": symbol,
            "Signal": "SELL",
            "Entry": round(px, 2),
            "SL": round(px + max(0.006*px, 50), 2),
            "TP1": round(px - max(0.012*px, 100), 2),
            "TP2": round(px - max(0.024*px, 200), 2)
        }
    else:
        print("ℹ️ No valid signal this bar.")
        return None

    try:
        with open(SIGNAL_PATH, "w") as f:
            json.dump(signal, f)
        print("✅ Signal generated and saved to", SIGNAL_PATH)
    except Exception as e:
        print("❌ Could not write signal file:", e)
        return None

    return signal

# ========== Logging & Execution ==========
def save_log(signal: dict, pnl_expected: float):
    try:
        now_str = now_ist().strftime("%Y-%m-%d %H:%M")
        row = pd.DataFrame([{
            "Time": now_str,
            "Asset": signal.get("Asset", "NA"),
            "Type": signal.get("Signal", "NA"),
            "Entry": signal.get("Entry", 0),
            "SL": signal.get("SL", 0),
            "TP1": signal.get("TP1", 0),
            "TP2": signal.get("TP2", 0),
            "ExpPnL": pnl_expected
        }])
        if os.path.exists(LOG_XL):
            try:
                old = pd.read_excel(LOG_XL)
            except Exception:
                old = pd.read_csv(LOG_CSV) if os.path.exists(LOG_CSV) else pd.DataFrame()
            out = pd.concat([old, row], ignore_index=True)
        elif os.path.exists(LOG_CSV):
            old = pd.read_csv(LOG_CSV)
            out = pd.concat([old, row], ignore_index=True)
        else:
            out = row
        safe_to_excel_or_csv(out, LOG_XL, LOG_CSV)
        print("📁 Trade log updated.")
    except Exception as e:
        print("❌ Log save error:", e)

def send_to_telegram(signal: dict, pnl_expected: float):
    if not signal or "Signal" not in signal:
        print("⚠️ Empty or invalid signal, skipping Telegram.")
        return
    msg = (
        f"📢 FXGRIT VIP ALERT\n"
        f"✅ Signal: {signal.get('Signal','NA')}\n"
        f"💰 Asset: {signal.get('Asset','NA')}\n"
        f"🎯 Entry: {signal.get('Entry','NA')}\n"
        f"🛑 SL: {signal.get('SL','NA')}\n"
        f"🎯 TP1: {signal.get('TP1','NA')}\n"
        f"🎯 TP2: {signal.get('TP2','NA')}\n"
        f"💹 Expected PnL: {pnl_expected} pts"
    )
    send_vip(msg)

def execute_trade(signal: dict):
    if not signal or "Signal" not in signal:
        print("⚠️ No trade to execute.")
        return
    print(f"🚀 Executing {signal['Signal']} for {signal['Asset']}")
    print(f"🎯 Entry {signal['Entry']} | 🛑 SL {signal['SL']} | 🎯 TP1 {signal['TP1']} | 🎯 TP2 {signal['TP2']}")
    pnl_expected = round((signal["TP1"] - signal["Entry"]) if signal["Signal"] == "BUY" else (signal["Entry"] - signal["TP1"]), 2)
    save_log(signal, pnl_expected)
    send_to_telegram(signal, pnl_expected)
    try:
        if os.path.exists(SIGNAL_PATH):
            os.remove(SIGNAL_PATH)
            print("🗑️ trade_execute.json deleted after execution.")
    except Exception as e:
        print("⚠️ Could not delete signal file:", e)

# ========== Main loop ==========
def main_loop():
    print("🔁 FXGRIT AutoFlow Started...")
    # prefetch holidays for this year
    _ = get_nse_holidays(now_ist().year, force_refresh=False)
    while True:
        try:
            # Refresh holidays daily (if midnight IST passed)
            # If cache older than 24h, get_nse_holidays will refresh automatically
            if not is_market_open():
                print(f"⏳ Market closed or holiday/weekend - {now_ist().strftime('%Y-%m-%d %H:%M')}. Next check after {LOOP_SECONDS}s")
                time.sleep(LOOP_SECONDS)
                continue

            if not os.path.exists(SIGNAL_PATH):
                sig = generate_signal()
                if sig:
                    execute_trade(sig)
            else:
                # if signal file already present (maybe from other process), just execute it
                try:
                    with open(SIGNAL_PATH, "r") as f:
                        sig = json.load(f)
                    execute_trade(sig)
                except Exception as e:
                    print("❌ Could not read existing signal file:", e)
        except Exception as e:
            print("❌ Error in main loop:", e)
        time.sleep(LOOP_SECONDS)

if __name__ == "__main__":
    main_loop()
