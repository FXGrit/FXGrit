import json
import os

state_file = '/storage/emulated/0/FXGRIT/System/lot_state.json'

# अगर फाइल नहीं है तो default values बनाओ
if not os.path.exists(state_file):
    state = {"last_lot": 0.01, "last_result": "WIN"}
    with open(state_file, 'w') as f:
        json.dump(state, f)

# फाइल लोड करो
with open(state_file, 'r') as f:
    state = json.load(f)

last_lot = state['last_lot']
last_result = state['last_result']

# Logic: Compound अगर WIN हुआ हो, Reset अगर LOSS
if last_result == 'WIN':
    new_lot = round(last_lot + 0.002, 3)
else:
    new_lot = 0.01

# Update state
state['last_lot'] = new_lot
with open(state_file, 'w') as f:
    json.dump(state, f)

print(f"✅ Current Lot Size: {new_lot}")