import kagglehub

print("Attempting to download 'google/paligemma/keras/pali_gemma_3b_mix_224'...")
try:
    path = kagglehub.model_download("google/paligemma/keras/pali_gemma_3b_mix_224")
    print("SUCCESS! Path:", path)
except Exception as e:
    print(f"FAILED 'google': {e}")

print("\nAttempting to download 'keras/paligemma/keras/pali_gemma_3b_mix_224'...")
try:
    path = kagglehub.model_download("keras/paligemma/keras/pali_gemma_3b_mix_224")
    print("SUCCESS! Path:", path)
except Exception as e:
    print(f"FAILED 'keras': {e}")
