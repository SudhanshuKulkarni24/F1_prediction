import pickle
import requests
import os

CATBOOST_MODEL_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/catboost_model.pkl"
ENCODERS_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/encoders.pkl"

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"🔽 Downloading {filename}...")
        r = requests.get(url)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f"✅ Downloaded {filename}")

# Download and cache model files
download_file(CATBOOST_MODEL_URL, "catboost_model.pkl")
download_file(ENCODERS_URL, "encoders.pkl")

# Load the models
with open("catboost_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

# Unpack encoders
le_driver = encoders["driver"]
le_race = encoders["race"]
