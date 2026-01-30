import kaggle
import os

# This loads the credentials from C:\Users\axeld\.kaggle\kaggle.json
api_client = kaggle.KaggleApi()
api_client.authenticate()

print(f"--- IDENTITY CHECK ---")
print(f"Script is logged in as:  {api_client.get_config_value('username')}")
print(f"Key file location:       {kaggle.api.config_file}")
print(f"----------------------")
