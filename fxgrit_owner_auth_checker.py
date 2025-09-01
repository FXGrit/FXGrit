import json
import os

owner_file = "/storage/emulated/0/FXGRIT/Auth/owner_auth.json"

if os.path.exists(owner_file):
    with open(owner_file, 'r') as f:
        data = json.load(f)
        print("✅ Owner Auth Found:", data["name"], "-", data["mobile"])
else:
    print("❌ Owner auth file not found")