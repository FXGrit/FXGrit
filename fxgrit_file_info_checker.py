import pandas as pd

file_path = "/storage/emulated/0/FXGrit/fxgrit_advanced_chart_data.csv"

df = pd.read_csv(file_path)

print("✅ File mil gayi – Columns yeh hain:")
print(df.columns.tolist())

print("✅ Total rows:", len(df))