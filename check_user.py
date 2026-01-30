import kaggle
try:
    print(f"Current API User: {kaggle.api.get_config_value('username')}")
except Exception as e:
    print(f"Error checking user: {e}")
