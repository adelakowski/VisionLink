import kagglehub

handles_to_test = [
    "keras/paligemma/keras/pali_gemma_3b_mix_224", # Standard ID (underscores)
    "keras/paligemma/keras/paligemma_3b_mix_224",  # User suggested (no underscores)
    "google/paligemma/keras/pali_gemma_3b_mix_224", # Google - underscore
    "google/paligemma/keras/paligemma_3b_mix_224",  # Google - no underscore
    "google/paligemma/jax/pali_gemma_3b_mix_224",   # Google - JAX
]

print("--- TESTING DOWNLOAD HANDLES ---")
for handle in handles_to_test:
    print(f"\nTesting: {handle}")
    try:
        path = kagglehub.model_download(handle)
        print(f"✅ SUCCESS! Path: {path}")
        # Save working handle to file
        with open("working_handle.txt", "w") as f:
            f.write(handle)
        break
    except Exception as e:
        print(f"❌ FAILED: {e}")
