import tarfile
import os

tar_path = r"d:\Users\axeld\MCIT\VisionLink\VisionLink\paligemma-keras-pali_gemma_3b_mix_224-v4.tar.gz"
extract_path = r"d:\Users\axeld\MCIT\VisionLink\VisionLink\pali_gemma_local_model"

if not os.path.exists(extract_path):
    os.makedirs(extract_path)

print(f"Extracting {tar_path} to {extract_path}...")
try:
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_path)
    print("Extraction complete.")
except Exception as e:
    print(f"Error extracting: {e}")
