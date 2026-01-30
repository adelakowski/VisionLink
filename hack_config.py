import json
import shutil
import os

task_path = r"d:\Users\axeld\MCIT\VisionLink\VisionLink\pali_gemma_local_model\task.json"
backup_path = task_path + ".bak"

# Backup
if not os.path.exists(backup_path):
    shutil.copy(task_path, backup_path)
    print("Backed up task.json")

# Read
with open(task_path, "r") as f:
    data = json.load(f)

# Modify
if "config" in data and "preprocessor" in data["config"]:
    print("Removing preprocessor from config...")
    data["config"]["preprocessor"] = None

# Write
with open(task_path, "w") as f:
    json.dump(data, f, indent=4)
print("Updated task.json to remove preprocessor.")
