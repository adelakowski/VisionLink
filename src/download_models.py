import os
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

load_dotenv()

token = os.environ.get("HF_TOKEN")
if not token:
    print("WARNING: HF_TOKEN not found! Model download may fail if models are gated.")

print("Downloading google/paligemma-3b-mix-224...")
snapshot_download(
    repo_id="google/paligemma-3b-mix-224",
    token=token,
    ignore_patterns=["*.msgpack", "*.h5", "coreml/*"]
)

print("Downloading google/gemma-2-2b-it...")
snapshot_download(
    repo_id="google/gemma-2-2b-it",
    token=token,
    ignore_patterns=["*.msgpack", "*.h5", "coreml/*"]
)

print("Models successfully downloaded and cached!")
