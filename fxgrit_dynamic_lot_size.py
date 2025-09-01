def get_live_broker_balance():  
    # 🔐 Future logic to fetch real balance from broker API
    return 315.25  # Just a simulated value

def get_compound_lot():
    try:
        with open("/storage/emulated/0/FXGRIT/Settings/user_settings.json") as f:
            user = json.load(f)

        if not user.get("compound_permission"):
            return 0.01  # Compound not allowed

        balance = get_live_broker_balance()
        percent = 2  # Can also be user-controlled
        lot = round((balance * percent) / 1000, 3)
        return max(0.01, lot)

    except:
        return 0.01