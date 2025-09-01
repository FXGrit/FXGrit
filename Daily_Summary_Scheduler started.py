import schedule
import time
import requests

BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = '-1002544936660'  # Free Channel ID

def send_summary():
    summary_msg = """📊 FXGRIT VIP DAILY SUMMARY
🥇 GOLD: +42 pips
🥈 BTCUSD: +102 points
🥉 EURUSD: +28 pips
❌ GBPUSD: -15 pips
🔁 Total Trades: 6
✅ Win: 5 | ❌ Loss: 1
📈 Net P/L: +158 points 🔥

🔓 Join VIP Now – ₹499/month for full signals & bot
👉 https://t.me/+71OHe-MMvpIyY2E1"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': summary_msg}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Summary sent successfully.")
    else:
        print("❌ Failed to send summary:", response.text)

# ⏰ Schedule daily at 22:30 (10:30 PM)
schedule.every().day.at("22:30").do(send_summary)

print("⏳ FXGRIT Daily Summary Scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(30)