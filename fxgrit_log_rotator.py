import os
import shutil
from datetime import datetime

# 🔃 Rotate if log > 1MB
log_file = '/storage/emulated/0/FXGrit/fxgrit_signal_log.xlsx'
backup_folder = '/storage/emulated/0/FXGrit/backup_logs/'

def rotate_log_file():
    if os.path.exists(log_file):
        size = os.path.getsize(log_file)
        if size > 1_000_000:  # ~1 MB
            now = datetime.now().strftime("%Y-%m-%d_%H-%M")
            new_name = f"{backup_folder}signal_log_{now}.xlsx"
            shutil.move(log_file, new_name)
            print(f"📁 Backup Created: {new_name}")