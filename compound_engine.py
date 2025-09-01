import json
import os

# Path setup
settings_path = "/storage/emulated/0/FXGRIT/Settings"
os.makedirs(settings_path, exist_ok=True)

# Settings data
user_settings = {
    "country": "India",
    "compound_permission": True,
    "gamma_blast_permission": True
}

# Save JSON file
with open(f"{settings_path}/user_settings.json", "w") as f:
    json.dump(user_settings, f, indent=4)

print("✅ User Settings file created successfully.")
print(f"📁 Path: {settings_path}/user_settings.json")