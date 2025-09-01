import json
import os

# Step 4: Validation System
auth_folder = "/storage/emulated/0/FXGRIT/Auth"
owner_file = os.path.join(auth_folder, "owner_auth.json")
foc_file = os.path.join(auth_folder, "foc_members.json")

def validate_user(mobile_number, broker_id):
    # Check if user is owner
    if os.path.exists(owner_file):
        with open(owner_file, 'r') as f:
            owner = json.load(f)
            if owner['mobile'] == mobile_number:
                return "OWNER ✅ Full Access"

    # Check if user is FOC member
    if os.path.exists(foc_file):
        with open(foc_file, 'r') as f:
            foc_list = json.load(f)
            for member in foc_list:
                if member['mobile'] == mobile_number and member['broker_id'] == broker_id:
                    return f"FOC Member ✅ Access granted to {member['name']}"

    # If neither owner nor FOC
    return "❌ Unauthorized – No access"

# 🔍 Example test
test_mobile = "7669980001"
test_broker_id = "123456789"
result = validate_user(test_mobile, test_broker_id)
print(result)