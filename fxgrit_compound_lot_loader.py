# 🧠 Compound Lot Size Load (Attach this wherever needed)
def get_compound_lot():
    try:
        with open("/storage/emulated/0/FXGRIT/Wallet/wallet_data.json") as f:
            balance = float(json.load(f).get("balance", 0))
        with open("/storage/emulated/0/FXGRIT/Settings/compound_config.json") as f:
            percent = float(json.load(f).get("percent", 2))
        lot = round((balance * percent) / 1000, 3)
        return max(0.01, lot)
    except:
        return 0.01