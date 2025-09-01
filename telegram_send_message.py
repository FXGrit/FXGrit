import requests

def send_telegram(message):
    bot_token = "7908555569:AAFvSdGRDXfgrGc0mS2Gx1mmY9UmND_crG8"
    chat_id = "6183259863"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=data)
    print("📨 Telegram Status:", response.status_code)