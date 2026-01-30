import kagglehub
import os

# Download latest version
print("Downloading model...")
try:
    path = kagglehub.model_download("keras/paligemma/keras/pali_gemma_3b_mix_224")
    print("Path to model files:", path)
except Exception as e:
    print(f"Error downloading: {e}")
