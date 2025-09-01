VIP_CHAT_ID = '-1002433721766'
FREE_CHAT_ID = '-1002544936660'

def send_vip_signal(msg):
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', data={
        'chat_id': VIP_CHAT_ID, 'text': msg
    })

def send_free_summary(signal, asset, tp1, tp2):
    summary = f"""📢 FXGRIT FREE SIGNAL
✅ Signal: {signal}
💰 Asset: {asset}
🎯 Target Zone: {tp1} to {tp2}
🚀 Join VIP for full details!
👉 https://t.me/+LjCZa8100yE4ODE1"""
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', data={
        'chat_id': FREE_CHAT_ID, 'text': summary
    })