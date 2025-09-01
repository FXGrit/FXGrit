import requests
from datetime import datetime

# ✅ Replace this with your real token and chat_id
BOT_TOKEN = '7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8'
CHAT_ID = 'PASTE_YOUR_CHAT_ID_HERE'  # Important: Replace this in next step

def send_telegram_message(signal_type, entry, sl, tp1, tp2):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"""📢 FXGRIT ALERT
🕒 Time: {now}
✅ Signal: {signal_type}
🎯 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}"""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ Telegram signal sent successfully!")
    else:
        print("❌ Failed to send Telegram message:", response.text)