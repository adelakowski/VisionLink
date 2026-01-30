import kagglehub
from kagglehub.config import get_kaggle_credentials

try:
    creds = get_kaggle_credentials()
    print(f"Authenticated as: {creds['username']}")
    print(f"Key starts with: {creds['key'][:5]}...")
except Exception as e:
    print(f"Auth error: {e}")
