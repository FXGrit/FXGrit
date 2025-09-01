from datetime import datetime, timedelta
import os
import shutil

log_folder = "/storage/emulated/0/FXGrit/Logs/"

def cleanup_logs():
    print("🧹 Checking logs...")
    now = datetime.now()
    deleted = 0
    for filename in os.listdir(log_folder):
        file_path = os.path.join(log_folder, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_time > timedelta(days=2):
                os.remove(file_path)
                print("✅ Deleted:", filename)
                deleted += 1
    if deleted == 0:
        print("ℹ️ No old logs found.")

# ✅ Run cleanup immediately for test
cleanup_logs()