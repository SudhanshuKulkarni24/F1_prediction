import pickle
import os
import requests
from io import BytesIO

# GitHub raw URLs
CATBOOST_MODEL_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/catboost_model.pkl"
ENCODERS_URL = "https://raw.githubusercontent.com/SudhanshuKulkarni24/F1_prediction/main/models/encoders.pkl"

encoder = {}

def download_and_load_pickle(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return pickle.load(BytesIO(resp.content))
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def load_models():
    global encoder
    models = {}

    # Download from GitHub if running on Vercel
    if os.getenv("VERCEL") == "1" or os.getenv("VERCEL_ENV"):
        print("[INFO] Loading model from GitHub...")
        models_dict = download_and_load_pickle(CATBOOST_MODEL_URL)
        encoder = download_and_load_pickle(ENCODERS_URL)
    else:
        print("[INFO] Loading model locally...")
        with open("models/catboost_model.pkl", "rb") as f:
            models_dict = pickle.load(f)
        with open("models/encoders.pkl", "rb") as f:
            encoder = pickle.load(f)

    if not models_dict or not encoder:
        raise RuntimeError("❌ Failed to load model or encoders")

    return models_dict
